# Week 10: Select checkpoints and execute the frozen final study

[English](week-10.en.md) | [简体中文](week-10.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Goal:** Apply the predeclared selection rule, then complete final evaluation without tuning on its outcomes.

**Start when:** Both full training arms are complete and reloadable; final language states/templates and robustness manifests remain frozen and unused for tuning.

Time budget: 12 active hours across five sessions; one hour is independent work with the agent closed. Computer runtime is additional.

## Prepare and learn

- Read the implementation plan's validation-only checkpoint selection, final episode budget, and incomplete-run rules.
- Learn why model selection must finish before inspecting held-out outcomes, including why repeated test-driven fixes change the study's interpretation.
- Inspect all case-level pairing keys and the result-coverage summary before allocating long evaluation jobs.

## Work sessions

### 1. Select checkpoints using development validation (2 hours)

- [ ] Evaluate each arm's five candidate checkpoints on the four tasks, five development states, canonical wording, and the validation-only paraphrase.
- [ ] Use the predeclared mean success rule, breaking ties toward the earlier checkpoint; preserve all validation scores and selected identities.
- [ ] You: calculate a small selection example yourself and confirm neither training loss nor final-test performance overrode the rule.

### 2. Freeze final policy and case identities (3 hours)

- [ ] Record immutable identities for the pretrained policy and the two selected adapters, processors, backends, and evaluation configurations.
- [ ] Audit the final language matrix, robustness cases, seeds, initial states, prompt splits, time limits, and action horizon against the plan.
- [ ] Generate a complete case-count/coverage expectation and estimate wall-clock runtime from actual pilot throughput, including prior selection runs.

### 3. Run the final language and robustness panels (3 hours)

- [ ] Agent: execute the frozen manifests for all three policies with videos, trajectories, complete metadata, and progress reporting.
- [ ] You: monitor operational health and completion coverage without using emerging success rates to change prompts, tasks, checkpoints, or settings.
- [ ] Use supported same-manifest resume after interruption; do not treat infrastructure exceptions as completed failures or silently drop hard cases.

### 4. Audit evidence independently, then review (2 hours)

- [ ] For the first hour, close the agent and audit one original/changed-target pair across policies and one robustness case from records and videos.
- [ ] Verify actual requested text, goal scorer, starting state/variant, sampling seed, policy identity, and termination behavior.
- [ ] In the second hour, review any discrepancy with the agent; if a real bug invalidates outcomes, identify and rerun all affected comparisons consistently.

### 5. Close coverage and preserve the final dataset (2 hours)

- [ ] Verify 480 language cases and 160 robustness/anchor cases per policy, for 1,920 completed final episodes in total.
- [ ] Keep development and checkpoint-selection runs separately labeled; retain exceptions and rerun provenance rather than hiding them.
- [ ] Freeze the completed result collection for Week 11 analysis and record any unresolved omissions explicitly instead of claiming full completion.

## Evidence and completion checks

- [ ] Checkpoint selection is reproducible from validation-only scores and follows the fixed tie rule.
- [ ] All final cases have correct immutable policy/backend identities and preserved matched comparison keys.
- [ ] The complete 1,920-episode result collection is auditable; unresolved infrastructure gaps are not disguised as measured outcomes.

## Explain without the agent

1. Why does selecting the checkpoint with the best final-test score invalidate a clean held-out comparison?
2. What distinguishes an operational retry from changing experimental conditions after seeing results?
3. Which outcomes must be revisited if a goal-scoring bug is discovered during the audit?

## Suggested request to the coding agent

> Evaluate validation checkpoints with the fixed rule, freeze selected identities, execute and resume the final manifests, and report coverage without tuning on test results.

## Ready for the next week

Begin final analysis only when coverage is complete or clearly marked incomplete, and all correctness issues affecting reported comparisons are resolved.

