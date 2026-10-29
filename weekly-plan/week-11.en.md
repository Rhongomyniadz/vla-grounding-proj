# Week 11: Analyze results and write the evidence-based interpretation

[English](week-11.en.md) | [简体中文](week-11.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Documentation:** Update the [bilingual code guide](../doc/CODE_GUIDE.en.md) with this week's design rationale, implemented structures and verification evidence.

**Goal:** Analyze and document the evidence, uncertainty and failure modes, and deliver the complete bilingual report.

**Start authoring when:** The report structure and analysis contract are agreed; final numbers, figures and interpretation require Week 10's audited returned evidence.

**Run-computer prerequisite:** Week 10 provides a frozen, audited final result collection with complete coverage or explicit limitations.

Planning estimate: 12 active hours across five sessions, including evidence review and documentation. GPU runtime is additional and must be measured.

## Execution locations

Use the [shared handoff procedure](../doc/ENVIRONMENT.en.md#handoff-for-every-execution-visit); the session locations below govern the detailed steps.

1. **Prepare on the coding computer:** Prepare the report outline and analysis entry points; once real final records return, write and document the interpretation and generate/check figures locally with declared dependencies.
2. **Execute on the run computer:** Use the frozen target result collection. Retrieve referenced artifacts needed for review; new execution is needed only to resolve an actual evidence/correctness gap.
3. **Return for review:** Bring back all final manifest/result/coverage records, compute logs and the twelve selected real episode bundles with hashes and run-relative links; retain target provenance in the report.

Without target access, keep real-run checks pending, record the specific access or setup blocker, prepare the exact handoff and continue authoring that does not depend on target evidence.

## What to read and understand

Read in this order. Pending source is listed explicitly. Before completing this milestone, replace planned-code descriptions with exact implemented file/symbol links and add the relevant evidence reference.

| Order | Required reading |
| --- | --- |
| 1. Documents | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md#e-measure-and-interpret-results): metrics, intervals, taxonomy and inference limits. [Code guide](../doc/CODE_GUIDE.en.md): delivered analysis and artifact-path structure. |
| 2. Current code | [evidence.py](../src/vla_grounding/evidence.py) and the actual result reader, grouped metrics/bootstrap, plotting/export and coverage modules delivered earlier. |
| 3. Follow the calls | Report/figure generation and illustrative-episode selection/annotation functions: planned; read their real inputs and transformations after implementation. |
| 4. Milestone code/evidence | Read the bilingual results report once it exists in `doc/`, its frozen manifest/coverage references and twelve sampled episode bundles. Do not treat a report path as implemented before it exists. |

Understanding goals:

- Trace one headline number and one policy difference to paired rows, denominator, interval and plot labels.
- Distinguish measured findings, causal hypotheses and unknowns; explain wording robustness versus changed-goal responsiveness.
- Explain negative evidence, illustrative sampling limits, one-seed/four-task uncertainty and what additional experiment could change a claim.

## Prepare and learn

- Revisit your early predictions, the fixed metric definitions, and the distinction between eventual goal success and first-object selection.
- Review the bootstrap grouping and the limits of four tasks, one training seed per arm, benchmark overlap, and a sampled robustness panel.
- Inspect the result schema and artifact references so every report claim can point to measured evidence.

## Reading route and expected understanding

- Revisit the [analysis and interpretation contract](../doc/IMPLEMENTATION_PLAN.en.md#e-measure-and-interpret-results) and your frozen metric implementation before deciding which figures tell the story.
- Read your early hypotheses in the relevant paired document in `doc/`, including predictions that turned out wrong; use them to distinguish confirmation from post-hoc explanations.
- Inspect one complete chain of manifest, real result, trajectory, video, grouped statistic, and figure. Every major report claim needs such a recoverable chain.

## Implementation tasks

The items below define the code and documentation deliverables for this week. Existing source should be completed or extended; future components remain planned until implemented. Keep experimental parameters authoritative in the linked implementation plan.

1. **Frozen result ingestion.** Implement or finish portable result/artifact readers that validate final run identities and coverage without importing the simulator. Keep target provenance unchanged and resolve copied artifacts from an explicit local run root; preserve known incompleteness in all summaries.
2. **Final quantitative analysis.** Reuse the verified metric/uncertainty functions to regenerate task/condition/policy tables, paired differences, first-object summaries, robustness/anchor comparisons and measured compute costs. Keep development/selection results labeled separately and reconcile representative headline values against real paired records.
3. **Figure and table outputs.** Implement reproducible figure/export entry points consuming frozen records and explicit output paths. Include axes/units, sample counts, backend identity, coverage and interval definitions. Save traceable output-to-input references so every published number can be reconstructed.
4. **Illustrative episode selection and annotations.** Implement a recorded selection procedure for the planned episode review panel. Align exact instructions, state/action/predicate traces and video frames for each chosen example, annotate evidence-supported failure categories and preserve uncertain causes. Do not estimate category prevalence from illustrative sampling.
5. **Evidence-based bilingual report.** Write the research question, referenced method, results, uncertainty, examples, alternative explanations, limitations and next experiment. Connect each major claim to measured comparisons and contradictory evidence; keep hypotheses distinct from findings and do not infer improvement from training loss alone.
6. **Consistency and structure documentation.** Audit figures/tables/captions against the frozen records and synchronize report numbers/qualifiers across languages. Update the code guide with reader/aggregation/plot/annotation structures, artifact-path flow and evidence links. Retain any post-hoc ideas as explicitly labeled future work without retuning the original final study.

## Work sessions

### 1. Write an interpretation before polishing (2 hours)

**Location:** Coding computer: write the evidence-based interpretation from audited returned final tables and real cases.

**Detailed procedure**

1. Write the research question and evidence-based interpretation, including uncertainty and competing explanations.

2. Compare baseline versus canonical control to understand additional adaptation, then paraphrase versus canonical control to isolate the intended language intervention.

3. Discuss original wording, held-out paraphrases, changed targets, empty instructions, and robustness separately before combining them into a conclusion.

4. For each proposed claim, identify the measured quantity, uncertainty, supporting cases, contradictory cases, and an alternative explanation.

**Expected output:** An evidence outline that does not depend on favorable results.

**If this does not work:** If no reliable improvement appears, explain the observed limits rather than changing the question after seeing the answer.

**Session completion checklist**

- [ ] inspect the aggregate tables and write and document the explanation of canonical, paraphrase, changed-target, empty-instruction, and robustness outcomes.
- [ ] Identify evidence supporting and opposing the intervention hypothesis, including any manipulation regressions.
- [ ] Separate measured findings from causal hypotheses and unknowns; do not invent a positive narrative.

### 2. Generate and verify the final figures (3 hours)

**Location:** Coding computer: regenerate final figures from copied frozen records with declared analysis dependencies; verify one headline number manually.

**Detailed procedure**

1. Regenerate all tables and figures directly from the frozen result collection using your verified analysis functions.

2. Check task-level and aggregate rates, paired differences, first-object selection, robustness/clean comparisons, sample counts, and compute/resource costs.

3. Manually reconcile one headline value and one adaptation-control difference with underlying paired records.

4. Check axes, units, labels, backend identities, and uncertainty definitions. Do not mix development plots into final figures without explicit labeling.

**Expected output:** Final figures whose numbers and labels can be independently reconstructed.

**If this does not work:** A visually persuasive chart is not valid if counts or paired group membership differ from the declared statistic.

**Session completion checklist**

- [ ] produce per-task/condition success plots, paired target-selection summaries, robustness comparisons, uncertainty intervals, and compute-cost tables.
- [ ] manually trace at least one headline figure and one policy difference to the underlying paired episode records.
- [ ] Verify labels disclose sample counts, backend identity, development versus final status, and the conditional interpretation of intervals.

### 3. Review failures with a declared sampling method (3 hours)

**Location:** Coding computer: select and inspect twelve real returned episode bundles under the declared rule; retrieve missing referenced artifacts from the target.

**Detailed procedure**

1. Declare how the planned illustrative episodes are chosen, including coverage of policies, conditions, and available outcomes.

2. For each chosen episode, align instruction, first relevant observation, predicted/executed action, goal predicate, and video frame.

3. Assign a failure category only when the trace supports it; keep unknown or multiple plausible causes explicit.

4. Annotate examples with case identity and what they demonstrate. Do not estimate category prevalence from a small illustrative selection.

**Expected output:** Annotated, traceable examples that illustrate mechanisms without replacing full-panel statistics.

**If this does not work:** If a video seems to show success while the predicate says failure, inspect timing and goal semantics before blaming the model.

**Session completion checklist**

- [ ] Choose twelve real episodes for detailed review, four per policy, using a recorded sampling rule that covers available conditions and outcomes.
- [ ] inspect videos with state/action/predicate traces and classify failures using the agreed taxonomy; mark uncertain causes as unknown.
- [ ] Use these cases to illustrate mechanisms, not to estimate population failure frequencies or replace the complete quantitative results.

### 4. Defend one conclusion and document the findings (2 hours)

**Location:** Coding computer: support one claim using the returned statistics, uncertainty and traces.

**Detailed procedure**

1. Select one conclusion you intend to put in the report.

2. Support it with the relevant aggregate comparison, interval, and one trace example; explain why the example alone is insufficient.

3. Write the strongest alternative explanation and a specific future experiment that could separate it from your claim.

4. Review the evidence and strongest alternative explanation, correct any identified root cause, rerun affected checks and document the reasoning in the relevant bilingual `doc/` pair.

**Expected output:** A conclusion supported by documented evidence and a clear statement of what remains unknown.

**If this does not work:** Do not infer behavior across new training seeds or tasks from intervals that resample only these evaluated states.

**Session completion checklist**

- [ ] defend one claim with a table, an interval, and a video/trace example.
- [ ] Write the strongest alternative explanation and state what additional experiment would distinguish it.
- [ ] verify the reasoning and any correction, rerun affected checks, and update the bilingual design/code explanations with evidence references.

### 5. Complete the report and bilingual consistency (2 hours)

**Location:** Coding computer: finish and synchronize the bilingual report with portable artifact links and honest target provenance.

**Detailed procedure**

1. Organize the report into research question, referenced method, measured results, failure mechanisms, limitations, and the next experiment.

2. Reference manifests and the architecture document for exact settings instead of maintaining another independent parameter table.

3. Translate and edit the evidence-based report; compare numbers, qualifiers, scope, and negative findings across languages.

4. Keep post-hoc exploratory ideas labeled as future work. If the verified implementation changed a design, synchronize the corresponding architectural pair.

**Expected output:** An evidence-based bilingual report with consistent claims and recoverable artifacts.

**If this does not work:** A stronger-sounding translation must not turn a tentative mechanism or conditional result into a general claim.

**Session completion checklist**

- [ ] Write the report covering question, method references, results, uncertainty, failure examples, limitations, and the next experiment.
- [ ] assist with English/Chinese report consistency, captions, artifact links, and editing after the evidence-based interpretation is recorded.
- [ ] Keep architecture/implementation document pairs synchronized if the verified system differs from the plan; do not launch test-driven retuning as part of the original held-out claim.

## Evidence and completion checks

- [ ] Documentation ready: the paired design/code guide covers all implemented structures, rationale, interfaces and verification status.
- [ ] Authoring ready: this week's source/configuration and applicable local checks are included in the identified handoff.
- [ ] Target verified: the required real target evidence has returned and been reviewed against that handoff.
- [ ] Every headline claim traces to measured results, with uncertainty and negative evidence included.
- [ ] Reviewed examples use a declared selection rule, retain unknown causes, and do not substitute for full-panel metrics.
- [ ] The report substantiates its interpretation; the report and any updated architectural documentation are consistent across languages.

## Optional review questions

1. What evidence distinguishes robustness to wording from responsiveness to a changed goal?
2. If paraphrase adaptation helps one condition but harms canonical success, how should the report describe that tradeoff?
3. Which limitations would require more tasks or training seeds rather than more repeats of the same case?

## Delivery summary

> Analyze the frozen records, write the interpretation, challenge alternative explanations, produce figures and annotated examples, and deliver a consistent bilingual report.

## Ready for the next week

Independent authoring for later milestones may continue from agreed interfaces. The following gate applies to dependent execution and result claims.

Proceed when results, figures, failure examples, and conclusions are internally consistent and their limits are documented.

