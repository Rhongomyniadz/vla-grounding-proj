# Week 11: Analyze results and write your own interpretation

[English](week-11.en.md) | [简体中文](week-11.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Goal:** Explain the evidence, uncertainty, and failure modes before the agent helps polish the report.

**Start when:** Week 10 provides a frozen, audited final result collection with complete coverage or explicit limitations.

Time budget: 12 active hours across five sessions; one hour is independent work with the agent closed. Computer runtime is additional.

## Prepare and learn

- Revisit your early predictions, the fixed metric definitions, and the distinction between eventual goal success and first-object selection.
- Review the bootstrap grouping and the limits of four tasks, one training seed per arm, benchmark overlap, and a sampled robustness panel.
- Inspect the result schema and artifact references so every report claim can point to measured evidence.

## Work sessions

### 1. Write an interpretation before polishing (2 hours)

- [ ] You: inspect the aggregate tables and write your first explanation of canonical, paraphrase, changed-target, empty-instruction, and robustness outcomes.
- [ ] Identify evidence supporting and opposing the intervention hypothesis, including any manipulation regressions.
- [ ] Separate measured findings from causal hypotheses and unknowns; do not ask the agent to invent a positive narrative.

### 2. Generate and verify the final figures (3 hours)

- [ ] Agent: produce per-task/condition success plots, paired target-selection summaries, robustness comparisons, uncertainty intervals, and compute-cost tables.
- [ ] You: manually trace at least one headline figure and one policy difference to the underlying paired episode records.
- [ ] Verify labels disclose sample counts, backend identity, development versus final status, and the conditional interpretation of intervals.

### 3. Review failures with a declared sampling method (3 hours)

- [ ] Choose twelve real episodes for detailed review, four per policy, using a recorded sampling rule that covers available conditions and outcomes.
- [ ] You: inspect videos with state/action/predicate traces and classify failures using the agreed taxonomy; mark uncertain causes as unknown.
- [ ] Use these cases to illustrate mechanisms, not to estimate population failure frequencies or replace the complete quantitative results.

### 4. Defend one conclusion independently, then review (2 hours)

- [ ] For the first hour, close the agent and defend one claim with a table, an interval, and a video/trace example.
- [ ] Write the strongest alternative explanation and state what additional experiment would distinguish it.
- [ ] In the second hour, ask the agent to challenge the claim, check unsupported language, and help tighten the explanation.

### 5. Complete the report and bilingual consistency (2 hours)

- [ ] Write the report covering question, method references, results, uncertainty, failure examples, limitations, and the next experiment.
- [ ] Agent: assist with English/Chinese report consistency, captions, artifact links, and editing after your first interpretation is recorded.
- [ ] Keep architecture/implementation document pairs synchronized if the verified system differs from the plan; do not launch test-driven retuning as part of the original held-out claim.

## Evidence and completion checks

- [ ] Every headline claim traces to measured results, with uncertainty and negative evidence included.
- [ ] Reviewed examples use a declared selection rule, retain unknown causes, and do not substitute for full-panel metrics.
- [ ] The learner can defend the interpretation; the report and any updated architectural documentation are consistent across languages.

## Explain without the agent

1. What evidence distinguishes robustness to wording from responsiveness to a changed goal?
2. If paraphrase adaptation helps one condition but harms canonical success, how should the report describe that tradeoff?
3. Which limitations would require more tasks or training seeds rather than more repeats of the same case?

## Suggested request to the coding agent

> Generate plots from the frozen records, critique my first interpretation, identify unsupported causal claims, and help edit consistent bilingual reporting.

## Ready for the next week

Proceed when results, figures, failure examples, and conclusions are internally consistent and their limits can be explained without the agent.

