# Build Jarvis skill

Create a portable, comprehensive skill under `skills/build-jarvis/` on `review/build-jarvis-skill`, based on published `main` at 284874b. This task authors guidance and templates; it does not install an assistant, modify stable services or publish to main.

## Scope

- Focused discovery and executable lifecycle in SKILL.md; exhaustive domain references loaded by task.
- Requirements/selection, architecture, protocol/provider contracts, implementation, acoustic voice, worker authority/cancellation, memory/context, UI/proactivity, acceptance, diagnosis, privacy/security and operations.
- Dated project evidence with exact provenance; portable environment discovery replaces personal hostnames/credentials.
- Templates for build contract, acceptance matrix and operational handover.
- Skill folder usable outside the full repository, with public evidence links as optional deeper sources.

## Verification

1. Validate skill frontmatter and names, all reference/template paths and portable scope.
2. Inspect source coverage against blueprint, methodology, testing history and November cases.
3. Forward-test isolated realistic planning/diagnostic prompts against a no-skill baseline; include task limits and unrelated-request routing. Skill-creator explicitly requires fresh-context evaluation. Evaluation agents may read/write private test artifacts only, with no network, installation, calls, credentials or lab changes.
4. Inspect actual outputs and reference use; correct demonstrated failures. Preserve unexecuted live assistant tests as outside this authoring task.
5. Run relevant repository lint/link checks and report validation limits. Keep work on the new branch.

Expected behavioral cases: local-only/limited-hardware design respects resources and verifies protocol feasibility; a Stop badge with a growing worker heartbeat is classified as failed cancellation with exact cleanup; background phone failure stays a scoped transport issue, with no automatic calls or invented root cause. A generic chatbot question should not trigger a full Jarvis build workflow.

Status: complete. See [validation results](../../research/build-jarvis-skill-evaluation.md). This archived plan preserves the intended scope; no live assistant installation or production promotion was part of this authoring task.
