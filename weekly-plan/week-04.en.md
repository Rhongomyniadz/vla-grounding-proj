# Week 4: Experiment manifests, reliable execution, and resumption

[English](week-04.en.md) | [简体中文](week-04.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Documentation:** Update the [bilingual code guide](../doc/CODE_GUIDE.en.md) with this week's design rationale, implemented structures and verification evidence.

**Goal:** Turn individual rollouts into explicit, resumable experiments without losing the controls you established.

**Start authoring when:** The Week 3 state/reset contract is specified; schemas, case construction and runner code can be authored while reset checks are pending.

**Run-computer prerequisite:** Week 3 provides verified state restoration and an explicit main-study execution horizon.

Planning estimate: 12 active hours across five sessions, including evidence review and documentation. GPU runtime is additional and must be measured.

## Execution locations

Use the [shared handoff procedure](../doc/ENVIRONMENT.en.md#handoff-for-every-execution-visit); the session locations below govern the detailed steps.

1. **Prepare on the coding computer:** Write your case builder, structured manifest validation, stable identities, source-snapshot provenance, run-relative artifact references and resume logic.
2. **Execute on the run computer:** After the Week 3 target gate, resolve the pinned task/state catalog and execute the eight-case interrupt/resume, timeout and genuine-error checks.
3. **Return for review:** Return task/state hashes, resolved manifests, source/lock/config identities, eight-case results and artifacts, error logs and before/after resume coverage.

Without target access, keep real-run checks pending, record the specific access or setup blocker, prepare the exact handoff and continue authoring that does not depend on target evidence.

## What to read and understand

Read in this order. Pending source is listed explicitly. Before completing this milestone, replace planned-code descriptions with exact implemented file/symbol links and add the relevant evidence reference.

| Order | Required reading |
| --- | --- |
| 1. Documents | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md#architecture-and-interfaces): record contracts and error/resume behavior; baseline/language sections for task/state identities. [Code guide](../doc/CODE_GUIDE.en.md): records, evidence and planned runner. |
| 2. Current code | [config.py](../src/vla_grounding/config.py): strict required-record validation; [evidence.py](../src/vla_grounding/evidence.py): `write_report` exclusive creation. |
| 3. Follow the calls | [tests/smoke_authoring.py](../tests/smoke_authoring.py): `check_cli_round_trip` / `check_rejected_configuration`; connect evidence-preservation checks to runner requirements. |
| 4. Milestone code/evidence | Task/state catalog, case builder, manifest/result schemas, ID derivation and runner/resume functions: planned; read every corresponding implemented module and CLI. |

Understanding goals:

- Distinguish physical scenario identity, paired sampling seed, policy/condition episode identity and whole-run specification identity.
- Trace one manifest row to its state, instruction, result and video; explain coverage using the eight-case panel.
- Explain why partial writes/exceptions are unfinished, why timeouts count as outcomes and why changed settings cannot resume under the same identity.

## Prepare and learn

- Read the implementation plan's experiment, episode, result, and run-manifest interfaces.
- Learn the difference between a scenario identity shared across policies and an episode identity that includes a particular policy and condition.
- Inspect the four primary task definitions and how the pinned benchmark resolves their names, objects, and IDs.

## Reading route and expected understanding

- Use the [architecture and record contracts](../doc/IMPLEMENTATION_PLAN.en.md#architecture-and-interfaces) as the required information checklist; do not invent a second incompatible schema in this weekly guide.
- Use the [task and evaluation protocol](../doc/IMPLEMENTATION_PLAN.en.md#3-experimental-protocol) to locate the four exact task names and the required development/final split.
- Read the pinned environment's reset path and your existing episode loop together. Identify where an explicit case must override an automatically advancing state index.

## Implementation tasks

The items below define the code and documentation deliverables for this week. Existing source should be completed or extended; future components remain planned until implemented. Keep experimental parameters authoritative in the linked implementation plan.

1. **Task/state catalog.** Implement catalog construction that resolves the protocol's full task names against the pinned benchmark, validates original/alternative objects and goal regions, and records actual runtime IDs. Resolve and hash explicit initial states, then reserve disjoint development/final groups according to the authoritative protocol.
2. **Manifest models and case construction.** Implement validated experiment, episode, result and run-manifest records with all reconstruction fields required. Build canonical development cases as pure functions of explicit task/state/policy/seed inputs. Reject missing references, duplicate cases and incompatible mappings before creating simulations.
3. **Stable identities and provenance.** Derive scenario identities from physical scene/control inputs and episode identities from the scenario plus policy/condition. Preserve source-snapshot, lock/config and model/data/asset identities in the resolved run manifest. Store portable references separately from local paths and use run-relative artifact links.
4. **Manifest execution.** Add a manifest-driven command that calls the verified single-episode loop, reports structured progress with `tqdm`, and writes one typed result and artifact set per intended case. Keep timeouts as completed unsuccessful episodes; stop with contextual errors when infrastructure execution is invalid.
5. **Correct resumption and coverage.** Resume only unfinished episodes under an unchanged meaningful specification. Distinguish incomplete/partial artifacts from valid completed records, reject conflicting run identities, and prevent duplicate results. Calculate planned, completed, unsuccessful and unfinished coverage from episode IDs rather than directory order.
6. **Real panel and documentation.** Execute the planned small canonical panel, interrupt between completed episodes and resume it. Verify exactly-once coverage, genuine timeout/error handling and changed-specification rejection. Document schema relationships, ID derivation, completion decisions, path resolution and a manifest-row-to-video example in the code guide.

## Work sessions

### 1. Freeze task and initial-state identities (2 hours)

**Location:** Coding computer: design the catalog and pairing fields. Run computer: resolve actual task IDs, object/region definitions and state hashes before freezing.

**Detailed procedure**

1. Resolve every primary task by its full name and inspect its task definition. Record the runtime ID as metadata, not as the only long-term identifier.

2. List available initial-state references and choose disjoint development and final groups according to the plan. Verify their counts and fingerprints before generating cases.

3. For each physical scene, verify the original object, alternative object, and basket goal region exist. Do not infer object presence from a natural-language task title.

4. Write a conceptual case table with task name, state reference, instruction identity, policy identity, and sampling seed. Mark which columns must remain shared in paired comparisons.

**Expected output:** A reviewed task/state catalog and a clear distinction between scene identity and run identity.

**If this does not work:** If runtime task ordering differs from your expectations, resolve names against the installed suite rather than hardcoding another index.

**Session completion checklist**

- [ ] resolve the four primary tasks by full name and verify their original/alternative objects and basket goal regions.
- [ ] Reserve five development and twenty distinct final initial states per task; save explicit references and hashes.
- [ ] specify paired sampling seeds so the same state uses the same policy RNG seed across instruction conditions and policies.

### 2. Build the first manifest and validation (3 hours)

**Location:** Coding computer: implement the case builder and validation. Check real reference resolution on the target once its catalog exists.

**Detailed procedure**

1. Implement the case-construction function, starting with one canonical case per selected development state and explicit immutable inputs.

2. Serialize and validate the required records from the architecture. Require identifiers and settings needed for reconstruction; ignore only unrelated external fields.

3. Design scenario identity around the physical task/state and pair-control information; include policy and condition in individual episode identity so distinct outputs cannot overwrite one another.

4. Inspect malformed and duplicate inputs before simulator creation. Verify missing fields, nonexistent state references, or incompatible mappings produce actionable errors.

**Expected output:** A manifest whose rows have reproducible identities and cannot silently refer to a different scene or policy.

**If this does not work:** Do not solve an invalid manifest by accepting an empty task list, substituting a default state, or dropping an unknown condition.

**Session completion checklist**

- [ ] implement the first case-construction function for canonical development cases using the frozen task/state list.
- [ ] implement structured configuration validation, stable episode IDs, resolved artifact metadata, and explicit command inputs.
- [ ] Validate required fields, malformed state references, incompatible feature mappings, and duplicate case identities before allocating simulation resources.

### 3. Execute and resume a small real panel (3 hours)

**Location:** Run computer: execute, interrupt and resume the eight-case panel and distinguish timeout from infrastructure failure.

**Detailed procedure**

1. Generate the planned eight-case canonical development panel, print its resolved cases, and check every task/state association before execution.

2. Run part of the panel, interrupt between completed episodes, and resume without editing the manifest. Compare completed IDs before and after.

3. Verify output writing distinguishes a complete episode from a partially written artifact. A partial record must not make resume skip an unfinished case.

4. Use a separately labeled short-limit development run for timeout behavior, and a genuinely invalid configuration for error behavior. Confirm only the former is a completed failed episode.

**Expected output:** An eight-case panel with one result per intended case and evidence that resume preserves correctness.

**If this does not work:** If results duplicate or disappear, fix episode identity and completion bookkeeping before running more cases.

**Session completion checklist**

- [ ] Run two development states for each primary task, producing eight canonical episodes with complete records.
- [ ] Interrupt the development run between completed episodes, resume the same manifest, and verify each case appears exactly once.
- [ ] Exercise a short development timeout and a genuine configuration error separately; distinguish an unsuccessful episode from an incomplete run.

### 4. Audit case construction and document the findings (2 hours)

**Location:** Coding computer: audit returned manifest/result lineage and count coverage by hand.

**Detailed procedure**

1. Select one manifest row. Find its task definition, serialized initial state, exact instruction, policy seed, and output record.

2. Reconstruct why its ID differs from a second policy/condition case while its paired physical-state identity remains the same.

3. Use a real record to calculate the expected coverage table by hand. Count planned, complete, failed-task, and unfinished cases separately.

4. Review the evidence and strongest alternative explanation, correct any identified root cause, rerun affected checks and document the reasoning in the relevant bilingual `doc/` pair.

**Expected output:** A hand-verified lineage from one manifest row to output and coverage.

**If this does not work:** If you can only identify a video by directory order, add the missing case-to-artifact reference.

**Session completion checklist**

- [ ] trace a manifest row through task resolution, state restoration, policy seed, output identity, and summary inclusion.
- [ ] Use real episode records to verify that instruction/policy identity can change while matched starting-state and sampling-seed identities remain fixed.
- [ ] verify the reasoning and any correction, rerun affected checks, and update the bilingual design/code explanations with evidence references.

### 5. Freeze the runner contract and hand off (2 hours)

**Location:** Coding computer: finalize the contract and review coverage. Run computer: verify changed-specification rejection before any resume.

**Detailed procedure**

1. Attempt to resume with a changed meaningful setting in a development check. Require a clear configuration-identity error or a new explicit run identity.

2. Save the validated manifest and resolved environment/model metadata alongside the eight-case results.

3. Document the runner contract in docstrings and explain its structure and rationale in the code guide. Update both architecture versions only if the actual contract changes.

4. Prepare an extension point for explicit instruction/goal cases next week without implementing speculative task modes.

**Expected output:** A runner that resumes the same experiment and keeps different experiments distinct.

**If this does not work:** Do not let current environment variables silently redefine the conditions of an existing manifest.

**Session completion checklist**

- [ ] Confirm configuration changes require a new manifest/run identity and cannot silently alter an existing resumed experiment.
- [ ] Save the eight-case development panel, manifest, trajectory references, videos, and a coverage summary.
- [ ] Prepare Week 5's language-case requirements without running the final held-out panel.

## Evidence and completion checks

- [ ] Documentation ready: the paired design/code guide covers all implemented structures, rationale, interfaces and verification status.
- [ ] Authoring ready: this week's source/configuration and applicable local checks are included in the identified handoff.
- [ ] Target verified: the required real target evidence has returned and been reviewed against that handoff.
- [ ] The four tasks and disjoint development/final state references are explicit and recoverable.
- [ ] Eight real development cases can be interrupted and resumed without missing or duplicate completed records.
- [ ] Errors retain actionable context, timeouts remain valid failures, and final-evaluation states have not been used for tuning.

## Optional review questions

1. Which identifiers must be shared for paired comparisons, and which must distinguish individual runs?
2. Why should an exception not be silently counted as an ordinary failed manipulation?
3. What must happen if a rendering, preprocessing, or policy setting changes before resuming a run?

## Delivery summary

> Implement case construction, manifest validation, artifact handling and resume support; verify the real eight-case panel and document identity, lineage and error handling.

## Ready for the next week

Independent authoring for later milestones may continue from agreed interfaces. The following gate applies to dependent execution and result claims.

Proceed when execution is explicit and resumable, and the code guide traces a manifest case through its recorded result.

