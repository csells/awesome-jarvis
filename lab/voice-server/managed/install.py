"""Install a versioned, user-owned launchd voice service using already pinned local runtimes."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import plistlib
import secrets
import shutil
import subprocess
import time

LABEL = 'com.jarvislab.voice-service'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--home', type=Path, default=Path.home()/'Library/Application Support/JarvisVoice')
    p.add_argument('--ollama', default='/usr/local/bin/ollama')
    p.add_argument('--models', type=Path, default=Path.home()/'.ollama/models')
    p.add_argument('--pocket-url', help='Private Pocket backend URL, e.g. http://127.0.0.1:18769; adds REST speech streaming')
    p.add_argument('--unified', action='store_true', default=True, help=argparse.SUPPRESS)
    p.add_argument('--pocket-home', type=Path, help='Existing native Pocket runtime, supervised by this service')
    args = p.parse_args()
    if args.unified and not args.pocket_home:
        p.error('--unified requires --pocket-home')
    os.umask(0o077)
    home = args.home.resolve()
    runtime = home/'runtime'
    for name in ('s2s-venv', 'mlx-audio-venv', 'hf'):
        if not (runtime/name).exists():
            raise SystemExit(f'Missing cached runtime: {runtime/name}')
    source = Path(__file__).resolve().parent.parent
    release = home/'releases'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    release.mkdir(parents=True)
    shutil.copytree(source/'managed', release/'managed', ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copytree(source/'bin', release/'bin', ignore=shutil.ignore_patterns('__pycache__'))
    manifest = {}
    for name in ('requirements-audio.lock.txt', 'requirements-realtime.lock.txt'):
        shutil.copyfile(source/name, release/name)
        manifest[name] = hashlib.sha256((source/name).read_bytes()).hexdigest()
    (release/'pins.json').write_text(json.dumps(manifest, indent=2))
    key = home/'admin.key'
    if not key.exists():
        key.write_text(secrets.token_urlsafe(48)+'\n')
    key.chmod(0o600)
    ffmpeg = runtime/'mlx-audio-venv/bin/python'
    executable = subprocess.check_output([str(ffmpeg), '-c', 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())'], text=True).strip()
    (home/'bin').mkdir(exist_ok=True)
    link = home/'bin/ffmpeg'
    if link.is_symlink():
        link.unlink()
    if not link.exists():
        link.symlink_to(executable)
    config_path = home/'config.json'
    model = 'qwen2.5:7b-instruct-q4_K_M'
    python = str(runtime/'s2s-venv/bin/python')
    environment = {'HF_HOME': str(runtime/'hf'), 'HF_HUB_OFFLINE': '1',
        'PATH': str(home/'bin')+':/usr/bin:/bin:/usr/sbin:/sbin', 'PYTHONUNBUFFERED': '1',
        'TOKENIZERS_PARALLELISM': 'false',
        'VOICE_SERVICE_CONFIG': str(config_path), 'VOICE_LLM_TIMEOUT': '90',
        'MLX_AUDIO_ALLOWED_ORIGINS': 'http://localhost'}
    config = {'admin_key_file': str(key), 'gateway_port': 18800,
        'realtime_url': 'http://127.0.0.1:18765', 'audio_url': 'http://127.0.0.1:18766',
        'ollama_url': 'http://127.0.0.1:18768', 'model': model,
        'working_directory': str(release), 'environment': environment,
        'processes': {
            'model': {'argv': [args.ollama, 'serve'], 'environment': {
                'OLLAMA_HOST': '127.0.0.1:18768', 'OLLAMA_MODELS': str(args.models),
                'OLLAMA_MAX_LOADED_MODELS': '1', 'OLLAMA_NUM_PARALLEL': '1', 'OLLAMA_KEEP_ALIVE': '15m'},
                'health_url': 'http://127.0.0.1:18768/api/tags'},
            'realtime': {'argv': [python, str(release/'bin/s2s_serve.py'), 'serve', '--host', '127.0.0.1', '--port', '18765',
                '--stt', 'openai', '--tts', 'openai',
                '--llm_backend', 'chat-completions', '--model_name', model,
                '--responses_api_base_url', 'http://127.0.0.1:18768/v1', '--responses_api_api_key', 'local',
                '--responses_api_stream', '--init_chat_prompt', 'You are a concise voice assistant. Answer briefly.'],
                'health_url': 'http://127.0.0.1:18765/v1/pool'},
            'audio': {'argv': [str(runtime/'mlx-audio-venv/bin/python'), str(release/'bin/audio_serve.py'), '--host', '127.0.0.1', '--port', '18766'],
                'health_url': 'http://127.0.0.1:18766/health'},
            'gateway': {'argv': [python, str(release/'managed/gateway.py')], 'health_url': 'http://127.0.0.1:18800/healthz'},
        }}
    if args.pocket_url:
        from urllib.parse import urlsplit
        url = urlsplit(args.pocket_url)
        if url.scheme not in ('http', 'https') or not url.hostname or url.username or url.password:
            raise SystemExit('Pocket URL must be a credential-free HTTP(S) service URL.')
        config['pocket_url'] = args.pocket_url.rstrip('/')
    if args.unified:
        from unified_config import unify
        pocket_home = args.pocket_home.resolve()
        pocket_python = pocket_home/'.venv/bin/python'
        if not pocket_python.is_file() or not (pocket_home/'app.py').is_file():
            raise SystemExit('Pocket runtime is incomplete; installation unchanged.')
        config['pocket_url'] = 'http://127.0.0.1:51998'
        pocket_process = {'argv': [str(pocket_python), '-m', 'uvicorn', 'app:app',
            '--app-dir', str(pocket_home), '--host', '127.0.0.1', '--port', '51998',
            '--no-access-log', '--ws-max-size', '16384'],
            'environment': {'HEALTH_PORT':'18771','OMP_NUM_THREADS':'2','POCKET_THREADS':'2','POCKET_QUANTIZE':'0','HF_HUB_OFFLINE':'1','PATH':'/opt/homebrew/bin:/usr/bin:/bin'},
            'health_url':'http://127.0.0.1:51998/healthz'}
        config = unify(config, release, python, pocket_process)
    # A second independent model process avoids owning or restarting the host's existing Ollama.
    config_path.write_text(json.dumps(config, indent=2))
    current = home/'current'
    tmp = home/'current.next'
    tmp.unlink(missing_ok=True)
    tmp.symlink_to(release, target_is_directory=True)
    tmp.replace(current)
    plist = {'Label': LABEL, 'ProgramArguments': [python, str(current/'managed/supervisor.py'), str(config_path)],
        'RunAtLoad': True, 'KeepAlive': True, 'ThrottleInterval': 10, 'ExitTimeOut': 30,
        'ProcessType': 'Interactive', 'WorkingDirectory': str(home), 'Umask': 0o077,
        'StandardOutPath': '/dev/null', 'StandardErrorPath': '/dev/null'}
    destination = Path.home()/'Library/LaunchAgents'/(LABEL+'.plist')
    destination.parent.mkdir(exist_ok=True)
    with destination.open('wb') as f:
        plistlib.dump(plist, f)
    domain = f'gui/{os.getuid()}'
    target = domain+'/'+LABEL
    present = subprocess.run(['launchctl', 'print', target], capture_output=True).returncode == 0
    if present:
        subprocess.run(['launchctl', 'bootout', target], check=True)
        # bootout returns while the old process group may still be exiting.
        for _ in range(45):
            if subprocess.run(['launchctl', 'print', target], capture_output=True).returncode != 0:
                break
            time.sleep(1)
        else:
            raise SystemExit('Previous service did not unload within 45 seconds.')
    if args.unified:
        legacy = domain+'/com.jarvislab.alfred-local'
        if subprocess.run(['launchctl','print',legacy],capture_output=True).returncode == 0:
            subprocess.run(['launchctl','bootout',legacy],check=True)
        # Disable the old job so only the shared supervisor owns Pocket after login.
        subprocess.run(['launchctl','disable',legacy],check=True)
    for attempt in range(10):
        loaded = subprocess.run(['launchctl', 'bootstrap', domain, str(destination)], capture_output=True, text=True)
        if loaded.returncode == 0:
            break
        if attempt == 9:
            raise SystemExit('launchd bootstrap failed: '+loaded.stderr.strip())
        time.sleep(1)
    print(json.dumps({'service': LABEL, 'release': str(release), 'config': str(config_path),
                      'credential_file': str(key), 'startup': 'at user login', 'log_directory': str(home/'logs')}, indent=2))


if __name__ == '__main__':
    main()
