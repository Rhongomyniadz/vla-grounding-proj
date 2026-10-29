# Week 3: Reproducible resets and an action-horizon exercise

[English](week-03.en.md) | [简体中文](week-03.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Documentation:** Update the [bilingual code guide](../doc/CODE_GUIDE.en.md) with this week's design rationale, implemented structures and verification evidence.

**Goal:** Establish matched development rollouts and understand the effect of executing more actions between observations.

**Start authoring when:** The implemented Week 2 loop and reset/action interfaces are written; actual trace-dependent work waits for target evidence.

**Run-computer prerequisite:** Week 2 provides a working episode loop and saved observations, actions, and outcomes.

Planning estimate: 12 active hours across five sessions, including evidence review and documentation. GPU runtime is additional and must be measured.

## Execution locations

Use the [shared handoff procedure](../doc/ENVIRONMENT.en.md#handoff-for-every-execution-visit); the session locations below govern the detailed steps.

1. **Prepare on the coding computer:** Specify explicit state/seed records, reset comparisons, tolerance rationale and the isolated horizon exercise; preserve the main configuration.
2. **Execute on the run computer:** After the Week 2 target gate, resolve real state references and run A/A, A/B/A and matched horizon comparisons.
3. **Return for review:** Return serialized-state references/hashes, restored observations, first predictions, comparison/tolerance reports, counters, latency, outcomes and videos.

Without target access, keep real-run checks pending, record the specific access or setup blocker, prepare the exact handoff and continue authoring that does not depend on target evidence.

## What to read and understand

Read in this order. Pending source is listed explicitly. Before completing this milestone, replace planned-code descriptions with exact implemented file/symbol links and add the relevant evidence reference.

| Order | Required reading |
| --- | --- |
| 1. Documents | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md#perception-to-action-contract): reset/action-horizon controls. [Environment guide](../doc/ENVIRONMENT.en.md#handoff-for-every-execution-visit): source/evidence identity. [Code guide](../doc/CODE_GUIDE.en.md): reset limitations. |
| 2. Current code | [simulator.py](../src/vla_grounding/simulator.py): `SimulatorConnector.reset` and `environment_config`; identify the advancing upstream state index. |
| 3. Follow the calls | [policy.py](../src/vla_grounding/policy.py): `PolicyConnector.reset` and action queue use; [config.py](../src/vla_grounding/config.py): explicit seed and rollout-limit settings. |
| 4. Milestone code/evidence | Explicit state capture/restoration, A/A and A/B/A comparisons and horizon diagnostic functions: planned; read their real source and tolerance decisions after implementation. |

Understanding goals:

- List simulator, settling, RNG, processor and policy state that must be controlled before comparing episodes.
- Explain why the same integer seed or similar image does not prove identical restored state.
- Locate the earliest divergence in paired traces and explain how a shorter execution horizon changes replanning without changing weights.

## Prepare and learn

- Read how the pinned environment restores initial states and settles physics after reset; distinguish reset seeds from explicit simulator state.
- Inspect all policy state that persists across calls, including action queues and model caches.
- Learn why stochastic action sampling, settling steps, and rendering settings can affect repeatability.

## Reading route and expected understanding

- [Pinned reset implementation](https://github.com/huggingface/lerobot/blob/v0.6.1/src/lerobot/envs/libero.py): find how initial-state indices advance and when settling steps occur. Read the order, not just method names.
- [Policy reset/action selection](https://github.com/huggingface/lerobot/blob/v0.6.1/src/lerobot/policies/smolvla/modeling_smolvla.py): identify state retained between calls and the configured action execution horizon.
- Revisit the implementation plan's perception-to-action contract. Write down which settings will remain fixed in the main study before running the exploratory horizon comparison.

## Implementation tasks

The items below define the code and documentation deliverables for this week. Existing source should be completed or extended; future components remain planned until implemented. Keep experimental parameters authoritative in the linked implementation plan.

1. **Explicit state restoration.** Extend the simulator boundary to capture and restore a specified serialized initial state rather than relying on the advancing reset index. Separate portable task/state identity and content hashes from target-local file resolution. Validate that the requested state belongs to the intended task and record settling order and the policy-visible starting observation.
2. **Complete reset procedure.** Implement one explicit episode-start sequence covering simulator state, settling steps, policy/model cache, action queue, both processor pipelines and sampling RNG. Keep state restoration and observation capture ordered consistently. Use fresh returned data and avoid mutating a shared case specification.
3. **Comparison records and tolerances.** Produce structured state/observation/first-chunk comparison records. Separate exact identity checks from numeric checks with tolerances justified before outcome inspection. Report the earliest mismatching field, shape, magnitude and source identity; do not loosen tolerance to obtain a passing label.
4. **A/A and A/B/A diagnostics.** Implement development procedures that restore A twice and restore A after an unrelated B episode. Save inputs, state fingerprints, first predictions and outcomes, then identify whether any divergence begins in restoration, preprocessing, RNG or cached policy state.
5. **Isolated action-horizon comparison.** Construct matched development configurations for the checkpoint horizon and one supported shorter horizon. Preserve weights, physical states, instruction, policy seed, control frequency and episode limits. Measure replanning/chunk counts, executed actions, latency and behavior; keep these outputs and identities separate from the frozen main study.
6. **Integration and explanation.** Reuse the episode loop and real traces to verify both diagnostics. Document restoration order, all retained state, hash meanings, tolerance rationale, counter behavior and the exploratory horizon result in the existing code guide; link the evidence and leave unexplained runtime differences open.

## Work sessions

### 1. Specify a reproducible development case (2 hours)

**Location:** Coding computer: design case fields and comparison rules. Run computer: resolve/capture real states and confirm numeric representation.

**Detailed procedure**

1. Choose a few development state references and save the actual serialized simulator state identity, not merely an environment seed.

2. For each case, record policy sampling seed, instruction, camera/control settings, settling steps, action execution horizon, and episode limit.

3. Decide where to capture state: distinguish the loaded state from the post-settling observation actually received by the policy.

4. Before comparing runs, identify exact-match metadata and numeric quantities requiring a documented tolerance. Determine tolerance from the numeric representation and supported platform, not from a desired success label.

**Expected output:** A small explicit case table and a justified comparison procedure.

**If this does not work:** If your wrapper automatically advances the initial-state index, restore by explicit reference instead of assuming consecutive resets repeat the scene.

**Session completion checklist**

- [ ] identify a small set of development initial states and define the instruction, policy seed, settling behavior, horizon, and step limit for each case.
- [ ] expose supported state restoration and capture the restored state and observation fingerprints.
- [ ] Write down which quantities should match exactly and which require a justified tolerance before running comparisons.

### 2. Verify restoration and policy reset (3 hours)

**Location:** Run computer: perform A/A and A/B/A restoration, reset and first-prediction checks; diagnose returned differences here.

**Detailed procedure**

1. Restore case A, reset policy state and the policy RNG deliberately, and capture its first observation and first predicted chunk.

2. Repeat A immediately, then run another case B and restore A again. Compare initial state, post-settling observation, first prediction, and outcome.

3. Find the earliest divergence. A state mismatch precedes any model issue; matching inputs with different predictions suggests policy RNG/cache or numerical settings.

4. Fix or characterize the source, then rerun the same comparison. Keep the renderer, settling steps, and execution settings unchanged during diagnosis.

**Expected output:** An A/A and A/B/A comparison with a clear explanation of equality or the first divergence.

**If this does not work:** A similar-looking screenshot is insufficient evidence of identical simulator state.

**Session completion checklist**

- [ ] Run the same development case twice with explicit simulator state restoration and policy reset; compare starting state, observations, first prediction, and outcome.
- [ ] Interleave an unrelated development episode, then restore the original case again to detect state leaking between episodes.
- [ ] If results differ, isolate simulator, policy-RNG, action-cache, preprocessing, and rendering causes before treating the pair as matched.

### 3. Run the horizon comparison (3 hours)

**Location:** Coding computer: predict the horizon effect and prepare configs. Run computer: execute both supported horizons on matched development cases.

**Detailed procedure**

1. Read the configured chunk capacity and action execution horizon. Select the original horizon and one shorter supported value; do not change model weights or control frequency.

2. Predict the number of replanning events and what visual corrections could occur for each value.

3. Run the same small development cases with both horizons, preserving state, instruction, sampling seed, and step limit.

4. Compare success, latency, inference count, executed actions, and videos. Treat this as a development sensitivity exercise; keep the original main-study setting.

**Expected output:** A paired horizon comparison with pre-run predictions and measured behavior.

**If this does not work:** If you also change chunk generation size, denoising settings, or physics frequency, separate that experiment before interpreting a horizon effect.

**Session completion checklist**

- [ ] choose the checkpoint execution horizon and one shorter supported horizon, holding scene, instruction, seed, and rollout limit fixed.
- [ ] Predict the effect on replanning frequency and behavior, then run a small matched development panel for both settings.
- [ ] Measure inference calls, executed actions, latency, outcome, and visible corrections; retain the main study's original horizon.

### 4. Diagnose one trace and document the findings (2 hours)

**Location:** Coding computer: inspect returned traces and form a hypothesis. A new controlled rollout requires a new target handoff.

**Detailed procedure**

1. Select one unexpected difference from your saved cases.

2. Locate the first observation/action where the traces differ, then form one testable hypothesis about its source.

3. Change one development factor only and repeat the diagnostic. Record which evidence would contradict your explanation.

4. Review the evidence and strongest alternative explanation, correct any identified root cause, rerun affected checks and document the reasoning in the relevant bilingual `doc/` pair.

**Expected output:** A concrete debugging argument grounded in the earliest divergence.

**If this does not work:** Do not explain every difference as randomness before checking explicit state references and action-queue reset.

**Session completion checklist**

- [ ] use saved traces to investigate one repeatability difference or one horizon-dependent behavior.
- [ ] Write a specific hypothesis, identify supporting observations, and perform one controlled development check.
- [ ] verify the reasoning and any correction, rerun affected checks, and update the bilingual design/code explanations with evidence references.

### 5. Prepare the runner contract (2 hours)

**Location:** Coding computer: document only the verified reset contract and prepare manifest fields from returned evidence.

**Detailed procedure**

1. Record the verified reset/settling order in the environment connector docstring and retain the development comparison evidence.

2. Summarize the horizon experiment in the relevant paired document in `doc/`, clearly marking it as exploratory and separate from the main evaluation.

3. Write the minimal identifiers needed to reconstruct a paired case; hand these to the manifest work next week.

4. Check that an exploratory run cannot overwrite the main configuration or be resumed under a different horizon with the same identity.

**Expected output:** A reproducible reset contract and evidence that exploratory changes remain isolated.

**If this does not work:** Unexplained state drift blocks paired evaluation even if the robot sometimes succeeds.

**Session completion checklist**

- [ ] Save the reset procedure, tolerance rationale, development-case identities, and horizon-exercise results in the relevant paired document in `doc/` and code docstrings.
- [ ] List the case identifiers and runtime metadata that Week 4's manifest must preserve.
- [ ] Ensure exploratory horizon changes and development state choices cannot silently enter the frozen evaluation configuration.

## Evidence and completion checks

- [ ] Documentation ready: the paired design/code guide covers all implemented structures, rationale, interfaces and verification status.
- [ ] Authoring ready: this week's source/configuration and applicable local checks are included in the identified handoff.
- [ ] Target verified: the required real target evidence has returned and been reviewed against that handoff.
- [ ] Repeated and interleaved restoration checks produce explainable matching states and observations.
- [ ] A small matched horizon comparison includes a prediction, measured counters, outcomes, and an interpretation.
- [ ] The main checkpoint horizon remains explicit, and episode state cannot leak through retained policy queues.

## Optional review questions

1. Why does sharing an environment seed not guarantee an identical initial scene?
2. How can a long action execution horizon reduce the opportunity to correct a mistaken grasp?
3. Which mismatch would you investigate first if starting states match but the first predicted actions differ?

## Delivery summary

> Implement explicit restoration and reset checks, run A/A and A/B/A comparisons and the isolated horizon study, and document tolerances, state control and measured behavior.

## Ready for the next week

Independent authoring for later milestones may continue from agreed interfaces. The following gate applies to dependent execution and result claims.

Proceed when paired development cases can be restored reliably and unexplained differences have been resolved or characterized before analysis.

