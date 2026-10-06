"""Add WebRTC output-buffer events using RTP track drain, not LLM completion."""
from collections import deque
import json
from uuid import uuid4


def install(session_class):
    if getattr(session_class, '_lab_playback_events', False):
        return
    original_init = session_class.__init__
    original_send = session_class.send_events

    def initialize(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        state = {'generating': None, 'playing': None, 'done': set(), 'segments': deque()}
        self._lab_playback = state
        track = self._track
        write, recv, clear = track.write, track.recv, track.clear

        def emit(kind, response_id):
            if self._dc is not None and self._dc.readyState == 'open':
                self._dc.send(json.dumps({'type': 'output_audio_buffer.'+kind,
                    'event_id': 'evt_'+uuid4().hex, 'response_id': response_id}))

        def synchronize():
            segments, playing = state['segments'], state['playing']
            if playing is not None and not any(s[0] == playing for s in segments) and (
                    playing in state['done'] or segments):
                emit('stopped', playing)
                state['done'].discard(playing)
                state['playing'] = None
            if segments and state['playing'] is None:
                state['playing'] = segments[0][0]
                emit('started', state['playing'])

        self._lab_drained = synchronize

        def write_audio(pcm):
            write(pcm)
            if pcm:
                state['segments'].append([state['generating'], len(pcm)])
                synchronize()

        async def receive():
            frame = await recv()
            # The pinned track emits mono s16 frames, padding short payloads
            # with silence. Only queued PCM consumes response-owned bytes.
            remaining = frame.samples * 2
            while remaining and state['segments']:
                segment = state['segments'][0]
                count = min(remaining, segment[1])
                segment[1] -= count
                remaining -= count
                if not segment[1]:
                    state['segments'].popleft()
                synchronize()
            synchronize()
            return frame

        def clear_audio():
            clear()
            state['segments'].clear()
            playing = state['playing']
            if playing is not None:
                emit('cleared', playing)
                emit('stopped', playing)
                state['done'].discard(playing)
                state['playing'] = None

        track.write, track.recv, track.clear = write_audio, receive, clear_audio

    async def send(self, events):
        await original_send(self, events)
        for event in events:
            value = event.model_dump()
            if value['type'] == 'response.created':
                self._lab_playback['generating'] = value['response']['id']
            elif value['type'] == 'response.done':
                response_id = value['response']['id']
                state = self._lab_playback
                if state['playing'] == response_id or any(s[0] == response_id for s in state['segments']):
                    state['done'].add(response_id)
                self._lab_drained()

    session_class.__init__ = initialize
    session_class.send_events = send
    session_class._lab_playback_events = True
