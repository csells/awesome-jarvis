"""Supervise only this installation's children; never stop the host's other model services."""
import asyncio
import contextlib
import fcntl
import json
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import signal
import sys
import subprocess
import time
import urllib.request


def logger(directory, name):
    log = logging.getLogger('jarvis-voice.'+name)
    log.setLevel(logging.INFO)
    handler = RotatingFileHandler(directory/(name+'.log'), maxBytes=5*1024*1024, backupCount=3)
    handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    log.addHandler(handler)
    return log


def process_details(pid):
    result = subprocess.run(['/bin/ps', '-p', str(pid), '-o', 'lstart=', '-o', 'command='], capture_output=True, text=True)
    fields = result.stdout.strip().split(None, 5)
    return (' '.join(fields[:5]), fields[5]) if result.returncode == 0 and len(fields) == 6 else (None, None)


def process_identity(pid, argv):
    started, _ = process_details(pid)
    # Homebrew's Python launcher execs Python.app after spawn. Its executable path
    # changes, but creation time and the script argument remain stable.
    marker = argv[1] if len(argv) > 1 and argv[1].endswith('.py') else ' '.join(argv)
    return {'started': started, 'marker': marker}


def matches_process(pid, identity):
    if not isinstance(identity, dict) or not identity.get('started'):
        return False
    started, command = process_details(pid)
    return started == identity['started'] and identity['marker'] in command


async def recover_orphans(pids_file, names, log):
    if not pids_file.exists():
        return
    previous = json.loads(pids_file.read_text())
    identities = previous.get('identities', {})
    for name in names:
        pid = previous.get(name)
        expected = identities.get(name)
        if not pid or not expected or not matches_process(pid, expected):
            continue
        # The exclusive supervisor lock is held. Creation time plus command verifies
        # identity before signaling, so a recycled PID cannot kill unrelated work.
        log.warning('Cleaning up orphaned %s pid=%s', name, pid)
        os.kill(pid, signal.SIGTERM)
        for _ in range(50):
            await asyncio.sleep(.1)
            if not matches_process(pid, expected):
                break
        else:
            if matches_process(pid, expected):
                os.kill(pid, signal.SIGKILL)
        for _ in range(50):
            if not matches_process(pid, expected):
                break
            await asyncio.sleep(.1)
        else:
            raise RuntimeError(f'Orphaned {name} pid={pid} did not exit')


async def supervise(config, log_dir):
    log = logger(log_dir, 'supervisor')
    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, stop.set)
    children = {}
    pids_file = log_dir.parent/'pids.json'
    await recover_orphans(pids_file, config['processes'], log)
    identities = {}

    def save_pids():
        temp = pids_file.with_suffix('.tmp')
        temp.write_text(json.dumps({'supervisor': os.getpid(), **{n:p.pid for n,p in children.items() if p.returncode is None}, 'identities': identities}))
        temp.replace(pids_file)

    async def terminate(process):
        if process.returncode is None:
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), 15)
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()

    async def worker(name, spec):
        output = logger(log_dir, name)
        while not stop.is_set():
            env = {**os.environ, **config['environment'], **spec.get('environment', {})}
            process = await asyncio.create_subprocess_exec(*spec['argv'], cwd=config['working_directory'], env=env,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT, limit=1024*1024)
            children[name] = process
            identities[name] = process_identity(process.pid, spec['argv'])
            save_pids()
            log.info('Started %s pid=%s', name, process.pid)
            started = time.monotonic()
            async def read_output():
                while line := await process.stdout.readline():
                    output.info('%s', line.decode(errors='replace').rstrip())
            async def watchdog():
                failures = 0
                while process.returncode is None and not stop.is_set():
                    await asyncio.sleep(30)
                    if time.monotonic()-started < 150:
                        continue
                    try:
                        def check():
                            with urllib.request.urlopen(spec['health_url'], timeout=8) as r:
                                return r.status == 200 and (name != 'realtime' or all(u.get('state') != 'stuck' for u in json.load(r).get('units', [])))
                        healthy = await asyncio.to_thread(check)
                    except Exception:
                        healthy = False
                    failures = 0 if healthy else failures+1
                    if failures >= 3:
                        log.error('%s failed three health probes; restarting owned pid=%s', name, process.pid)
                        await terminate(process)
                        return
            reader = asyncio.create_task(read_output())
            watcher = asyncio.create_task(watchdog())
            waiter = asyncio.create_task(stop.wait())
            exited = asyncio.create_task(process.wait())
            await asyncio.wait([waiter, exited], return_when=asyncio.FIRST_COMPLETED)
            if stop.is_set():
                await terminate(process)
            watcher.cancel()
            waiter.cancel()
            await asyncio.gather(watcher, waiter, return_exceptions=True)
            await reader
            log.info('%s exited code=%s', name, process.returncode)
            save_pids()
            if not stop.is_set():
                try:
                    await asyncio.wait_for(stop.wait(), 5)
                except asyncio.TimeoutError:
                    pass
    tasks = [asyncio.create_task(worker(name, spec)) for name,spec in config['processes'].items()]
    try:
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION)
        for task in done:
            task.result()
    finally:
        stop.set()
        await asyncio.gather(*tasks, return_exceptions=True)
        log.info('All owned services stopped')
        with contextlib.suppress(FileNotFoundError):
            pids_file.unlink()


if __name__ == '__main__':
    os.umask(0o077)
    config_path = Path(sys.argv[1])
    log_dir = config_path.parent/'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    lock = (config_path.parent/'supervisor.lock').open('w')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    try:
        asyncio.run(supervise(json.loads(config_path.read_text()), log_dir))
    except Exception:
        logger(log_dir, 'fatal').exception('Supervisor failed')
        sys.exit(1)
