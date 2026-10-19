# Week 6: Metrics, uncertainty, and a development baseline

[English](week-06.en.md) | [简体中文](week-06.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Goal:** Implement the core metrics yourself and explain what the development results do and do not establish.

**Start when:** Week 5 provides valid language cases and verified requested-goal scoring, with held-out final cases still unused.

Time budget: 12 active hours across five sessions; one hour is independent work with the agent closed. Computer runtime is additional.

## Prepare and learn

- Read the implementation plan's metric definitions and distinguish paired outcomes from independent success-rate comparisons.
- Learn percentage-point differences, equal task weighting, uncertainty conditional on selected tasks, and bootstrap resampling units.
- Inspect real episode records, including timeouts, simultaneous goals, and infrastructure errors, before choosing summary logic.

## Work sessions

### 1. Calculate a real example by hand (2 hours)

- [ ] You: select a small completed development panel and manually count successes, first-object choices, paired correctness, and per-task coverage.
- [ ] Calculate the canonical success rate and the difference for a development paraphrase; explain the denominator and sign.
- [ ] Treat execution exceptions as incomplete work, and do not present a partial panel as a completed benchmark result.

### 2. Implement core metric functions (3 hours)

- [ ] You: write pure functions for per-condition success, paraphrase gaps, first-object selection, paired correctness, and policy differences.
- [ ] Check the functions against your manual calculations using saved real records; define simultaneous-goal handling consistently with the scorer.
- [ ] Agent: review typing, grouping, missing-case errors, and equal task weighting; do not replace the first implementation.

### 3. Add uncertainty estimates and useful plots (3 hours)

- [ ] With agent guidance, implement the planned grouped bootstrap with 2,000 resamples while preserving paired conditions within each initial state.
- [ ] Agent: add plots and exports using your metric functions, with clear development-only labels, task sample counts, coverage, and interval definitions.
- [ ] Use training/validation wording and development states for these checks; do not consume final held-out templates or states to debug analysis.

### 4. Audit one metric independently, then review (2 hours)

- [ ] For the first hour, close the agent and trace one plotted value from raw real episode records through grouping to the final number.
- [ ] Explain what would change if paraphrase outcomes for the same initial state were resampled independently.
- [ ] In the second hour, ask the agent to challenge your calculation and uncertainty interpretation, then correct the implementation if needed.

### 5. Write a provisional interpretation (2 hours)

- [ ] You: describe the development findings, uncertainty, and alternative explanations before asking the agent to critique them.
- [ ] Separate evidence about manipulation skill, language invariance, target selection, and empty-instruction behavior.
- [ ] Freeze analysis definitions and expected final outputs so later checkpoint results cannot redefine the main metric.

## Evidence and completion checks

- [ ] Learner-written metrics agree with hand calculations on real development records.
- [ ] Bootstrap grouping preserves pairs and task weighting; plots disclose sample counts and incomplete coverage.
- [ ] A provisional interpretation is explicitly developmental and final held-out cases remain unused.

## Explain without the agent

1. Why should two conditions on the same initial state remain paired during bootstrap resampling?
2. What does a negative paraphrase gap mean, and what does it not explain?
3. Why does this study's uncertainty not measure generalization across all tasks or training seeds?

## Suggested request to the coding agent

> Review my metric functions against real records, help implement the grouped bootstrap and plots, and challenge my interpretation before editing it.

## Ready for the next week

Proceed when every reported development number can be traced to saved records and you can explain the unit of resampling without the agent.

