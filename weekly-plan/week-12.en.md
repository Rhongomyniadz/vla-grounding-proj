# Week 12: Reproduce, demonstrate, and verify independent understanding

[English](week-12.en.md) | [简体中文](week-12.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Goal:** Finish a reviewable portfolio and demonstrate that you can operate and modify the core system yourself.

**Start when:** Week 11 provides an evidence-based report, final figures, annotated examples, and the preserved experiment artifacts.

Time budget: 12 active hours across five sessions; one hour is independent work with the agent closed. Computer runtime is additional.

## Prepare and learn

- Read the setup/run instructions as a new contributor and identify assumptions that only exist in your shell or memory.
- Review all learning acceptance criteria in the implementation plan and choose a small representative reproduction panel.
- Distinguish reproducing a configuration and measured behavior from promising bit-identical GPU results across different runtime environments.

## Work sessions

### 1. Prepare a fresh reproduction environment (2 hours)

- [ ] Agent: create a fresh project environment without deleting the working setup, datasets, checkpoints, or final artifacts.
- [ ] Use locked dependencies and immutable source/artifact references, then verify CUDA, both cameras, policy inputs, and processor identity again.
- [ ] You: follow the documented steps literally and identify missing environment variables, paths, assets, or unstated manual steps.

### 2. Reproduce a representative comparison (3 hours)

- [ ] Run a small explicit panel containing an original/changed-target pair and one robustness case for each of the three policies.
- [ ] Compare restored state/variant identity, actual instruction, predicted/executed actions, scoring, metadata, and outcomes with the preserved records.
- [ ] Investigate differences using documented numerical tolerances and runtime details; report remaining reproducibility limits without claiming full-suite reruns.

### 3. Complete the portfolio walkthrough (3 hours)

- [ ] You: prepare a short explanation of the research question, system data flow, comparison design, principal findings, and limitations.
- [ ] Agent: help organize existing figures, annotated videos, artifact links, and verified setup/run commands in the README and report.
- [ ] Check that every showcased result is real and labeled, generated outputs are recoverable, and no automatic publishing or commit occurs.

### 4. Make a core change independently, then review (2 hours)

- [ ] For the first hour, close the agent and add one useful analysis metric or make a controlled development-only change to your episode/case logic.
- [ ] Predict the effect, implement it, and verify it against real saved records or development rollouts without changing frozen final conditions.
- [ ] In the second hour, explain the change and evidence to the agent, then review correctness and both architectural language versions if affected.

### 5. Perform the final learning and repository audit (2 hours)

- [ ] With the agent closed, trace a complete instruction-to-action episode, explain paired goal scoring and the adaptation control, and diagnose one saved failure.
- [ ] Verify document links, paired translations, the weekly checklist status, reproduction evidence, and report consistency; leave unfinished items visibly open.
- [ ] Record a justified next experiment as future work while keeping the current project's scope, evidence, and uncommitted review state intact.

## Evidence and completion checks

- [ ] A fresh environment can execute the documented representative comparison and explain any reproducibility differences.
- [ ] The portfolio links verified setup, real results, uncertainty, annotated examples, and clear limitations.
- [ ] You independently modify and verify a core component and can explain the system, experiments, metrics, and conclusions without the agent.

## Explain without the agent

1. Which parts of the project can you now implement or diagnose without generated code?
2. What evidence would change your main conclusion, and how would you design that next experiment?
3. Can another person reproduce a selected comparison using only the repository and referenced artifacts?

## Suggested request to the coding agent

> Help reproduce the project in a fresh environment, verify artifact/document consistency, and review my independent core-code exercise without taking over the initial attempt.

## Ready for the next week

The project is complete when both the software and independent-learning criteria pass. Leave any unmet criterion open; a reproducible negative adaptation result is still a valid outcome.

