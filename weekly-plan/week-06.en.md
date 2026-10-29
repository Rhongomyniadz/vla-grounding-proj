# Week 6: Metrics, uncertainty, and a development baseline

[English](week-06.en.md) | [简体中文](week-06.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Documentation:** Update the [bilingual code guide](../doc/CODE_GUIDE.en.md) with this week's design rationale, implemented structures and verification evidence.

**Goal:** Implement the core metrics and explain what the development results do and do not establish.

**Start authoring when:** The result schema and metric definitions are agreed; you may write pure metric/plot code before records return, but real-data reconciliation must wait.

**Run-computer prerequisite:** Week 5 provides valid language cases and verified requested-goal scoring, with held-out final cases still unused.

Planning estimate: 12 active hours across five sessions, including evidence review and documentation. GPU runtime is additional and must be measured.

## Execution locations

Use the [shared handoff procedure](../doc/ENVIRONMENT.en.md#handoff-for-every-execution-visit); the session locations below govern the detailed steps.

1. **Prepare on the coding computer:** Make the metric implementation, grouped bootstrap and plot pipeline using declared portable dependencies; leave values unreported until real records exist.
2. **Execute on the run computer:** Use Week 5 verified development records; generate any missing development coverage on the run computer before numerical verification.
3. **Return for review:** Return all manifest/result rows needed for denominators and pairing, including incomplete-run logs and first-object ties. Reconcile hand calculations and produce development plots on this computer.

Without target access, keep real-run checks pending, record the specific access or setup blocker, prepare the exact handoff and continue authoring that does not depend on target evidence.

## What to read and understand

Read in this order. Pending source is listed explicitly. Before completing this milestone, replace planned-code descriptions with exact implemented file/symbol links and add the relevant evidence reference.

| Order | Required reading |
| --- | --- |
| 1. Documents | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md#e-measure-and-interpret-results): all metric definitions, task weighting, grouped bootstrap and interpretation limits. [Code guide](../doc/CODE_GUIDE.en.md): planned analysis and evidence contracts. |
| 2. Current code | [evidence.py](../src/vla_grounding/evidence.py): serialized result boundary; revisit the actual result/case/scoring modules delivered in Weeks 4–5. |
| 3. Follow the calls | Per-task aggregation, paraphrase gap, first-object/paired correctness, policy difference and missing-coverage validation functions: planned; read their actual modules once implemented. |
| 4. Milestone code/evidence | Grouped bootstrap and figure/export functions: planned; trace raw rows through group keys to one plotted number. |

Understanding goals:

- Derive denominators and signs for success, paraphrase gap and intervention gain from a small real-record table.
- Explain equal task weighting, strict first selection versus eventual success and explicit simultaneous-goal handling.
- Explain why all conditions/policies for an initial state remain together in bootstrap and why intervals do not cover new tasks or training seeds.

## Prepare and learn

- Read the implementation plan's metric definitions and distinguish paired outcomes from independent success-rate comparisons.
- Learn percentage-point differences, equal task weighting, uncertainty conditional on selected tasks, and bootstrap resampling units.
- Inspect real episode records, including timeouts, simultaneous goals, and infrastructure errors, before choosing summary logic.

## Reading route and expected understanding

- Use the [metric definitions](../doc/IMPLEMENTATION_PLAN.en.md#e-measure-and-interpret-results) as the source of truth and inspect the actual result records they consume.
- Read your Week 5 scorer and case builder before implementing aggregation. Identify timeout, exception, first-object tie, and eventual-success representations.
- Review the [final budget](../doc/IMPLEMENTATION_PLAN.en.md#final-evaluation-budget) only to understand coverage; this week's computations use development cases, not the final panel.

## Implementation tasks

The items below define the code and documentation deliverables for this week. Existing source should be completed or extended; future components remain planned until implemented. Keep experimental parameters authoritative in the linked implementation plan.

1. **Validated result loading and coverage.** Read saved development manifests/results into typed records without importing the simulator. Reject duplicate IDs, missing required pairs, mixed backend identities and unexplained missing coverage before presenting completed-panel statistics. Preserve timeout failures and incomplete infrastructure execution as different states.
2. **Core pure metrics.** Implement task/condition/policy success, paraphrase gaps, changed-target success, first-object selection, strict paired correctness and policy/intervention differences using the authoritative definitions. Return new summary records without modifying input rows; retain simultaneous first-goal ties rather than assigning an arbitrary object.
3. **Arithmetic reconciliation and task weights.** Calculate a small real-record example independently from the aggregation implementation, showing numerators, denominators, pair membership and difference signs. Reconcile the functions against it and aggregate with equal task weight instead of allowing uneven completion counts to change the intended statistic.
4. **Grouped uncertainty.** Implement reproducible bootstrap resampling at the initial-state-group level within each task, carrying all linked language conditions and policy outcomes together. Use the interval/resample specification from the implementation plan and save seed, grouping unit, metric identity and task weighting with each summary.
5. **Figures and exports.** Generate plots and machine-readable tables directly from validated summaries, including counts, coverage, interval definitions and development-only labels. Resolve artifacts relative to the copied run root so analysis can run on Windows with declared dependencies. Keep absent adapted-policy results unreported.
6. **Analysis command and documentation.** Expose explicit manifest/result/output inputs, run analysis on real returned records and trace one plotted number back to source rows. Document metric equations, pair/tie handling, bootstrap control flow, error conditions and the provisional interpretation with alternative explanations in the existing paired documentation.

## Work sessions

### 1. Calculate a real example by hand (2 hours)

**Location:** Coding computer: hand-calculate from real returned Week 5 records; defer this session's evidence if they are unavailable.

**Detailed procedure**

1. Choose a small complete development subset. Create a hand table with task, state, condition, outcome, first object, and paired-case identity.

2. Count planned versus complete cases before computing rates. Keep simulator task failure, timeout, and incomplete infrastructure execution distinguishable.

3. Compute each condition's successes divided by its valid completed cases for this complete subset. Calculate task-level rates first, then apply equal task weighting.

4. For each paired state, compare canonical and paraphrase outcomes, and separately check first-object correctness for original versus changed goal. Write down the sign of each difference.

**Expected output:** A hand-calculated table that can serve as the explanation for the first real metric output.

**If this does not work:** If you cannot reconstruct a denominator from saved records, fix missing/duplicate identities before writing a plotting function.

**Session completion checklist**

- [ ] select a small completed development panel and manually count successes, first-object choices, paired correctness, and per-task coverage.
- [ ] Calculate the canonical success rate and the difference for a development paraphrase; explain the denominator and sign.
- [ ] Treat execution exceptions as incomplete work, and do not present a partial panel as a completed benchmark result.

### 2. Implement core metric functions (3 hours)

**Location:** Coding computer: implement pure metrics and reconcile against the real hand table after it exists.

**Detailed procedure**

1. Implement pure aggregation functions using explicit input records. Return computed summaries without modifying the original records.

2. Implement the agreed relationships: paraphrase gap is paraphrase success minus canonical success; intervention gain compares adapted and control policies on matching cases.

3. Define pair correctness using the requested first object in both trials, keeping simultaneous first-goal ties explicit. Do not substitute eventual success for strict first selection.

4. Compare your outputs against the hand table. Missing pairs, duplicate results, or mixed backend identities must produce clear errors rather than silently changing denominators.

**Expected output:** Correct metric functions and a real-record reconciliation you can explain line by line.

**If this does not work:** If the global average changes only because a task has more completed episodes, check task weighting and incomplete coverage.

**Session completion checklist**

- [ ] write pure functions for per-condition success, paraphrase gaps, first-object selection, paired correctness, and policy differences.
- [ ] Check the functions against your manual calculations using saved real records; define simultaneous-goal handling consistently with the scorer.
- [ ] review typing, grouping, missing-case errors, and equal task weighting; implement and verify the complete metric pipeline.

### 3. Add uncertainty estimates and useful plots (3 hours)

**Location:** Coding computer: implement and run bootstrap/plots with declared analysis dependencies using the returned complete development records.

**Detailed procedure**

1. Group real development rows by task and initial-state identity. Keep all language conditions and compared policy outcomes for a state in the same group.

2. Within each task, bootstrap the state groups with replacement and recompute the same paired statistic; use the planned number of resamples.

3. Take the interval from the resampled statistic distribution and record the resampling seed, unit, task weighting, and metric definition.

4. Build plots from your summaries, showing sample counts and development labels. For empty-instruction diagnostics, retain the same declared original-goal scoring.

**Expected output:** An uncertainty calculation with a named sampling unit and a plot traceable to the same real records.

**If this does not work:** Resampling individual paraphrases independently breaks their shared-state dependence and is not the planned paired procedure.

**Session completion checklist**

- [ ] Implement the planned grouped bootstrap with 2,000 resamples while preserving paired conditions within each initial state.
- [ ] add plots and exports using your metric functions, with clear development-only labels, task sample counts, coverage, and interval definitions.
- [ ] Use training/validation wording and development states for these checks; do not consume final held-out templates or states to debug analysis.

### 4. Audit one metric and document the findings (2 hours)

**Location:** Coding computer: audit real records, grouping and plotted arithmetic; request target execution only if underlying evidence is missing or invalid.

**Detailed procedure**

1. Select one plotted rate and one paired difference. Find every underlying result and reproduce the arithmetic.

2. Trace one bootstrap draw conceptually: identify repeated state groups and show which associated conditions must travel together.

3. Explain why this interval is conditional on the selected tasks and trained weights, rather than evidence across all tasks or new training seeds.

4. Review the evidence and strongest alternative explanation, correct any identified root cause, rerun affected checks and document the reasoning in the relevant bilingual `doc/` pair.

**Expected output:** A defensible explanation of one result and its uncertainty with documented arithmetic and grouping evidence.

**If this does not work:** A narrow interval cannot compensate for an incorrect scorer or a biased selection of tasks.

**Session completion checklist**

- [ ] trace one plotted value from raw real episode records through grouping to the final number.
- [ ] Explain what would change if paraphrase outcomes for the same initial state were resampled independently.
- [ ] verify the reasoning and any correction, rerun affected checks, and update the bilingual design/code explanations with evidence references.

### 5. Write a provisional interpretation (2 hours)

**Location:** Coding computer: write the development interpretation and freeze metric definitions after real-record checks.

**Detailed procedure**

1. Write a short development-only finding in the relevant paired document in `doc/` with the relevant table, interval, and at least one competing explanation.

2. Separate language invariance, responsiveness to target changes, manipulation competence, and behavior without a task instruction.

3. Freeze metric definitions, aggregation rules, and intended figure labels before seeing final adaptation results.

4. List the extra comparison outputs that will become possible when the two trained policies exist, without fabricating their values now.

**Expected output:** A cautious provisional interpretation and a fixed analysis contract for later results.

**If this does not work:** Do not revise the primary metric merely because an exploratory number looks less favorable than another.

**Session completion checklist**

- [ ] document the development findings, uncertainty and alternative explanations, then check each claim against the evidence.
- [ ] Separate evidence about manipulation skill, language invariance, target selection, and empty-instruction behavior.
- [ ] Freeze analysis definitions and expected final outputs so later checkpoint results cannot redefine the main metric.

## Evidence and completion checks

- [ ] Documentation ready: the paired design/code guide covers all implemented structures, rationale, interfaces and verification status.
- [ ] Authoring ready: this week's source/configuration and applicable local checks are included in the identified handoff.
- [ ] Target verified: the required real target evidence has returned and been reviewed against that handoff.
- [ ] Implemented metrics agree with hand calculations on real development records.
- [ ] Bootstrap grouping preserves pairs and task weighting; plots disclose sample counts and incomplete coverage.
- [ ] A provisional interpretation is explicitly developmental and final held-out cases remain unused.

## Optional review questions

1. Why should two conditions on the same initial state remain paired during bootstrap resampling?
2. What does a negative paraphrase gap mean, and what does it not explain?
3. Why does this study's uncertainty not measure generalization across all tasks or training seeds?

## Delivery summary

> Implement all metric functions, verify arithmetic against real records, add grouped bootstrap and plots, and document equations, grouping, uncertainty and the development interpretation.

## Ready for the next week

Independent authoring for later milestones may continue from agreed interfaces. The following gate applies to dependent execution and result claims.

Proceed when every reported development number can be traced to saved records and the code guide explains the unit of resampling.

