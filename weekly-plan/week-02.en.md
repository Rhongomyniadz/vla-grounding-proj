# Week 2: Write and understand one complete robot episode

[English](week-02.en.md) | [简体中文](week-02.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Goal:** Implement the first outer inference loop yourself and trace a complete simulated episode.

**Start when:** Week 1 checks pass, the checkpoint/processors load, and the simulator and policy connectors are available.

Time budget: 12 active hours across five sessions; one hour is independent work with the agent closed. Computer runtime is additional.

## Prepare and learn

- Inspect the pinned policy's reset and action-selection methods and the simulator's reset, step, success, and termination behavior.
- Learn the difference between normalized model actions, decoded control actions, and the controller's coordinate conventions.
- Read the action-queue implementation: determine when a new chunk is generated and when an existing action is reused.

## Work sessions

### 1. Specify one episode before coding (2 hours)

- [ ] You: write pseudocode covering environment reset, policy reset, observation preparation, instruction injection, action selection, stepping, scoring, and closing.
- [ ] Inspect a real step result and distinguish task success, episode termination, timeout, and an execution exception.
- [ ] Agent: review the pseudocode and connector contracts without providing the completed loop.

### 2. Implement your first episode loop (3 hours)

- [ ] You: implement the loop using established LeRobot calls and the agreed checkpoint execution settings; keep the first version single-task and single-episode.
- [ ] Trace one iteration with actual tensors, including the instruction that reaches tokenization and the seven-dimensional action sent to the environment.
- [ ] Run a development episode with an explicit step limit and verify that policy state and queued actions are reset at its start.

### 3. Add evidence and resolve integration failures (3 hours)

- [ ] Agent: integrate video and trajectory writing around your loop, preserving raw observations, predictions, executed actions, and completion information.
- [ ] You: inspect action decoding, image orientation, feature mapping, state construction, and relative control if behavior is unexpectedly unsuccessful.
- [ ] Save three development rollouts for the pilot task and classify observed outcomes honestly; do not assume a successful video must already exist.

### 4. Change the loop independently, then review (2 hours)

- [ ] For the first hour, close the agent and add inference-call and executed-action counters to your loop.
- [ ] Predict why the counters differ under chunked execution, then verify the explanation using a real trace.
- [ ] In the second hour, review your change with the agent and simplify it without hiding the data flow.

### 5. Explain the episode and prepare reset experiments (2 hours)

- [ ] Replay one video alongside its trace and explain the path from a specific instruction through one predicted chunk to motion.
- [ ] Confirm resources close after normal completion and after a real development failure; preserve the useful error context.
- [ ] Identify which simulator state, RNG state, and policy cache must be controlled for Week 3 comparisons.

## Evidence and completion checks

- [ ] Your own outer loop completes a bounded real episode and saves a playable video and inspectable trajectory.
- [ ] Success, timeout, and infrastructure failure remain distinguishable; a failed grasp is not relabeled as an exception.
- [ ] You can explain action caching and point to where preprocessing and decoding happen.

## Explain without the agent

1. What changes when a queued action is used instead of generating a new chunk?
2. Which state must be reset between episodes, and what could happen if the policy queue is retained?
3. Why could correct tensor shapes coexist with incorrect physical control?

## Suggested request to the coding agent

> Review my episode-loop pseudocode and implementation, supply missing connector or recording utilities, and explain integration errors without replacing my first attempt.

## Ready for the next week

Proceed when the bounded episode loop and its trace are reliable. Task failures can be investigated, but unexplained interface errors must be resolved first.

