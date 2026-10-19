# Week 7: Camera and object-layout robustness

[English](week-07.en.md) | [简体中文](week-07.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Goal:** Build an isolated LIBERO-plus evaluation panel and understand what changes in each perturbation.

**Start when:** The base-language development pipeline and metrics work, and the base environment's dependencies and assets are recorded.

Time budget: 12 active hours across five sessions; one hour is independent work with the agent closed. Computer runtime is additional.

## Prepare and learn

- Read the implementation plan's robustness protocol and the pinned LIBERO-plus installation, task mapping, and asset-loading code.
- Distinguish camera-only changes, changed physical layouts, and differences introduced by a separate simulator backend.
- Inspect how each environment resolves package imports, configuration, and assets so installing the fork cannot redirect the base setup.

## Work sessions

### 1. Specify backend isolation and comparison rules (2 hours)

- [ ] Agent: prepare a separate LIBERO-plus environment with pinned dependencies, code, and assets, using supported configuration mechanisms.
- [ ] You: verify each environment imports the intended package and resolves the intended assets and initial-state files.
- [ ] Write down which camera cases can share physical states and why layout comparisons require their own explicit variant states.

### 2. Create and inspect the variant manifest (3 hours)

- [ ] Agent: expose category/task metadata and resolve runtime IDs by actual suite names rather than assuming metadata IDs equal indices.
- [ ] You: inspect representative camera and layout cases and verify their intended target and destination.
- [ ] Freeze ten variants per task per dimension with seed 42 and explicit state/seed references, without selecting by observed policy success.

### 3. Verify clean anchors and development pilots (3 hours)

- [ ] Construct the planned clean anchors inside the robustness backend from pinned original task definitions and states.
- [ ] Run separate development pilots for both perturbation dimensions; keep these pilot cases outside the final held-out panel.
- [ ] Compare camera images, physical state, observation mapping, scoring, and control settings; investigate unexpected backend differences before pooling anything.

### 4. Diagnose a perturbation independently, then review (2 hours)

- [ ] For the first hour, close the agent and compare one development perturbation against its appropriate clean reference using states, images, actions, and video.
- [ ] Propose why it changes behavior and identify any alternative explanation caused by the backend or scorer.
- [ ] In the second hour, review that reasoning and perform one controlled development check with the agent.

### 5. Audit the final robustness panel (2 hours)

- [ ] Verify the frozen panel contains eighty perturbed cases and eighty clean-anchor cases per policy, with recoverable mappings and no duplicates.
- [ ] Confirm base-LIBERO development still works after setting up the fork and that labels preserve backend identity.
- [ ] Prepare coverage and per-dimension summaries without reporting the development pilot as the complete LIBERO-plus benchmark.

## Evidence and completion checks

- [ ] Base and robustness environments resolve their intended code, configuration, and assets independently.
- [ ] Camera and layout pilots have valid observations and goal scoring; backend differences are explainable.
- [ ] The final variant and anchor manifest is frozen independently of performance and has not been used for tuning.

## Explain without the agent

1. Why does a layout perturbation not automatically support an exactly matched clean-state comparison?
2. What could go wrong if the two Python environments resolve the same unintended asset configuration?
3. Why must the robustness panel include clean anchors within its own backend?

## Suggested request to the coding agent

> Implement the isolated LIBERO-plus connector and variant manifest support, verify asset/configuration resolution, and let me inspect and interpret the development perturbations.

## Ready for the next week

Proceed when both backends are reliable, final robustness cases are frozen, and you can identify the physical and visual changes in pilot examples.

