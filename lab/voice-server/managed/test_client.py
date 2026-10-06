import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import client


class ClientTests(unittest.TestCase):
    def test_session_commands_use_saved_endpoint_and_explicit_override(self):
        with tempfile.TemporaryDirectory() as directory:
            session = Path(directory)/'session.json'
            session.write_text(json.dumps({'api_key':'test-lease', 'base_url':'https://saved.example'}))
            for command in ('renew', 'release'):
                for override in ([], ['--base', 'https://override.example']):
                    with self.subTest(command=command, override=override):
                        argv = ['client.py', *override, command, '--session', str(session)]
                        with patch('sys.argv', argv), patch('client.request', return_value={}) as request, contextlib.redirect_stdout(io.StringIO()):
                            client.main()
                        self.assertEqual(request.call_args.args[0], 'https://override.example' if override else 'https://saved.example')
                        self.assertEqual(request.call_args.args[2], 'test-lease')


if __name__ == '__main__':
    unittest.main()
