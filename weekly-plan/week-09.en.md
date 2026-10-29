# Week 9: Run the two controlled fine-tuning arms

[English](week-09.en.md) | [简体中文](week-09.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Documentation:** Update the [bilingual code guide](../doc/CODE_GUIDE.en.md) with this week's design rationale, implemented structures and verification evidence.

**Goal:** Complete comparable canonical and paraphrase training runs while understanding their diagnostics and limitations.

**Start authoring when:** The two-arm training contract is specified; launch/resume audits can be prepared before Week 8 completes, but full training cannot start.

**Run-computer prerequisite:** Week 8 verifies data equivalence, the shared recipe, trainable parameters, checkpoint reload, and measured runtime/memory requirements.

Planning estimate: 12 active hours across five sessions, including evidence review and documentation. GPU runtime is additional and must be measured.

## Execution locations

Use the [shared handoff procedure](../doc/ENVIRONMENT.en.md#handoff-for-every-execution-visit); the session locations below govern the detailed steps.

1. **Prepare on the coding computer:** Compare the arm configurations and implement explicit launch/resume procedures and log audits. Schedule runs only after the target smoke evidence exists.
2. **Execute on the run computer:** After the Week 8 target gate, execute the two arms from the same base, inspect early updates, retain checkpoints and verify fresh-process reload rollouts.
3. **Return for review:** Return resolved invocations/config hashes, data/processor identities, real update/loss/resource logs, resume provenance, checkpoint inventory and reload videos. Keep large weights/optimizer state on target.

Without target access, keep real-run checks pending, record the specific access or setup blocker, prepare the exact handoff and continue authoring that does not depend on target evidence.

## What to read and understand

Read in this order. Pending source is listed explicitly. Before completing this milestone, replace planned-code descriptions with exact implemented file/symbol links and add the relevant evidence reference.

| Order | Required reading |
| --- | --- |
| 1. Documents | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md#d-prepare-demonstrations-and-adapt-the-policy): frozen recipe, initialization, update budget and checkpoint schedule. [Code guide](../doc/CODE_GUIDE.en.md): training structures when implemented. |
| 2. Current code | [policy.py](../src/vla_grounding/policy.py): strict load and processor restoration; [evidence.py](../src/vla_grounding/evidence.py): output preservation. |
| 3. Follow the calls | Week 8's actual split/copy verifier, trainer configuration and processed-batch inspection code after implementation. |
| 4. Milestone code/evidence | Both arm configurations, launch/resume and log-audit functions: planned; inspect the pinned upstream training loop for optimizer/scheduler/checkpoint resume state. |

Understanding goals:

- Identify permitted arm differences and prove both start from the same pretrained base with equal sample/update budgets.
- Explain loss, learning rate, gradients, trainable weights and resource diagnostics without equating lower loss with language grounding.
- Explain supported resume state and how interrupted or unequal training affects comparability before checkpoint selection.

## Prepare and learn

- Revisit the exact shared recipe in the implementation plan and the frozen training manifests; do not copy parameters into a separate competing specification.
- Inspect the pinned SmolVLA training objective and identify its predictions, targets, loss reduction, and frozen/trainable modules.
- Learn how data order, optimizer updates, normalization, sample exposure, and initialization can confound an adaptation comparison.

## Reading route and expected understanding

- Read the shared [training recipe](../doc/IMPLEMENTATION_PLAN.en.md#d-prepare-demonstrations-and-adapt-the-policy) and your verified smoke-run configuration side by side.
- Inspect the [pinned training loop](https://github.com/huggingface/lerobot/blob/v0.6.1/src/lerobot/scripts/lerobot_train.py) for optimizer updates, learning-rate scheduling, checkpoint saving, and resume behavior.
- Follow the installed policy's actual loss computation from processed action targets to its reduction. Explain what the loss measures before interpreting its curve.

## Implementation tasks

The items below define the code and documentation deliverables for this week. Existing source should be completed or extended; future components remain planned until implemented. Keep experimental parameters authoritative in the linked implementation plan.

1. **Comparable launch specifications.** Produce fully resolved canonical/paraphrase run configurations from the same verified base, dataset split, normalizers and shared recipe. Validate the permitted language/output differences field by field; reject accidental initialization from smoke weights or the already trained opposite arm.
2. **Explicit launch commands.** Provide separate reproducible invocations for both arms with configuration/data/base/output paths and immutable identities. Check measured disk/checkpoint/runtime requirements before launch and preserve exact commands, source/config/lock hashes and package/hardware details with each run.
3. **Training progress and diagnostics.** Integrate upstream training outputs with structured local progress records for optimizer updates, sample exposure, loss, learning rate, trainable-module diagnostics and resource use. Inspect early real batches and updates before unattended continuation, retaining warnings and genuine failures.
4. **Checkpoint inventory and supported resume.** Record the optimizer-step identity, weights, processors and training state for every required save. Resume through the pinned trainer's supported interface only under compatible unchanged specifications, preserving interruption and resume provenance. Do not infer completion from directory names or conceal unequal budgets.
5. **Arm-comparison and reload audit.** Reconcile both runs' initialization, numeric data, normalization, sample exposure and completed update counts. Investigate discrepancies using development evidence only. Reload a saved checkpoint from each arm in a fresh process and save a development rollout before checkpoint selection.
6. **Completion records and explanations.** Generate an auditable candidate checkpoint inventory and final progress/coverage records for both arms. Document launch/resume structures, optimizer/checkpoint relationships, allowed differences, measured costs and limited interpretation of loss. Keep full-training and validation selection prerequisites open until their real evidence exists.

## Work sessions

### 1. Audit both run specifications (2 hours)

**Location:** Coding computer: compare configurations and prepare launch commands. Run computer: confirm actual storage, checkpoint footprint and measured budget.

**Detailed procedure**

1. Compare fully resolved configurations, source/derived data identities, processors, normalization, trainable parameters, optimizer settings, seed, and update counts.

2. Make a short permitted-differences list containing the intended instruction source and output/run identity. Investigate every other difference before launch.

3. Verify both full runs initialize from the same pretrained base rather than a smoke checkpoint or the other arm's trained weights.

4. Check local disk capacity and checkpoint retention against the measured footprint. Estimate runtime as remaining updates multiplied by measured update duration, allowing separately for startup/evaluation.

**Expected output:** An audited pair of run specifications and a measured resource/scheduling estimate.

**If this does not work:** If the configurations differ unexpectedly, correct their source rather than editing only the printed log.

**Session completion checklist**

- [ ] compare the two full-run configurations field by field, permitting only the intended instruction-source and output-identity differences.
- [ ] Confirm both start from the same pretrained checkpoint, use the same source episodes and shared training seed, and keep publishing/tracking disabled.
- [ ] prepare explicit launch and supported resume commands, local checkpoint locations, and structured progress/resource logs.

### 2. Launch and inspect the canonical control (3 hours)

**Location:** Run computer: launch and inspect the canonical control, then allow verified long computation to continue unattended.

**Detailed procedure**

1. Start the canonical control with the verified command/configuration and retain the exact resolved invocation.

2. Inspect the first interval for correct data labels, optimizer progress, learning-rate schedule, intended gradients, memory, and finite losses.

3. After the first periodic save, verify its metadata and that model, processors, and training state refer to the same update.

4. Let long computation continue unattended only after these checks. Preserve warnings and actual completion state.

**Expected output:** A canonical training run whose configuration, progress, and saved state agree.

**If this does not work:** A decreasing loss does not prove valid language conditioning; inspect a real processed batch if labels seem wrong.

**Session completion checklist**

- [ ] Launch the canonical-instruction arm after checking the measured budget and output paths; long computer runtime is outside this session's active hours.
- [ ] Inspect early losses, finite gradients, trainable modules, learning-rate progression, memory, and actual update counts.
- [ ] Preserve its periodic checkpoints and source/processor identities; do not judge instruction-following improvement from the training curve alone.

### 3. Launch and inspect paraphrase adaptation (3 hours)

**Location:** Run computer: launch and inspect the independent paraphrase arm with the same optimization/sample budget.

**Detailed procedure**

1. Launch the adaptation arm independently from the same pretrained base and same shared recipe.

2. Inspect loaded batch text to confirm only canonical and training-paraphrase assignments appear, with unchanged numeric supervision.

3. Compare cumulative optimizer updates and sample exposure with the control; do not compare wall-clock durations as a substitute for equal training.

4. Keep periodic checkpoints and logs. If a resource or numerical problem changes the required recipe, document the change and restore comparability for both arms.

**Expected output:** A genuinely comparable treatment run with verified language labels and equal optimization budget.

**If this does not work:** Do not make the adaptation arm inherit the control's optimizer state or trained parameters.

**Session completion checklist**

- [ ] Start the paraphrase arm independently from the same pretrained model, never from the trained canonical control.
- [ ] Verify actual training batches use only the assigned canonical/training-paraphrase labels and no validation/final wording.
- [ ] Check matched optimization/sample budgets and retain checkpoints at the planned intervals; if a recipe change is necessary, do not continue an unequal comparison.

### 4. Audit training evidence and document the findings (2 hours)

**Location:** Coding computer: compare returned logs at the same real update interval; investigate any runtime anomaly on the target.

**Detailed procedure**

1. Select the same update interval from both logs.

2. Compare actual update count, learning rate, loss, gradient/resource diagnostics, and input identities, then explain which differences are expected from text.

3. List at least two explanations for a loss difference that do not imply better target selection, such as sampling variability or different supervision difficulty.

4. Review the evidence and strongest alternative explanation, correct any identified root cause, rerun affected checks and document the reasoning in the relevant bilingual `doc/` pair.

**Expected output:** An independent training-diagnostic comparison with appropriately limited conclusions.

**If this does not work:** Do not choose a favorite checkpoint from its loss curve; the validation selection rule comes next week.

**Session completion checklist**

- [ ] compare one checkpoint interval from each arm using actual loss, learning rate, update count, and sample metadata.
- [ ] Explain at least two reasons an apparent difference might not translate into better closed-loop behavior.
- [ ] verify the reasoning and any correction, rerun affected checks, and update the bilingual design/code explanations with evidence references.

### 5. Verify complete, reloadable training outputs (2 hours)

**Location:** Run computer: verify update completion and checkpoint reload/rollouts. Coding computer: audit the returned inventory and prepare selection.

**Detailed procedure**

1. Verify both runs reached the declared optimizer budget and each planned checkpoint exists with its exact step identity.

2. Reload a checkpoint from each arm in a fresh process using saved preprocessing and the same base revision, then run development rollouts.

3. If interruption occurred, retain resume provenance and verify that update accounting and dataset exposure remain comparable.

4. Prepare the development validation panel and enumerate checkpoint candidates, leaving final-test outcomes unavailable until selection is complete.

**Expected output:** Two complete, reloadable training arms ready for predeclared validation selection.

**If this does not work:** A directory called final or last does not establish the training budget was reached; verify recorded update state.

**Session completion checklist**

- [ ] Confirm both arms reach the planned 10,000 updates and retain the five planned periodic checkpoints, configuration, optimizer state, and processors.
- [ ] Reload a saved checkpoint from each arm and run a development rollout, recording any genuine load or execution failure.
- [ ] Prepare the fixed development validation cases for Week 10 selection; keep all final evaluation results unavailable until selection is frozen.

## Evidence and completion checks

- [ ] Documentation ready: the paired design/code guide covers all implemented structures, rationale, interfaces and verification status.
- [ ] Authoring ready: this week's source/configuration and applicable local checks are included in the identified handoff.
- [ ] Target verified: the required real target evidence has returned and been reviewed against that handoff.
- [ ] Both arms have matched initialization, data exposure, normalization, optimization budget, and intended language differences.
- [ ] Each completed run has reloadable checkpoints and sufficient metadata to explain or resume its actual execution.
- [ ] The documented diagnostics distinguish lower loss from evidence of better language grounding.

## Optional review questions

1. Why must the paraphrase arm not initialize from the already fine-tuned control?
2. Which settings besides prompt wording could explain a difference between the two runs?
3. What must you do if one arm only finishes part of its planned optimization budget?

## Delivery summary

> Launch and monitor both frozen training arms, diagnose anomalies, preserve exact run metadata and document comparability; keep the agreed recipe and final-test boundary.

## Ready for the next week

Independent authoring for later milestones may continue from agreed interfaces. The following gate applies to dependent execution and result claims.

Proceed to checkpoint selection when both matched runs are complete and reloadable. If measured computer time overruns the calendar, carry the work forward without silently shrinking its budget.

