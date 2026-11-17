# Deployment, operations and lifecycle

## Placement and real staging

Inventory existing machines, models, voice services, registries, leases, templates, capacity and recovery mechanisms through authorized normal interfaces. Reuse real dependencies rather than creating duplicates or synthetic replacements. A portable skill names required capabilities; machine names, IPs, credential references and administrative commands come from the current environment.

Place general Linux/server tests on suitable workers and native Apple/device jobs on compatible hardware. Verify live CPU/RAM/storage reservations, model footprint, host headroom and graphics/virtualization support before starting workloads. Queue work when capacity is unavailable. Cached inventory and a hypervisor API do not establish admission capacity or a working guest.

Service development follows the applicable isolated-candidate rule. Use a separate candidate VM/environment against real services and data through scoped identities; stable source/config/user data stay unchanged until authorized promotion. Installing/configuring a third-party service is a different operation and follows its authorized backup, migration and cutover plan. Writing operational configuration alone does not make it service-source development.

Record exact ownership, purpose, environment ID, resource limits, access references, expiry, artifact destination and cleanup procedure before long work. Do not encode one user's hostnames, subscription, no-Tailscale preference or personal credentials into this portable skill. Apply those constraints only when the current user/environment actually supplies them.

## Long-running work

Use native process/job/agent handles. Capture logs and measurable progress before launching long installs, model downloads, builds or batches. Report actual phases or completed/total work rather than invented percentages. Bound individual waits so the user can get status and steer the task. Keep long work alive through a task-owned process manager when shell lifetime or inherited background priority is inadequate.

Watch warnings as well as fatal errors: resource pressure, deprecated plugins, wrong engine versions, private-directory permissions and unavailable optional dependencies have different impact. Correct routine candidate setup within authority. Record unresolved actionable warnings with owner, reason, deadline and next check instead of suppressing them or inflating them into unrelated product failures.

## Promotion and production verification

Prepare source, configuration references, backup/restore, rollback artifacts, tested build identity and a staged review endpoint before requesting any required cutover approval. Present the actual candidate with its test coverage and limitations. Code passing tests, permission to develop and approval of a previous version do not substitute for the applicable promotion grant.

After promotion, verify the production endpoint and actual user flow: authentication, capture/reply, expected worker/action controls, persistence and recoverable restart according to the contract. Confirm native autostart, PATH, environment and permissions rather than relying on a development shell. Check recurring health delivery from its expected observer. A listening port alone is not functional verification.

For repository-only documentation/curation work, checks and published commit identity establish a different deliverable from service readiness. Verify remote branch/main state and CI coverage, distinguishing docs-only changes from the last tested implementation. A merged branch does not certify every third-party agent described by it.

## Backup, rollback and retention

Back up configuration and user data through the environment's approved service and destination. Preserve source/pins and evidence outside disposable storage. Verify restore/rollback for the changed surfaces before cutover; keeping an old VM disk is not itself a tested restore procedure. Avoid duplicating production data into evidence without a justified purpose and access policy.

Document rollback trigger, exact owner, last known good version/config and expected effects on tasks, credentials, histories and external actions. Some effects cannot be undone; reconcile their receipts instead of blindly replaying them. Test the relevant restart/reconnect policy before enabling unattended work.

## Cleanup verification

Use an ownership manifest and verify identity before deleting or stopping anything. Export evidence first. Remove candidate apps/jobs, worker descendants, browser contexts, virtual audio modules, temporary defaults, forwards, review URLs, copied/imported credentials, private profiles and unused reservations. Verify real absence, service lease release and shared-service health. Restore the original configuration state, including absence of files created only for an experiment.

Follow the actual retention policy. If promotion requires deleting dedicated staging VMs/disks, stopping them is insufficient. If a lab explicitly retains stopped test guests for reuse, keep them stopped with unnecessary credentials removed and a concrete owner/expiry. Preserve shared dependencies, templates, user work and unrelated environments. Record cleanup blockers with an owner and review date.

## Maintenance contract

Assign an operator and a place for current service identity, access references, dependencies, recovery, backups and dated checks. Review auth/lease expiry, certificate and model availability, disk/log growth, retained memory and failed/uncertain jobs. Monitor control-plane and real-path health separately.

Retest after major/minor application changes, model/provider/adapter updates, default approval policy changes, OS/audio route changes and migrations. Review security fixes promptly. Historical latency, voice and cancellation results do not transfer automatically to another provider/mode/version. The catalog's periodic reviews are useful triggers; the deployment's own required paths decide its acceptance.

Keep a small recurring real task that validates the intended chain safely, with no surprise phone call, message or physical actuation. Verify user-facing mute/stop/revoke remain accessible during outages. Maintenance should leave enough evidence to distinguish a vendor regression, expired credential, changed device permission, exhausted service capacity and a broken observer.
