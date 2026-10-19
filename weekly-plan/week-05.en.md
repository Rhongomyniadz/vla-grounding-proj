# Week 5: Language cases and correct goal scoring

[English](week-05.en.md) | [简体中文](week-05.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Goal:** Implement controlled instruction comparisons and verify that changed-target trials score the requested object.

**Start when:** Week 4 provides fixed task/state identities, a working case builder, and resumable development execution.

Time budget: 12 active hours across five sessions; one hour is independent work with the agent closed. Computer runtime is additional.

## Prepare and learn

- Read the implementation plan's language protocol and inspect LIBERO's existing goal predicates and termination path.
- Learn why paraphrase invariance, changed-target responsiveness, and empty-instruction behavior test different properties.
- Inspect the actual object and basket-region identifiers in all four scenes; task names alone do not define the scorer.

## Work sessions

### 1. Design instructions before implementation (2 hours)

- [ ] You: write canonical, paraphrase, changed-target, and empty-instruction development examples and predict the expected behavior.
- [ ] Write four training paraphrase templates, one validation-only template, and three final-test templates; keep target and destination explicit.
- [ ] Freeze and label template families before adaptation, checking semantic equivalence and tokenization without running final-test rollouts.

### 2. Implement language-case construction (3 hours)

- [ ] You: extend your case builder to attach instruction identity, exact text, requested object, goal predicate, and matched state/seed references.
- [ ] Build canonical and changed-target cases from the same scene; do not load a different task to change the requested object.
- [ ] Agent: review serialization and tokenizer checks, ensuring prompt text is not overwritten by the environment's original task description.

### 3. Validate predicates and termination with real states (3 hours)

- [ ] You: implement requested-goal selection using existing LIBERO predicates; score every relevant basket-object goal needed to identify first completion.
- [ ] Verify both goals are false at reset and use known positive simulator states to show that placing A or B satisfies the corresponding predicate.
- [ ] Agent: review the environment boundary so achieving the old goal cannot terminate a changed-target trial; record simultaneous first goals explicitly.

### 4. Inspect a paired failure independently, then review (2 hours)

- [ ] For the first hour, close the agent and inspect one original/changed-target development pair with its state, text, actions, predicates, and video.
- [ ] Classify the observed outcome as target-selection error, manipulation failure, or scoring/execution error, with concrete evidence.
- [ ] In the second hour, challenge that classification with the agent and verify one controlled follow-up if needed.

### 5. Run the development matrix and audit it (2 hours)

- [ ] Run canonical, training-paraphrase, changed-target, and empty-instruction conditions on development states only.
- [ ] Check that paired starting-state hashes and policy sampling seeds match while instruction and requested-goal fields differ as intended.
- [ ] Save exact prompts and tokenization checks; keep final-test templates and final initial states out of development execution.

## Evidence and completion checks

- [ ] The learner-written case builder and goal selector produce valid same-scene language comparisons.
- [ ] Real-state checks verify both requested-goal predicates and changed-target termination behavior.
- [ ] Training, validation, and final template sets are explicit, disjoint, and have not been silently substituted.

## Explain without the agent

1. Why can strong paraphrase performance coexist with weak instruction following?
2. What false conclusion could result from scoring a changed-target episode with the original task's success predicate?
3. Why is eventual success different from selecting the requested object first?

## Suggested request to the coding agent

> Review my language-case builder and predicate selection, verify real-state scoring and old-goal termination handling, and leave experimental interpretation to me first.

## Ready for the next week

Proceed only when changing text truly changes the requested-goal scorer without changing the physical scene, and the scoring contract passes real-state checks.

