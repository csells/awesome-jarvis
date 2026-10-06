import asyncio
import json
from pathlib import Path
import sys
import unittest
from types import SimpleNamespace
sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'bin'))
from speech_to_speech.api.openai_realtime.webrtc_session import WebRTCSession

from playback_events import install
install(WebRTCSession)

class Event:
    def __init__(self, value): self.value = value
    def model_dump(self): return self.value

class PlaybackTests(unittest.IsolatedAsyncioTestCase):
    async def test_stopped_waits_for_actual_track_drain_and_clear_is_signaled(self):
        events = []
        session = WebRTCSession(None, on_client_event=None, on_audio=None, on_open=None, on_closed=None)
        session._dc = SimpleNamespace(readyState='open', send=lambda s: events.append(json.loads(s)))
        async def send(value): await session.send_events([Event(value)])
        await send({'type': 'response.created', 'response': {'id': 'r1'}})
        session._track.write(b'\x01\x00'*1920)
        await send({'type': 'response.done', 'response': {'id': 'r1'}})
        self.assertNotIn('output_audio_buffer.stopped', [e['type'] for e in events])
        await session._track.recv()
        self.assertNotIn('output_audio_buffer.stopped', [e['type'] for e in events])
        await session._track.recv()
        self.assertEqual([e['type'] for e in events].count('output_audio_buffer.started'), 1)
        self.assertEqual([e['type'] for e in events].count('output_audio_buffer.stopped'), 1)
        await send({'type': 'response.created', 'response': {'id': 'r2'}})
        session._track.write(b'\x01\x00'*1920)
        session.discard_pending_audio()
        self.assertEqual(session._track.buffered_bytes, 0)
        self.assertEqual([e['type'] for e in events][-2:], ['output_audio_buffer.cleared', 'output_audio_buffer.stopped'])
        self.assertEqual(events[-1]['response_id'], 'r2')

    async def test_next_generation_does_not_hide_previous_playback_completion(self):
        events = []
        session = WebRTCSession(None, on_client_event=None, on_audio=None, on_open=None, on_closed=None)
        session._dc = SimpleNamespace(readyState='open', send=lambda s: events.append(json.loads(s)))
        async def send(kind, ident): await session.send_events([Event({'type': kind, 'response': {'id': ident}})])
        await send('response.created', 'first')
        session._track.write(b'\x01\x00'*960)
        await send('response.done', 'first')
        await send('response.created', 'second')
        await session._track.recv()
        self.assertEqual(events[-1]['type'], 'output_audio_buffer.stopped')
        self.assertEqual(events[-1]['response_id'], 'first')
        session._track.write(b'\x01\x00'*960)
        await send('response.done', 'second')
        await session._track.recv()
        self.assertEqual(events[-1]['response_id'], 'second')
