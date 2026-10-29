# Week 2: Write and understand one complete robot episode

[English](week-02.en.md) | [简体中文](week-02.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Documentation:** Update the [bilingual code guide](../doc/CODE_GUIDE.en.md) with this week's design rationale, implemented structures and verification evidence.

**Goal:** Implement the complete outer inference loop and trace a complete simulated episode.

**Start authoring when:** Week 1 connector contracts and pinned source are available; the loop can be implemented before target verification.

**Run-computer prerequisite:** Week 1 checks pass, the checkpoint/processors load, and the simulator and policy connectors are available.

Planning estimate: 12 active hours across five sessions, including evidence review and documentation. GPU runtime is additional and must be measured.

## Current implementation and verification

The complete canonical pilot source is implemented in [episode.py](../src/vla_grounding/episode.py), [episode_records.py](../src/vla_grounding/episode_records.py) and [trajectory.py](../src/vla_grounding/trajectory.py), with explicit-index reset/step support in the simulator and prediction-boundary recording in the policy connector. The [three case inputs](../configs/week-02-case-00.json) and [real target integration audit](../tests/smoke_episode.py) are available. Command syntax and artifact layout are in the [environment guide](../doc/ENVIRONMENT.en.md#week-1-audit-and-week-2-pilot-commands).

Portable array/case/stop/platform checks and Ruff pass. Actual policy queue/chunk behavior, selected states, three pilot videos and real failure cleanup remain target checks. Source availability does not complete those items. Strict static type-checker execution remains pending an available configured tool.

## Execution locations

Use the [shared handoff procedure](../doc/ENVIRONMENT.en.md#handoff-for-every-execution-visit); the session locations below govern the detailed steps.

1. **Prepare on the coding computer:** Write the lifecycle and the complete outer loop, then add counters and recording integration without importing the target stack for portable checks.
2. **Execute on the run computer:** After the Week 1 target gate, execute the bounded loop, three pilot rollouts, counter checks and resource-release checks.
3. **Return for review:** Return aligned observations/chunks/actions, counter and termination records, exact invocations, errors and pilot videos to document one iteration here.

Without target access, keep real-run checks pending, record the specific access or setup blocker, prepare the exact handoff and continue authoring that does not depend on target evidence.

## What to read and understand

Read in this order. Pending source is listed explicitly. Before completing this milestone, replace planned-code descriptions with exact implemented file/symbol links and add the relevant evidence reference.

| Order | Required reading |
| --- | --- |
| 1. Documents | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md#perception-to-action-contract): perception-to-action and software verification. [Code guide](../doc/CODE_GUIDE.en.md#3-data-flow-and-control-flow): pipeline and diagnostic-versus-executed action. |
| 2. Current code | [simulator.py](../src/vla_grounding/simulator.py): `RawObservation`, `environment_config` and all `SimulatorConnector` methods. |
| 3. Follow the calls | [policy.py](../src/vla_grounding/policy.py): `PolicyConnector.prepare_observation` / `select_action` / `reset` and `RecordedSmolVLA._get_action_chunk` and `ActionDecoder`; [smoke.py](../src/vla_grounding/smoke.py): upstream rollout wiring; [video.py](../src/vla_grounding/video.py): callback/recording. |
| 4. Milestone code/evidence | [episode.py](../src/vla_grounding/episode.py): `run_episode` / `main`; [episode_records.py](../src/vla_grounding/episode_records.py): required case/signals/result and `stop_reason`; [trajectory.py](../src/vla_grounding/trajectory.py): `save_arrays`; [tests/smoke_episode.py](../tests/smoke_episode.py): real chunk/frame audit. |

Understanding goals:

- Narrate one loop iteration from observation and instruction to a decoded seven-dimensional action and the next observation.
- Distinguish policy-step calls, new chunk predictions and executed actions; explain queue reset and decoding exactly once.
- Explain success, timeout, terminal events, infrastructure errors and resource cleanup using a real saved trace.

## Prepare and learn

- Inspect the pinned policy's reset and action-selection methods and the simulator's reset, step, success, and termination behavior.
- Learn the difference between normalized model actions, decoded control actions, and the controller's coordinate conventions.
- Read the action-queue implementation: determine when a new chunk is generated and when an existing action is reused.

## Reading route and expected understanding

- [SmolVLA policy source](https://github.com/huggingface/lerobot/blob/v0.6.1/src/lerobot/policies/smolvla/modeling_smolvla.py): find `reset`, `predict_action_chunk`, and `select_action`. Explain the public return value and the action queue without reading every network layer.
- [Environment source](https://github.com/huggingface/lerobot/blob/v0.6.1/src/lerobot/envs/libero.py): follow `reset` and `step` to the returned observation, success information, and termination value.
- [Processor source](https://github.com/huggingface/lerobot/blob/v0.6.1/src/lerobot/policies/smolvla/processor_smolvla.py): locate observation preparation and action decoding. Document where the outer loop calls these existing components.

## Implementation tasks

The items below define the code and documentation deliverables for this week. Existing source should be completed or extended; future components remain planned until implemented. Keep experimental parameters authoritative in the linked implementation plan.

1. **Single-episode inputs and outcomes.** Define runtime-validated episode inputs for one task, explicit instruction, state reference, policy seed and rollout limit. Return a typed episode outcome with stop reason, requested-goal result, step/counter totals, timing and artifact references. Keep genuine task failure, timeout, environment termination and infrastructure errors distinguishable.
2. **Complete outer loop.** Implement one synchronous episode lifecycle using the established connectors: restore/reset, clear policy/processors, prepare the observation and explicit instruction, select the next action through the supported queue, decode once, validate, step and record the next observation. Keep execution settings identical to the checkpoint contract; do not duplicate upstream model internals.
3. **Chunk and action instrumentation.** Count policy-step calls, newly generated chunks and simulator actions independently. Record where queue reuse occurs and associate predicted chunks with the actions actually executed from them. Instrument without requesting extra predictions, advancing RNG or changing action selection.
4. **Aligned trajectory and video writing.** Add per-step recording for raw observations, processed input summaries, exact instruction, chunk/action identifiers, decoded commands, predicate/outcome signals and frame indices. Preserve timing and ordering so one video frame can be traced to the relevant action and observation; save compressed trajectories with the episode result.
5. **Execution entry point and cleanup.** Expose a single-episode command with explicit configuration, case/assets and output paths. Reject an existing output identity and invalid inputs before expensive allocation. Close simulator/video resources on normal and error exits; preserve the original contextual exception and partial diagnostics without labeling an interrupted episode complete.
6. **Real integration and explanation.** Execute a short path check followed by the pilot episodes, reconcile counters against real chunk boundaries, and inspect preprocessing/decoding and final observations. Document the loop's functions, record fields, action-cache flow, stop decisions and resource lifecycle in the code guide with a concrete saved-episode walkthrough.

## Work sessions

### 1. Specify one episode before coding (2 hours)

**Location:** Coding computer: write pseudocode and inspect connector/source contracts. Any real step inspection uses returned Week 1 evidence or the target.

**Detailed procedure**

1. Write the episode lifecycle in plain language, from task/state selection through reset, action prediction, stepping, outcome recording, and resource release.

2. For each operation, identify the connector call, its actual return type, and which data the episode loop must retain. Mark the difference between a new observation and a processed model batch.

3. Define the stopping cases separately: requested-goal success, explicit episode limit, environment terminal event, and infrastructure exception. Do not collapse them into one Boolean.

4. Review the lifecycle and interfaces, resolve unclear contracts, and implement the complete loop in Session 2.

**Expected output:** Pseudocode and an input/output map for the complete loop implementation.

**If this does not work:** If you cannot say which object returns success or which function decodes actions, trace those two calls before writing the loop.

**Session completion checklist**

- [ ] write pseudocode covering environment reset, policy reset, observation preparation, instruction injection, action selection, stepping, scoring, and closing.
- [ ] Inspect a real step result and distinguish task success, episode termination, timeout, and an execution exception.
- [ ] review the pseudocode and connector contracts and implement the complete loop in Session 2.

### 2. Implement the complete episode loop (3 hours)

**Location:** Coding computer: make the complete loop implementation. Run computer: execute short-step and bounded-episode checks after the Week 1 gate.

**Detailed procedure**

1. Implement the first version, with one environment, one policy, one instruction, and one explicit development case.

2. Reset the environment and policy, prepare one observation, request an action through the supported policy API, decode it once, and send the correctly shaped action to the simulator.

3. First run only enough steps to inspect that path, then complete a bounded episode. Add the next observation only after the previous step result has been recorded.

4. At a selected step, inspect the actual instruction tokens, state shape, decoded action, and simulator outcome. Compare them with your Week 1 contract.

**Expected output:** A bounded loop whose individual state transitions can be inspected.

**If this does not work:** If the robot moves incorrectly, verify decoding happens exactly once and distinguish relative end-effector control from joint commands.

**Session completion checklist**

- [ ] implement the loop using established LeRobot calls and the agreed checkpoint execution settings; keep the first version single-task and single-episode.
- [ ] Trace one iteration with actual tensors, including the instruction that reaches tokenization and the seven-dimensional action sent to the environment.
- [ ] Run a development episode with an explicit step limit and verify that policy state and queued actions are reset at its start.

### 3. Add evidence and resolve integration failures (3 hours)

**Location:** Coding computer: integrate recording and review logs. Run computer: generate the three real pilot trajectories/videos and reproduce integration failures.

**Detailed procedure**

1. Connect recording around the implemented episode loop, preserving step indices and the relation between camera frames, observations, predicted chunks, and executed actions.

2. Record whether an action comes from a newly generated chunk or the existing queue; model output and executed-action count need not match.

3. Run the planned pilot episodes using recorded case settings. Keep unsuccessful trials and inspect the contact/grasp/place sequence in their videos.

4. Trace one successful or failed attempt back through the action decoding and state construction before proposing a model change.

**Expected output:** Pilot trajectories with aligned videos, predictions, actions, and honest outcome labels.

**If this does not work:** If video and state traces refer to different steps, fix recording alignment before using them to explain failures.

**Session completion checklist**

- [ ] integrate video and trajectory writing around the episode loop, preserving raw observations, predictions, executed actions, and completion information.
- [ ] inspect action decoding, image orientation, feature mapping, state construction, and relative control if behavior is unexpectedly unsuccessful.
- [ ] Save three development rollouts for the pilot task and classify observed outcomes honestly; do not assume a successful video must already exist.

### 4. Change the loop and document the findings (2 hours)

**Location:** Coding computer: implement and verify counters and predict counts. Transfer the change, run its short episode on the target and reconcile the returned trace.

**Detailed procedure**

1. Add counters for policy-step calls, newly generated chunks, and executed simulator actions using the actual public path.

2. Inspect the queue condition in the pinned source to decide what each counter means. Do not treat every `select_action` call as a new model prediction.

3. Run one short development episode and manually reconcile the counter values with recorded chunk boundaries.

4. Review the evidence and strongest alternative explanation, correct any identified root cause, rerun affected checks and document the reasoning in the relevant bilingual `doc/` pair.

**Expected output:** Counters that measure the events their names claim, supported by one manually checked trace.

**If this does not work:** If instrumentation changes action sampling or consumes extra random draws, remove that side effect and measure without a second policy call.

**Session completion checklist**

- [ ] add inference-call and executed-action counters to the episode loop.
- [ ] Predict why the counters differ under chunked execution, then verify the explanation using a real trace.
- [ ] verify the reasoning and any correction, rerun affected checks, and update the bilingual design/code explanations with evidence references.

### 5. Explain the episode and prepare reset experiments (2 hours)

**Location:** Coding computer: explain returned traces and prepare reset cases. Run computer: verify normal/error resource release.

**Detailed procedure**

1. Select a concrete frame and narrate its raw observation, processed input, queued/predicted action, decoded command, and next observation.

2. Verify normal completion and an actual development error both release resources while preserving a clear outcome or error record.

3. Write a short explanation of why task failure can occur even when the loop is technically correct.

4. List simulator state, policy queue/cache, RNG, and preprocessing settings needed for the next week's matched reset experiment.

**Expected output:** A complete episode explanation and a checklist of state that must be controlled next.

**If this does not work:** Do not declare a pipeline reliable while a terminal event is silently triggering another reset or losing its final observation.

**Session completion checklist**

- [ ] Replay one video alongside its trace and explain the path from a specific instruction through one predicted chunk to motion.
- [ ] Confirm resources close after normal completion and after a real development failure; preserve the useful error context.
- [ ] Identify which simulator state, RNG state, and policy cache must be controlled for Week 3 comparisons.

## Evidence and completion checks

- [x] Documentation ready: the paired design/code guide covers all implemented structures, rationale, interfaces and verification status.
- [ ] Authoring ready: this week's source/configuration and applicable local checks are included in the identified handoff.
- [ ] Target verified: the required real target evidence has returned and been reviewed against that handoff.
- [ ] The outer loop completes a bounded real episode and saves a playable video and inspectable trajectory.
- [ ] Success, timeout, and infrastructure failure remain distinguishable; a failed grasp is not relabeled as an exception.
- [ ] The code guide explains action caching and identifies preprocessing and decoding.

## Optional review questions

1. What changes when a queued action is used instead of generating a new chunk?
2. Which state must be reset between episodes, and what could happen if the policy queue is retained?
3. Why could correct tensor shapes coexist with incorrect physical control?

## Delivery summary

> Implement the complete episode loop, counters and recording; run three bounded pilot episodes, diagnose failures and document lifecycle, action caching and termination.

## Ready for the next week

Independent authoring for later milestones may continue from agreed interfaces. The following gate applies to dependent execution and result claims.

Proceed when the bounded episode loop and its trace are reliable. Task failures can be investigated, but unexplained interface errors must be resolved first.

