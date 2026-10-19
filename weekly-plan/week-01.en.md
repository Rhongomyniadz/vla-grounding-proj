# Week 1: Environment and the perception-to-action pipeline

[English](week-01.en.md) | [简体中文](week-01.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Goal:** Verify the RTX 5080/WSL2 runtime and explain what the robot observes and what the policy predicts.

**Start when:** The planning documents are available and you can access the separate RTX 5080 machine. No project runtime is assumed to exist.

Time budget: 12 active hours across five sessions; one hour is independent work with the agent closed. Computer runtime is additional.

## Prepare and learn

- Read the implementation plan's environment and perception-to-action sections, then inspect the pinned LeRobot installation and LIBERO interfaces.
- Learn observation, proprioception, end-effector pose, gripper command, relative control, action chunk, and model checkpoint.
- Sketch the path from two camera images, robot state, and instruction to an executed action. Mark preprocessing and action decoding.

## Work sessions

### 1. Inventory the target machine and predict the data flow (2 hours)

- [ ] You: record the target GPU, available memory/storage, Windows/WSL/Ubuntu versions, and where Linux project files will live.
- [ ] You: draw the observation-to-action sketch before asking the agent to explain it; identify the concepts you cannot yet explain.
- [ ] Agent: inspect the pinned upstream setup requirements and propose the smallest simulation-only environment configuration.

### 2. Build and verify the base environment (3 hours)

- [ ] Agent: implement reproducible dependency setup, CUDA checks, and headless rendering checks using the agreed versions and supported interfaces.
- [ ] You: run the checks inside WSL, inspect both camera images, and confirm that the reported device is the target RTX 5080.
- [ ] For any failure, save the exact command and error, identify the failing layer, and verify the root-cause correction before continuing.

### 3. Load the checkpoint and inspect a real prediction (3 hours)

- [ ] Agent: expose checkpoint loading and observation preprocessing through small connectors; do not implement your full outer episode loop.
- [ ] You: inspect raw and processed image/state shapes, tokenizer output and mask, feature-name mapping, normalizers, predicted chunk, and executed-action dimensions.
- [ ] Use existing upstream smoke/evaluation support to obtain a prediction, step the simulator, and save a short playable video. Record resolved artifact revisions.

### 4. Work independently, then review (2 hours)

- [ ] For the first hour, close the agent and write a small inspection function that reports shapes, dtypes, ranges, and finite-value checks for real observations.
- [ ] Use your inspection output to trace which representation changes at preprocessing and which quantities describe the robot rather than the scene.
- [ ] In the second hour, ask the agent to review your explanation and helper; correct one misunderstanding and rerun the relevant check.

### 5. Collect evidence and prepare the next task (2 hours)

- [ ] Save environment-check output, both camera examples, resolved versions, checkpoint identity, and the smoke video as development artifacts.
- [ ] Document only commands that actually worked; record unresolved compatibility questions instead of inventing a complete quickstart.
- [ ] Prepare the narrow Week 2 request: provide connectors and video support while leaving the episode loop for your implementation.

## Evidence and completion checks

- [ ] CUDA execution, both camera renders, checkpoint loading, finite predictions, simulator stepping, and video playback have been verified.
- [ ] You can point to actual image, state, language, chunk, and action representations in the saved example.
- [ ] The environment configuration and immutable artifact references can be recovered; failures are either resolved or explicitly outstanding.

## Explain without the agent

1. How do robot state and camera observations provide different information?
2. Where does the instruction enter the pipeline, and which preprocessing could accidentally remove important words?
3. What does one action control, and why does seeing a valid prediction not yet prove task success?

## Suggested request to the coding agent

> Implement the environment checker and minimal LeRobot connectors, explain their inputs and outputs, and leave the full single-episode loop for me.

## Ready for the next week

Begin Week 2 when the environment can produce and execute a real policy action and save its observations. Resolve environment failures before debugging task behavior.

