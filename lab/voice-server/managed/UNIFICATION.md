# Pocket service candidate

The service is Pocket. Alfred is one voice among its available profiles, for both REST
speech and realtime conversations. It is not promoted.

## Architecture

The authenticated gateway owns reservations. A private, loopback-only speech
router sends synthesis requests to Pocket with the requested voice profile. Both the REST
API and speech-to-speech's existing OpenAI HTTP adapters use that router.
The realtime process no longer loads separate inference model copies.

- Alfred / Ralph profile: existing Pocket TTS worker, PCM/WAV, unchanged profile.
- Synthesis: Pocket TTS with the available voice profiles.
- Transcription: one Parakeet worker in the existing audio process.
- Conversation text generation: existing dedicated Ollama service child.

There is one synthesis engine, one service lifecycle, reservation policy,
catalogue, backup and service registry record named Pocket. Alfred is its default voice. The catalogue is discovered from Pocket’s profile API, not an Alfred-only list.
Parakeet performs transcription only, via a worker that exposes no synthesis
or model-loading endpoints.

Alfred is the default for new requests that omit a voice. `voice: alfred` no longer requires the
caller to know the Pocket model name. `model: pocket-tts` stays compatible.

## Candidate execution

The disposable VM has its own code, Python environment, credentials and API.
During live tests it may use registered shared inference through loopback SSH
forwards while a production voice reservation is held. Do not bypass another
caller's reservation. Unit tests do not establish audio quality or realtime
correctness. Record real PCM, transcription, realtime turn and cancellation
results before requesting promotion.

## Promotion (only after explicit candidate approval)

1. Preserve source, test evidence, old configuration/releases and the Alfred
   profile through the central Google Drive backup. Verify the profile hashes.
2. Wait for or arrange release of active voice reservations; do not terminate a
   caller to install. Run the candidate installer with `--unified --pocket-home`
   pointing to the existing native Alfred runtime.
3. The shared supervisor takes ownership of the Pocket child; the legacy Alfred
   LaunchAgent is unloaded and disabled so it cannot start a second worker.
   Keep the existing unquantized float32 runtime, two CPU threads and profiles.
4. Verify REST Alfred, PCM/WAV, transcription, realtime Alfred, cancellation,
   authentication, lease cleanup and supervisor recovery on the actual Mac.
5. Record engine topology under the Pocket service record, remove the Alfred service dependency,
   retire the separate `alfred-voice` service only after functional verification,
   and preserve the existing combined voice backup coverage.
6. Delete the disposable candidate VM, its disks, test keys and relay routes
   after production verification and external evidence/recovery preservation.

Rollback: stop the candidate supervisor, restore the prior configuration and
versioned release, re-enable/bootstrap the prior Alfred LaunchAgent and shared
voice LaunchAgent, then verify both endpoints and reservation cleanup. Do not
remove Pocket models or profiles during either direction of the transition.

Mac launchd cutover must be verified on the Mac after approval. Linux staging
cannot establish macOS launchd or Apple MLX startup correctness.
