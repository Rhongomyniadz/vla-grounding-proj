# Week 4: Experiment manifests, reliable execution, and resumption

[English](week-04.en.md) | [简体中文](week-04.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Goal:** Turn individual rollouts into explicit, resumable experiments without losing the controls you established.

**Start when:** Week 3 provides verified state restoration and an explicit main-study execution horizon.

Time budget: 12 active hours across five sessions; one hour is independent work with the agent closed. Computer runtime is additional.

## Prepare and learn

- Read the implementation plan's experiment, episode, result, and run-manifest interfaces.
- Learn the difference between a scenario identity shared across policies and an episode identity that includes a particular policy and condition.
- Inspect the four primary task definitions and how the pinned benchmark resolves their names, objects, and IDs.

## Work sessions

### 1. Freeze task and initial-state identities (2 hours)

- [ ] You: resolve the four primary tasks by full name and verify their original/alternative objects and basket goal regions.
- [ ] Reserve five development and twenty distinct final initial states per task; save explicit references and hashes.
- [ ] You: specify paired sampling seeds so the same state uses the same policy RNG seed across instruction conditions and policies.

### 2. Build the first manifest and validation (3 hours)

- [ ] You: implement the first case-construction function for canonical development cases using the frozen task/state list.
- [ ] Agent: implement structured configuration validation, stable episode IDs, resolved artifact metadata, and explicit command inputs.
- [ ] Validate required fields, malformed state references, incompatible feature mappings, and duplicate case identities before allocating simulation resources.

### 3. Execute and resume a small real panel (3 hours)

- [ ] Run two development states for each primary task, producing eight canonical episodes with complete records.
- [ ] Interrupt the development run between completed episodes, resume the same manifest, and verify each case appears exactly once.
- [ ] Exercise a short development timeout and a genuine configuration error separately; distinguish an unsuccessful episode from an incomplete run.

### 4. Audit case construction independently, then review (2 hours)

- [ ] For the first hour, close the agent and trace a manifest row through task resolution, state restoration, policy seed, output identity, and summary inclusion.
- [ ] Use real episode records to verify that instruction/policy identity can change while matched starting-state and sampling-seed identities remain fixed.
- [ ] In the second hour, review your audit and case builder with the agent; correct any hidden settings or duplicate-ID behavior.

### 5. Freeze the runner contract and hand off (2 hours)

- [ ] Confirm configuration changes require a new manifest/run identity and cannot silently alter an existing resumed experiment.
- [ ] Save the eight-case development panel, manifest, trajectory references, videos, and a coverage summary.
- [ ] Prepare Week 5's language-case requirements without running the final held-out panel.

## Evidence and completion checks

- [ ] The four tasks and disjoint development/final state references are explicit and recoverable.
- [ ] Eight real development cases can be interrupted and resumed without missing or duplicate completed records.
- [ ] Errors retain actionable context, timeouts remain valid failures, and final-evaluation states have not been used for tuning.

## Explain without the agent

1. Which identifiers must be shared for paired comparisons, and which must distinguish individual runs?
2. Why should an exception not be silently counted as an ordinary failed manipulation?
3. What must happen if a rendering, preprocessing, or policy setting changes before resuming a run?

## Suggested request to the coding agent

> Implement manifest validation, artifact handling, and resume support around my case builder; verify behavior with the real eight-case development panel.

## Ready for the next week

Proceed when execution is explicit and resumable, and the learner can trace a manifest case through its recorded result.

