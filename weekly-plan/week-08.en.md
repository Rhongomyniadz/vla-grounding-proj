# Week 8: Demonstration data and a verified LoRA smoke run

[English](week-08.en.md) | [简体中文](week-08.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Goal:** Prepare a fair language-only adaptation dataset and verify the training/checkpoint lifecycle before full runs.

**Start when:** Both evaluation backends work, development analysis is valid, and training/validation/final prompt families are already frozen.

Time budget: 12 active hours across five sessions; one hour is independent work with the agent closed. Computer runtime is additional.

## Prepare and learn

- Read the implementation plan's dataset splits, normalization contract, and shared LoRA recipe; treat it as the parameter source of truth.
- Inspect a real demonstration's images, states, actions, timestamps, episode identity, and task instruction using LeRobot's loader.
- Learn behavior cloning/action prediction, frozen backbone versus trainable adapter parameters, and why changed-target instructions cannot relabel unchanged demonstrations.

## Work sessions

### 1. Inspect data and define splits (2 hours)

- [ ] You: inspect examples from all four primary tasks and explain how state/image/action samples align over time.
- [ ] Use the pinned dataset revision to create the agreed task-stratified, complete-episode splits and preserve original episode identities.
- [ ] Verify no demonstration appears in multiple splits; distinguish demonstration holdouts from the separate simulator-state evaluation holdouts.

### 2. Prepare the two training copies (3 hours)

- [ ] Agent: create project-owned copies from one training split and use supported LeRobot task-relabeling tools only on those copies.
- [ ] You: assign the canonical and four training paraphrase templates approximately evenly within each task while preserving one instruction per episode.
- [ ] Verify the two arms share numeric observations, actions, frames, order, and checkpoint normalization; no alternative-object instruction may be paired with the wrong demonstration.

### 3. Verify trainable parameters and checkpoint behavior (3 hours)

- [ ] Agent: configure the pinned upstream trainer and LoRA support using the shared recipe, BF16 interface, explicit local outputs, and uploads disabled.
- [ ] You: inspect the trainable parameter list and confirm the intended backbone remains frozen; explain what the learning objective compares.
- [ ] Run the planned 100-update smoke check, save and reload a checkpoint, and execute a development rollout with the restored processors.

### 4. Audit a training example independently, then review (2 hours)

- [ ] For the first hour, close the agent and trace one sample from its source episode through relabeling, tokenization, normalization, and action target.
- [ ] Verify that its instruction describes the recorded action and that it belongs to the intended split.
- [ ] In the second hour, review the trace and any smoke-run failure with the agent, addressing the root cause before full training.

### 5. Freeze the shared training recipe (2 hours)

- [ ] Save split maps, source revisions, prompt assignments, copy-comparison evidence, normalization identities, and measured update/memory cost.
- [ ] If a resource or numerical issue requires changing the recipe, explicitly apply the same revision to both arms before either full run.
- [ ] Estimate the two full runs and checkpoint-selection evaluation cost from measurements; keep all final-test cases untouched.

## Evidence and completion checks

- [ ] Source-to-split mappings are disjoint by episode and both training arms differ only in intended language labels.
- [ ] Trainable modules, frozen parameters, normalization, and sample/action alignment have been inspected.
- [ ] A real 100-update checkpoint saves, reloads, and runs; the shared recipe and measured resource budget are frozen.

## Explain without the agent

1. Why would changing the target object in a demonstration's text usually invalidate its action labels?
2. How can changing normalization confound a comparison that is intended to change only language?
3. What does a lower training loss demonstrate, and why does it not establish better goal selection?

## Suggested request to the coding agent

> Prepare the paired dataset copies and upstream LoRA smoke run, expose trainable parameters and sample traces, and have me verify the labels and intervention rationale.

## Ready for the next week

Begin full training only after data equivalence, parameter selection, finite updates, checkpoint reload, and a real post-reload rollout are verified.

