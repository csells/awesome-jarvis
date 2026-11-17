# Memory, perception and household context

## Separate stores by purpose

Distinguish live session state, conversation history, working context, durable user facts/preferences, task receipts, retrieved documents, sensor events and audit logs. Each needs an owner, provenance, retention and deletion policy. A long chat window is not durable memory, and an embedding index is not authoritative structured state.

Choose the simplest storage that meets the required retrieval and consistency. Files plus a small structured store may suffice; a graph/vector system earns its cost when relationships or semantic retrieval are actually needed. Keep raw source, derived summary and current fact distinguishable. Use timestamps, speaker/account scope, confidence and supersession links; contradictions should not silently overwrite a trusted preference.

## Consent and data flow

Record what is captured, where it is processed, what is saved, who can retrieve it, and how it expires. Audit audio, transcripts, images, screen context, clipboard, location, embeddings, cloud memory extraction and backups separately. An otherwise local configuration may still invoke remote summarization or telemetry using a configured cloud key.

Default to task-appropriate capture and explicit retention choices. Support remembering a selected fact without retaining every recording. Provide review, correction, export and forget controls. Deleting a chat should have defined consequences for extracted memories, embeddings, caches and backups; distinguish logical deletion, retention expiration and physical erasure.

Shared spaces need person and household boundaries. A visitor's utterance must not become a durable private fact about the owner. Identify which facts are household-visible and which are personal. Handle uncertain identity by narrowing disclosure and authority. Test cross-user retrieval rather than assuming a user ID column provides isolation.

## Retrieval correctness

Preserve source attribution and freshness. Filter retrieval by identity, task and consent before supplying model context. Treat retrieved text as untrusted data; embedded “approve this action” instructions cannot modify policy. Show uncertainty when memory is stale, contradictory or missing. Consider prompt-injection and secret leakage from files, websites, calendar events and worker summaries.

Test add/recall after a real process restart, update/supersede, deletion, namespace isolation, unavailable store, corrupted/partial write and a malicious retrieved instruction. Check actual stored artifacts and outbound processing, not only what the assistant claims it remembered. Have a recoverable backup/restore story for durable user data.

## Vision and sensors

Treat cameras, screen capture, occupancy, Bluetooth presence and location as separate capabilities requiring permission, freshness and purpose. A sensor event can suggest context without proving a person's identity or intent. Screenshots may include secrets and unrelated people; redact before publication and scope ingestion to the user-approved surface.

Define sampling rate, wake/capture trigger, privacy mask, event retention, bystander behavior and what occurs when sensors are stale/offline. Test denied/revoked permissions, device removal, an occluded camera and stale presence. Pair the intended visible state with actual capture activity. Pause indicators should reflect all active inputs, not only the conversation microphone.

Physical glasses or device SDKs can require signing, registration, native permissions and specific hardware. A simulator launch or unsigned build does not establish these paths. Preserve device-only value separately from optional glasses/camera features so one unavailable accessory does not falsely invalidate or qualify the whole product.
