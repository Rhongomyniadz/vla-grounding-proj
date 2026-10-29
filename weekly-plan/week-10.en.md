# Week 10: Select checkpoints and execute the frozen final study

[English](week-10.en.md) | [简体中文](week-10.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Documentation:** Update the [bilingual code guide](../doc/CODE_GUIDE.en.md) with this week's design rationale, implemented structures and verification evidence.

**Goal:** Apply the predeclared selection rule, then complete final evaluation without tuning on its outcomes.

**Start authoring when:** Selection, manifest and coverage contracts are available; author the logic now and bind actual checkpoint identities only after training evidence returns.

**Run-computer prerequisite:** Both full training arms are complete and reloadable; final language states/templates and robustness manifests remain frozen and unused for tuning.

Planning estimate: 12 active hours across five sessions, including evidence review and documentation. GPU runtime is additional and must be measured.

## Execution locations

Use the [shared handoff procedure](../doc/ENVIRONMENT.en.md#handoff-for-every-execution-visit); the session locations below govern the detailed steps.

1. **Prepare on the coding computer:** Prepare the fixed selection-rule implementation, candidate/manifest audit and coverage checker. Keep final results unavailable until validation selection is frozen.
2. **Execute on the run computer:** After both training arms pass, evaluate all validation candidates, freeze the selections and exact source/configuration, then execute/resume the complete final panels.
3. **Return for review:** Return candidate scores and selected checkpoint identities, immutable final manifests, all final result rows, source/backend identities, coverage/error/resume records and artifacts required for the audit.

Without target access, keep real-run checks pending, record the specific access or setup blocker, prepare the exact handoff and continue authoring that does not depend on target evidence.

## What to read and understand

Read in this order. Pending source is listed explicitly. Before completing this milestone, replace planned-code descriptions with exact implemented file/symbol links and add the relevant evidence reference.

| Order | Required reading |
| --- | --- |
| 1. Documents | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md#d-prepare-demonstrations-and-adapt-the-policy): validation selection; final evaluation budget and completion criteria. [Code guide](../doc/CODE_GUIDE.en.md): runner/selection/coverage structures as delivered. |
| 2. Current code | [evidence.py](../src/vla_grounding/evidence.py): evidence preservation; reread actual Week 4 manifest/resume code and Week 6 paired metrics. |
| 3. Follow the calls | Validation candidate enumeration, score aggregation and earlier-step tie-breaking functions: planned; read actual source and selected-weight/processor records. |
| 4. Milestone code/evidence | Final manifest freeze, identity/coverage validation and final execution CLI: planned; trace all three policy/backend jobs to their configurations. |

Understanding goals:

- Derive selection from validation states/wording and explain why final outcomes and training loss cannot replace the declared rule.
- Reconstruct 480 language + 160 robustness/anchor episodes per policy and 1,920 total from manifest identities.
- Distinguish operational retry from changed conditions; explain affected-comparison reruns after a genuine scorer or execution bug.

## Prepare and learn

- Read the implementation plan's validation-only checkpoint selection, final episode budget, and incomplete-run rules.
- Learn why model selection must finish before inspecting held-out outcomes, including why repeated test-driven fixes change the study's interpretation.
- Inspect all case-level pairing keys and the result-coverage summary before allocating long evaluation jobs.

## Reading route and expected understanding

- Read the [checkpoint selection rule](../doc/IMPLEMENTATION_PLAN.en.md#d-prepare-demonstrations-and-adapt-the-policy) and [final evaluation budget](../doc/IMPLEMENTATION_PLAN.en.md#final-evaluation-budget) before inspecting candidate scores.
- Revisit your runner's actual identity, completion, and resume code. Determine how it rejects a changed manifest and preserves an interrupted episode.
- Read your metric functions and audit the grouping keys needed to compare policies on exactly matched cases.

## Implementation tasks

The items below define the code and documentation deliverables for this week. Existing source should be completed or extended; future components remain planned until implemented. Keep experimental parameters authoritative in the linked implementation plan.

1. **Candidate and validation manifest preparation.** Enumerate actual saved checkpoints by optimizer step, validate base/processor identities and construct the declared development-state/canonical/validation-paraphrase panel. Reject missing or unloadable candidates and preserve per-candidate case-level outputs.
2. **Deterministic checkpoint selection.** Implement the predeclared score aggregation and earlier-checkpoint tie rule as explicit functions. Save the full candidate score table and selected immutable identities for both arms. Keep training-loss preference and final-test outcomes outside selection.
3. **Final case and policy freeze.** Bind the baseline and selected adapters/processors to the frozen language/robustness/anchor cases. Validate task/state/template splits, exact instruction, requested goal, sampling seed, backend, limits and action horizon; reject duplicate IDs, missing pairs and moving asset/model references before launch.
4. **Final execution and resumption.** Run all policy/backend jobs through the verified manifest runner with explicit outputs, trajectories/videos, structured progress and resource monitoring. Resume compatible unfinished work without changing conditions or converting infrastructure errors into completed failures.
5. **Coverage and correctness audit.** Compare expected versus actual episode IDs by policy, task, condition and backend, including unexpected records. Audit a real original/changed-target pair and robustness case across policies. For a genuine execution/scoring bug, identify invalid scope and rerun all affected comparisons under a consistently identified correction.
6. **Frozen result collection and documentation.** Preserve complete final records, selection evidence, manifests, source/backend identities and correction/resume provenance. Export a coverage report and links suitable for portable analysis. Document selection functions, freeze validation, resume boundaries and completeness rules; report gaps explicitly rather than claiming the planned study finished.

## Work sessions

### 1. Select checkpoints using development validation (2 hours)

**Location:** Coding computer: implement and review the selection rule. Run computer: load/evaluate real candidates; calculate selection from returned validation scores.

**Detailed procedure**

1. Enumerate candidate checkpoints by actual saved optimizer step for both arms; verify every candidate can load with its intended processors and base revision.

2. Generate the validation panel from development states, canonical instructions, and the single validation-only template. Check case counts before launch.

3. For each candidate, compute the declared equally weighted score and keep its full per-task results. Select the highest score and use the earlier step for exact ties.

4. Record the selected identities and the table supporting that choice. Stop model selection before generating any final outcome; do not replace the rule with visual preference or training loss.

**Expected output:** A reproducible selection table and two frozen selected checkpoints.

**If this does not work:** A missing or invalid candidate is a training/checkpoint issue, not permission to select from a different set silently.

**Session completion checklist**

- [ ] Evaluate each arm's five candidate checkpoints on the four tasks, five development states, canonical wording, and the validation-only paraphrase.
- [ ] Use the predeclared mean success rule, breaking ties toward the earlier checkpoint; preserve all validation scores and selected identities.
- [ ] calculate and document a small selection example and confirm neither training loss nor final-test performance overrode the rule.

### 2. Freeze final policy and case identities (3 hours)

**Location:** Coding computer: audit case expectations. Run computer: bind actual checkpoint/assets/state paths, confirm resources and freeze the final run identities.

**Detailed procedure**

1. Create a final inventory of the baseline and selected policy/adapter weights, processors, tokenizer, code/assets, backend, and configuration identities.

2. Audit the final case matrix against the source specification: tasks, initial states, exact texts, requested goals, sampling seeds, limits, camera/control settings, and horizon.

3. Check uniqueness and pair completeness before execution. Ensure no development case or validation wording is mislabeled as final.

4. Estimate selection and final runtime separately from measured throughput. Confirm storage and resource headroom, then freeze the final manifests.

**Expected output:** A complete final-run inventory that does not depend on changing local defaults.

**If this does not work:** If a command resolves a moving model/data reference at run time, freeze it before collecting final results.

**Session completion checklist**

- [ ] Record immutable identities for the pretrained policy and the two selected adapters, processors, backends, and evaluation configurations.
- [ ] Audit the final language matrix, robustness cases, seeds, initial states, prompt splits, time limits, and action horizon against the plan.
- [ ] Generate a complete case-count/coverage expectation and estimate wall-clock runtime from actual pilot throughput, including prior selection runs.

### 3. Run the final language and robustness panels (3 hours)

**Location:** Run computer: execute and resume the frozen final language/robustness panels without source or condition changes.

**Detailed procedure**

1. Launch the fixed manifests using the verified runner and record which policy/backend jobs are active. Keep all operational settings from the frozen configuration.

2. Monitor completed-case counts, exceptions, disk usage, and process health. Seeing low success is not a reason to alter conditions.

3. After interruption, verify the manifest identity and retained complete IDs before resuming unfinished cases. Preserve partial artifacts as diagnostics, not completed outcomes.

4. Keep development, selection, and final outputs separate so summaries cannot accidentally count the same case twice or mix tuning and test data.

**Expected output:** Final execution with auditable progress and unchanged scientific conditions.

**If this does not work:** If a genuine implementation bug affects scoring or actions, pause affected comparisons, identify the invalid scope, and rerun consistently after a documented correction.

**Session completion checklist**

- [ ] execute the frozen manifests for all three policies with videos, trajectories, complete metadata, and progress reporting.
- [ ] monitor operational health and completion coverage without using emerging success rates to change prompts, tasks, checkpoints, or settings.
- [ ] Use supported same-manifest resume after interruption; do not treat infrastructure exceptions as completed failures or silently drop hard cases.

### 4. Audit evidence and document the findings (2 hours)

**Location:** Coding computer: audit returned paired results/videos. Any bug correction requires consistent affected target reruns under an identified corrected snapshot.

**Detailed procedure**

1. Select an original/changed-target final pair plus a robustness case across all policies.

2. Compare exact input text, initial-state/variant identity, policy seed, weight/processor identity, first completed goal, end reason, and video.

3. Trace any disagreement to raw artifacts, not just aggregate summaries; identify whether only reporting or the underlying execution is invalid.

4. Review the evidence and strongest alternative explanation, correct any identified root cause, rerun affected checks and document the reasoning in the relevant bilingual `doc/` pair.

**Expected output:** An independent final-record audit and a defensible scope for any correction.

**If this does not work:** Do not remove inconvenient cases, keep only successful reruns, or correct one policy while leaving comparable others invalid.

**Session completion checklist**

- [ ] audit one original/changed-target pair across policies and one robustness case from records and videos.
- [ ] Verify actual requested text, goal scorer, starting state/variant, sampling seed, policy identity, and termination behavior.
- [ ] verify the reasoning and any correction, rerun affected checks, and update the bilingual design/code explanations with evidence references.

### 5. Close coverage and preserve the final dataset (2 hours)

**Location:** Coding computer: reconcile all returned final IDs against manifests. Run computer: finish missing valid cases and retain the full raw evidence.

**Detailed procedure**

1. Reconcile expected versus observed final episode IDs by policy, task, condition, and backend. Check both missing and unexpected records.

2. Verify the source plan's complete language and robustness totals; count timeout failures as completed and infrastructure exceptions as unfinished.

3. Make the aggregation read only the completed, correct final collection and retain correction/resume provenance.

4. Freeze the evidence collection and record unresolved gaps explicitly. A partial dataset can support clearly limited reporting, not a claim that the planned study finished.

**Expected output:** A coverage-verified result collection ready for analysis, with no hidden missing cases.

**If this does not work:** A total file count is insufficient: duplicate IDs can mask missing cases, so compare identities.

**Session completion checklist**

- [ ] Verify 480 language cases and 160 robustness/anchor cases per policy, for 1,920 completed final episodes in total.
- [ ] Keep development and checkpoint-selection runs separately labeled; retain exceptions and rerun provenance rather than hiding them.
- [ ] Freeze the completed result collection for Week 11 analysis and record any unresolved omissions explicitly instead of claiming full completion.

## Evidence and completion checks

- [ ] Documentation ready: the paired design/code guide covers all implemented structures, rationale, interfaces and verification status.
- [ ] Authoring ready: this week's source/configuration and applicable local checks are included in the identified handoff.
- [ ] Target verified: the required real target evidence has returned and been reviewed against that handoff.
- [ ] Checkpoint selection is reproducible from validation-only scores and follows the fixed tie rule.
- [ ] All final cases have correct immutable policy/backend identities and preserved matched comparison keys.
- [ ] The complete 1,920-episode result collection is auditable; unresolved infrastructure gaps are not disguised as measured outcomes.

## Optional review questions

1. Why does selecting the checkpoint with the best final-test score invalidate a clean held-out comparison?
2. What distinguishes an operational retry from changing experimental conditions after seeing results?
3. Which outcomes must be revisited if a goal-scoring bug is discovered during the audit?

## Delivery summary

> Evaluate validation candidates with the fixed rule, freeze selected identities, execute/resume the final manifests and audit coverage; document selection and execution without test-driven tuning.

## Ready for the next week

Independent authoring for later milestones may continue from agreed interfaces. The following gate applies to dependent execution and result claims.

Begin final analysis only when coverage is complete or clearly marked incomplete, and all correctness issues affecting reported comparisons are resolved.

