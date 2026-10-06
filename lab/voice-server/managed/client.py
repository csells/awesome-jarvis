"""Reserve a shared voice session; write credentials to a private file, never stdout."""
import argparse
import json
import os
from pathlib import Path
import urllib.error
import urllib.request


def request(base, path, token, method='GET', body=None):
    headers = {'Authorization': 'Bearer '+token}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(base.rstrip('/')+path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.load(response)
    except urllib.error.HTTPError as error:
        raise SystemExit(f'Voice service returned HTTP {error.code}: {error.read().decode()}')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--home', type=Path, default=Path.home()/'Library/Application Support/JarvisVoice')
    p.add_argument('--base', help='Override service URL; renew/release otherwise use the session file URL')
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('status')
    acquire = sub.add_parser('reserve')
    acquire.add_argument('--owner', required=True)
    acquire.add_argument('--ttl', type=int, default=900)
    acquire.add_argument('--out', type=Path, required=True)
    for name in ('renew', 'release'):
        command = sub.add_parser(name)
        command.add_argument('--session', type=Path, required=True)
        if name == 'renew':
            command.add_argument('--ttl', type=int, default=900)
    sub.add_parser('force-release')
    args = p.parse_args()
    if args.command in ('status', 'reserve', 'force-release'):
        token = (args.home/'admin.key').read_text().strip()
        args.base = args.base or 'http://127.0.0.1:18800'
    else:
        session = json.loads(args.session.read_text())
        token = session['api_key']
        args.base = args.base or session['base_url']
    if args.command == 'status':
        result = request(args.base, '/status', token)
    elif args.command == 'reserve':
        # Exclusive creation before reserving prevents losing an issued key to a path error.
        fd = os.open(args.out, os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600)
        try:
            result = request(args.base, '/leases', token, 'POST', {'owner': args.owner, 'ttl_seconds': args.ttl})
            with os.fdopen(fd, 'w') as output:
                fd = None
                json.dump({**result, 'base_url': args.base}, output, indent=2)
            result = {k:v for k,v in result.items() if k != 'api_key'}
            result['credential_file'] = str(args.out)
        except BaseException:
            if fd is not None:
                os.close(fd)
            args.out.unlink(missing_ok=True)
            raise
    elif args.command == 'renew':
        result = request(args.base, '/leases/current/renew', token, 'POST', {'ttl_seconds': args.ttl})
    else:
        result = request(args.base, '/leases/current', token, 'DELETE')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
