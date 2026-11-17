# Jarvis building skills

[build-jarvis](build-jarvis/SKILL.md) turns the catalog, blueprint and lab findings into a workflow for choosing, building, testing and operating a personal voice agent. It covers complete agents and components, local and cloud deployments, household and desktop use, and production acceptance.

Start with:

> Use the build-jarvis skill in skills/build-jarvis to help me build an assistant for my hardware and daily tasks.

Give the agent this folder, or install the complete `build-jarvis/` directory using your agent host's documented skill installation mechanism. Keep its `references/` and `assets/` siblings intact. The folder is self-contained; it links back to dated public repository evidence rather than requiring this checkout or Chris's lab. Host discovery and tool permissions vary; verify the skill is available in your agent's catalog.

The entrypoint routes to detailed references as needed. Read [the reference map](build-jarvis/SKILL.md#reference-map) to explore the full guide. Start a brief and test plan from the [templates](build-jarvis/assets/build-record.md). Existing lab findings are dated observations, not current installation guarantees.

This skill is guidance and reusable templates. It does not ship a running voice service, install global agent configuration, or enable tools merely by being loaded. It uses the user's existing environment, permissions, chosen providers and deployment policy.

The [live build evaluation](../specs/research/build-jarvis-live-evaluation.md) records a fresh implementation exercised through real voice, approvals, worker cancellation and restart, including the defects found and repaired. The earlier response scenarios are labelled as instruction smoke tests.
