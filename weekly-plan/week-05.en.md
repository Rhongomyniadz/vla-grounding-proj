# Week 5: Language cases and correct goal scoring

[English](week-05.en.md) | [简体中文](week-05.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Documentation:** Update the [bilingual code guide](../doc/CODE_GUIDE.en.md) with this week's design rationale, implemented structures and verification evidence.

**Goal:** Implement controlled instruction comparisons and verify that changed-target trials score the requested object.

**Start authoring when:** Week 4 manifest/case interfaces and the language protocol are available; runtime scoring validation is a separate gate.

**Run-computer prerequisite:** Week 4 provides fixed task/state identities, a working case builder, and resumable development execution.

Planning estimate: 12 active hours across five sessions, including evidence review and documentation. GPU runtime is additional and must be measured.

## Execution locations

Use the [shared handoff procedure](../doc/ENVIRONMENT.en.md#handoff-for-every-execution-visit); the session locations below govern the detailed steps.

1. **Prepare on the coding computer:** Write the template families, language-case builder and goal selector; review pinned predicate/termination code without claiming it works yet.
2. **Execute on the run computer:** After the Week 4 target gate, verify actual object/region names, tokenization, real positive/negative predicate states, old-goal termination and development language pairs.
3. **Return for review:** Return exact text/tokens, matched state/seed records, predicate truth tables, first-goal/end-reason traces, development results and paired videos.

Without target access, keep real-run checks pending, record the specific access or setup blocker, prepare the exact handoff and continue authoring that does not depend on target evidence.

## What to read and understand

Read in this order. Pending source is listed explicitly. Before completing this milestone, replace planned-code descriptions with exact implemented file/symbol links and add the relevant evidence reference.

| Order | Required reading |
| --- | --- |
| 1. Documents | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md#b-evaluate-language-behavior): six conditions, prompt splits, same-scene controls and requested-goal scoring. [Code guide](../doc/CODE_GUIDE.en.md): explicit-text pipeline and planned scorer. |
| 2. Current code | [simulator.py](../src/vla_grounding/simulator.py): `prepare_observation` / `instruction`; [policy.py](../src/vla_grounding/policy.py): tokenization path and masks. |
| 3. Follow the calls | [smoke.py](../src/vla_grounding/smoke.py): current benchmark-text injection; contrast it with the required explicit intervention path. |
| 4. Milestone code/evidence | Prompt registry, language-case builder, requested-goal predicate selection, first-goal recording and termination handling: planned; read actual code plus the pinned native predicate/termination source. |

Understanding goals:

- Explain which question paraphrases, changed targets and empty instructions answer, and identify their confounders.
- Trace exact text into tokens and show what is shared versus changed in a same-scene pair.
- Explain old-goal termination, initial false predicates, first-object ties and eventual success using real truth tables/traces.

## Prepare and learn

- Read the implementation plan's language protocol and inspect LIBERO's existing goal predicates and termination path.
- Learn why paraphrase invariance, changed-target responsiveness, and empty-instruction behavior test different properties.
- Inspect the actual object and basket-region identifiers in all four scenes; task names alone do not define the scorer.

## Reading route and expected understanding

- Read the [language protocol](../doc/IMPLEMENTATION_PLAN.en.md#b-evaluate-language-behavior) and the original/alternative object pairs before writing prompts.
- Inspect [LIBERO's floor-manipulation goal implementation](https://github.com/Lifelong-Robot-Learning/LIBERO/blob/master/libero/libero/envs/problems/libero_floor_manipulation.py) and the corresponding installed, pinned task definitions. Find how native predicates use object/region identities.
- Inspect the [environment termination wrapper](https://github.com/huggingface/lerobot/blob/v0.6.1/src/lerobot/envs/libero.py). Explain why changing the model's text does not automatically change the environment's old success condition.

## Implementation tasks

The items below define the code and documentation deliverables for this week. Existing source should be completed or extended; future components remain planned until implemented. Keep experimental parameters authoritative in the linked implementation plan.

1. **Prompt registry and split validation.** Implement a structured registry for canonical, training, validation-only, held-out final, changed-target and empty conditions. Make object/operation/destination and template identity explicit. Validate semantic consistency and disjoint split membership; freeze wording before adaptation without selecting final templates by rollout success.
2. **Language-case builder.** Extend pure case construction to return exact instruction text, condition/template identity, requested object/goal and inherited state/seed references. Keep the physical scene fixed across original/changed-target pairs. Permit only intended language/goal/episode-identity differences and validate this pairing before execution.
3. **Policy-text and token checks.** Pass the case's text through the actual observation and checkpoint processor path. Preserve intentional empty content, inspect tokens/masks and reject loss of required object/destination wording. Prevent environment task descriptions from overwriting the supplied instruction later in the pipeline.
4. **Requested-goal scoring.** Implement goal selection using verified native object/region predicate arguments. Evaluate all relevant object-placement predicates at each executed step, keep the first satisfied goal set and simultaneous ties, and separately report eventual requested-goal success. Require both competing goals to be false at reset.
5. **Termination integration.** Identify the old benchmark goal's terminal event separately from genuine simulator failure and timeout. Continue a changed-target trial after original-goal completion until its requested goal or another valid stopping condition. Preserve end reasons and predicate traces instead of discarding every terminal signal.
6. **Real development verification and explanation.** Check both scorers against known negative/positive real states and demonstrate continuation after old-goal completion. Execute only permitted development conditions, audit matched text/state/seed records and inspect paired videos. Document prompt lineage, case differences, predicate truth tables, tie semantics and termination flow in the code guide.

## Work sessions

### 1. Design instructions before implementation (2 hours)

**Location:** Coding computer: design and separate prompt families. Run computer: verify real scene identifiers and checkpoint tokenization before freezing.

**Detailed procedure**

1. Write the original meaning as object, operation, and destination before rewriting the sentence. For example, a development instruction about alphabet soup must still request alphabet soup in the basket.

2. Construct one equivalent development paraphrase and one changed-target instruction. Compare them word by word and identify the intended semantic difference.

3. Create the planned training, validation, and final template families. Separate phrasing families as well as exact strings; do not put trivial variants of the same template in every split.

4. Check every filled instruction against scene object identities and tokenizer output. Freeze the final template set without rolling it out for prompt selection.

**Expected output:** A prompt registry whose semantic role and split membership you can justify.

**If this does not work:** If a paraphrase introduces an ambiguous pronoun, missing object, different destination, or extra action, revise it before freezing.

**Session completion checklist**

- [ ] write canonical, paraphrase, changed-target, and empty-instruction development examples and predict the expected behavior.
- [ ] Write four training paraphrase templates, one validation-only template, and three final-test templates; keep target and destination explicit.
- [ ] Freeze and label template families before adaptation, checking semantic equivalence and tokenization without running final-test rollouts.

### 2. Implement language-case construction (3 hours)

**Location:** Coding computer: implement same-scene language cases. Run computer: trace the actual processor input, masks and requested-goal mapping.

**Detailed procedure**

1. Write your case-builder extension so instruction text, requested object/goal, and inherited physical-state identity are explicit outputs.

2. For a same-state original/changed-target pair, compare every case field. Only intended language/goal metadata and episode identity should differ.

3. Trace the actual text through the batch passed to tokenization; confirm the environment's original description is not reinserted later.

4. Preserve empty instruction content through the normal processor path and inspect its resulting mask/tokens rather than replacing it with the canonical task.

**Expected output:** A real paired input trace proving what text and goal each rollout actually receives.

**If this does not work:** Changing a filename or caption without changing policy input does not implement a language intervention.

**Session completion checklist**

- [ ] extend your case builder to attach instruction identity, exact text, requested object, goal predicate, and matched state/seed references.
- [ ] Build canonical and changed-target cases from the same scene; do not load a different task to change the requested object.
- [ ] review serialization and tokenizer checks, ensuring prompt text is not overwritten by the environment's original task description.

### 3. Validate predicates and termination with real states (3 hours)

**Location:** Coding computer: write your goal selection first. Run computer: verify native predicates and continuation after old-goal completion using real states.

**Detailed procedure**

1. Map the requested object and basket region to native predicate arguments. Keep goal selection separate from physical geometry calculations.

2. Use isolated real simulator states: neither object placed, A placed, and B placed. Check original and alternative predicates on each state; retain their outputs.

3. Observe the old task's terminal signal when A is completed during a B-requested development trial. Verify the connector continues the B trial while still respecting genuine simulator failure and the explicit limit.

4. Evaluate relevant object predicates at every executed step. Record the first satisfied set; if multiple goals first appear together, keep the tie explicitly.

**Expected output:** A scoring truth table and a real execution showing the old goal cannot end an alternative-goal trial.

**If this does not work:** Do not fix old-goal termination by blindly discarding every terminal event. Verify the source and distinguish goal completion from failure.

**Session completion checklist**

- [ ] implement requested-goal selection using existing LIBERO predicates; score every relevant basket-object goal needed to identify first completion.
- [ ] Verify both goals are false at reset and use known positive simulator states to show that placing A or B satisfies the corresponding predicate.
- [ ] review the environment boundary so achieving the old goal cannot terminate a changed-target trial; record simultaneous first goals explicitly.

### 4. Inspect a paired failure and document the findings (2 hours)

**Location:** Coding computer: inspect a returned original/changed-target pair; perform any new controlled check on the target.

**Detailed procedure**

1. Choose one same-scene original/changed-target development pair.

2. Check the restored state, instruction tokens, action trace, first satisfied object predicate, eventual goal result, and end reason before watching the video for interpretation.

3. Write one evidence-based classification: incorrect target selection, inability to manipulate the intended object, or scoring/execution error.

4. Review the evidence and strongest alternative explanation, correct any identified root cause, rerun affected checks and document the reasoning in the relevant bilingual `doc/` pair.

**Expected output:** A failure diagnosis that links the observation to a specific model or pipeline behavior.

**If this does not work:** Different physical scenes or mismatched sampling seeds must be corrected before attributing a difference to language.

**Session completion checklist**

- [ ] inspect one original/changed-target development pair with its state, text, actions, predicates, and video.
- [ ] Classify the observed outcome as target-selection error, manipulation failure, or scoring/execution error, with concrete evidence.
- [ ] verify the reasoning and any correction, rerun affected checks, and update the bilingual design/code explanations with evidence references.

### 5. Run the development matrix and audit it (2 hours)

**Location:** Run computer: execute the development matrix. Coding computer: audit returned pairing, prompts and scoring evidence.

**Detailed procedure**

1. Run the allowed development conditions on development states, keeping final templates and final states sealed from tuning.

2. Build a pair-audit view showing state fingerprint, policy seed, exact text, requested goal, first object, eventual success, and end reason.

3. Investigate unexpected identical behavior by first verifying text actually reaches the model and the scorer changes correctly.

4. Save both successful and unsuccessful evidence and prepare the clean real records needed for hand-calculated metrics.

**Expected output:** Audited development language results with valid pairing and no final-test-driven prompt selection.

**If this does not work:** Good paraphrase success alone is insufficient; inspect changed-target responsiveness and the possibility of scene-based habitual behavior.

**Session completion checklist**

- [ ] Run canonical, training-paraphrase, changed-target, and empty-instruction conditions on development states only.
- [ ] Check that paired starting-state hashes and policy sampling seeds match while instruction and requested-goal fields differ as intended.
- [ ] Save exact prompts and tokenization checks; keep final-test templates and final initial states out of development execution.

## Evidence and completion checks

- [ ] Documentation ready: the paired design/code guide covers all implemented structures, rationale, interfaces and verification status.
- [ ] Authoring ready: this week's source/configuration and applicable local checks are included in the identified handoff.
- [ ] Target verified: the required real target evidence has returned and been reviewed against that handoff.
- [ ] The case builder and goal selector produce valid same-scene language comparisons.
- [ ] Real-state checks verify both requested-goal predicates and changed-target termination behavior.
- [ ] Training, validation, and final template sets are explicit, disjoint, and have not been silently substituted.

## Optional review questions

1. Why can strong paraphrase performance coexist with weak instruction following?
2. What false conclusion could result from scoring a changed-target episode with the original task's success predicate?
3. Why is eventual success different from selecting the requested object first?

## Delivery summary

> Write and freeze the prompt families, implement language-case construction and goal selection, verify real-state scoring and termination, and document the controls and interpretation.

## Ready for the next week

Independent authoring for later milestones may continue from agreed interfaces. The following gate applies to dependent execution and result claims.

Proceed only when changing text truly changes the requested-goal scorer without changing the physical scene, and the scoring contract passes real-state checks.

