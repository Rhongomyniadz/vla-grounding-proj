# Week 3: Reproducible resets and an action-horizon exercise

[English](week-03.en.md) | [简体中文](week-03.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Goal:** Establish matched development rollouts and understand the effect of executing more actions between observations.

**Start when:** Week 2 provides a working learner-written episode loop and saved observations, actions, and outcomes.

Time budget: 12 active hours across five sessions; one hour is independent work with the agent closed. Computer runtime is additional.

## Prepare and learn

- Read how the pinned environment restores initial states and settles physics after reset; distinguish reset seeds from explicit simulator state.
- Inspect all policy state that persists across calls, including action queues and model caches.
- Learn why stochastic action sampling, settling steps, and rendering settings can affect repeatability.

## Work sessions

### 1. Specify a reproducible development case (2 hours)

- [ ] You: identify a small set of development initial states and define the instruction, policy seed, settling behavior, horizon, and step limit for each case.
- [ ] Agent: expose supported state restoration and capture the restored state and observation fingerprints.
- [ ] Write down which quantities should match exactly and which require a justified tolerance before running comparisons.

### 2. Verify restoration and policy reset (3 hours)

- [ ] Run the same development case twice with explicit simulator state restoration and policy reset; compare starting state, observations, first prediction, and outcome.
- [ ] Interleave an unrelated development episode, then restore the original case again to detect state leaking between episodes.
- [ ] If results differ, isolate simulator, policy-RNG, action-cache, preprocessing, and rendering causes before treating the pair as matched.

### 3. Run the horizon comparison (3 hours)

- [ ] You: choose the checkpoint execution horizon and one shorter supported horizon, holding scene, instruction, seed, and rollout limit fixed.
- [ ] Predict the effect on replanning frequency and behavior, then run a small matched development panel for both settings.
- [ ] Measure inference calls, executed actions, latency, outcome, and visible corrections; retain the main study's original horizon.

### 4. Diagnose one trace independently, then review (2 hours)

- [ ] For the first hour, close the agent and use saved traces to investigate one repeatability difference or one horizon-dependent behavior.
- [ ] Write a specific hypothesis, identify supporting observations, and perform one controlled development check.
- [ ] In the second hour, ask the agent to challenge the diagnosis and verify any code correction against the matched cases.

### 5. Prepare the runner contract (2 hours)

- [ ] Save the reset procedure, tolerance rationale, development-case identities, and horizon-exercise results in the existing notebook and code docstrings.
- [ ] List the case identifiers and runtime metadata that Week 4's manifest must preserve.
- [ ] Ensure exploratory horizon changes and development state choices cannot silently enter the frozen evaluation configuration.

## Evidence and completion checks

- [ ] Repeated and interleaved restoration checks produce explainable matching states and observations.
- [ ] A small matched horizon comparison includes a prediction, measured counters, outcomes, and an interpretation.
- [ ] The main checkpoint horizon remains explicit, and episode state cannot leak through retained policy queues.

## Explain without the agent

1. Why does sharing an environment seed not guarantee an identical initial scene?
2. How can a long action execution horizon reduce the opportunity to correct a mistaken grasp?
3. Which mismatch would you investigate first if starting states match but the first predicted actions differ?

## Suggested request to the coding agent

> Help expose explicit simulator restoration and policy-reset APIs, review my repeatability checks, and keep the horizon comparison separate from the main experiment.

## Ready for the next week

Proceed when paired development cases can be restored reliably and unexplained differences have been resolved or characterized before analysis.

