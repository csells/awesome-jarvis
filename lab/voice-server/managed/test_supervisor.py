import unittest
from unittest.mock import patch
from supervisor import process_identity, matches_process


class OwnershipTests(unittest.TestCase):
    def test_python_launcher_exec_does_not_hide_owned_process(self):
        started = 'Mon Oct 5 18:50:00 2026'
        script = '/service/releases/one/bin/s2s_serve.py'
        with patch('supervisor.process_details', return_value=(started, '/venv/python '+script)):
            identity = process_identity(123, ['/venv/python', script, 'serve'])
        with patch('supervisor.process_details', return_value=(started, '/Python.app/Python '+script+' serve')):
            self.assertTrue(matches_process(123, identity))
        with patch('supervisor.process_details', return_value=('Mon Oct 5 18:51:00 2026', '/Python.app/Python '+script)):
            self.assertFalse(matches_process(123, identity))
        with patch('supervisor.process_details', return_value=(started, '/unrelated.py')):
            self.assertFalse(matches_process(123, identity))


if __name__ == '__main__':
    unittest.main()
