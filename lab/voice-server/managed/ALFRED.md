# Alfred — a Pocket voice

Alfred uses the approved Ralph Fiennes Pocket TTS profile, encoded directly from the original actor reference. Personal use only, under the profile owner’s reported permission. The pinned model and reusable profile are installed locally; no Hugging Face inference service or per-request fee is involved.

## Use from an app

Discover service `voice` in the home-lab registry. Its authenticated HTTPS base URL is `https://voice.example.internal`. Reach it from the tailnet. Obtain a short-lived session key using the service's existing reservation flow; do not embed the administrator key in apps. Only one reservation is admitted; renew for longer sessions and release when finished.

On the service host, the existing helper can issue a key into a private file:

```sh
python3 "$HOME/Library/Application Support/JarvisVoice/current/managed/client.py" \
  --base https://voice.example.internal \
  reserve --owner YOUR_APP --ttl 900 --out /private/tmp/YOUR_APP-voice-session.json
```

Send the session key as `Authorization: Bearer SESSION_KEY` to `POST /v1/audio/speech`:

```json
{
  "model": "pocket-tts",
  "voice": "alfred",
  "input": "Good evening. Alfred is ready to help.",
  "speed": 1.25,
  "response_format": "pcm"
}
```

`pcm` streams signed 16-bit little-endian mono audio at 24,000 Hz. Read the response incrementally; play through a continuous buffer. `X-Sample-Rate`, `X-Audio-Channels` and `X-Audio-Format` describe it. `wav` instead waits for the complete file. Limits: 1–2000 nonblank input characters, speed0.5–2.0. Omitted speed defaults to1.25 with pitch preservation. Closing the stream cancels generation. `GET /v1/voices`, with the same session key, advertises Alfred and its parameters.

Release the reservation with `DELETE /leases/current`, or the helper's `release --session FILE` command. Delete the session file afterward. Missing/expired credentials return401, busy backends409, invalid input422. A running realtime conversation occupies the same shared reservation; stop it before requesting standalone speech.

In the unified candidate, Alfred is selected by voice name in REST requests and
realtime sessions. New requests default to Alfred; other Pocket profiles are selectable by voice ID. The realtime process uses the shared speech workers instead of
loading duplicate transcription and synthesis models. See [UNIFICATION.md](UNIFICATION.md)
for the architecture, validation and promotion checklist. The candidate has not
replaced production yet.

## Profile and operation

The approved Ralph Fiennes conditioning profile remains private and unchanged.
Do not publish reference recordings or profiles. Production currently runs natively
on the service host; Discover current
addresses, installation, versions and backup evidence from the registry.

The unified candidate places Pocket under the shared voice supervisor. It disables
the separate Alfred LaunchAgent only during explicitly approved promotion. Pocket is the only synthesis engine. Parakeet transcription is loaded
once by the audio worker and shared with realtime.

## Recovery and validation

The registered central voice backup plan covers both the shared service and
Alfred's model, profiles, source and configuration in encrypted Google Drive
snapshots. Discover current snapshot and restore evidence in the registry; do not
create additional retained repositories. Preserve source, evidence and recovery
artifacts before promoting and deleting staging.

Use the shared reservation contract for all callers. Validate PCM/WAV, transcription, an actual Alfred realtime turn, cancellation and
interruption before promotion. Mac launchd ownership transfer and post-login
startup must additionally be checked on the destination after approved cutover.
