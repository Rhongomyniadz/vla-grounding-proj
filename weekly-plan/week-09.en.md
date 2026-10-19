# Week 9: Run the two controlled fine-tuning arms

[English](week-09.en.md) | [简体中文](week-09.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Goal:** Complete comparable canonical and paraphrase training runs while understanding their diagnostics and limitations.

**Start when:** Week 8 verifies data equivalence, the shared recipe, trainable parameters, checkpoint reload, and measured runtime/memory requirements.

Time budget: 12 active hours across five sessions; one hour is independent work with the agent closed. Computer runtime is additional.

## Prepare and learn

- Revisit the exact shared recipe in the implementation plan and the frozen training manifests; do not copy parameters into a separate competing specification.
- Inspect the pinned SmolVLA training objective and identify its predictions, targets, loss reduction, and frozen/trainable modules.
- Learn how data order, optimizer updates, normalization, sample exposure, and initialization can confound an adaptation comparison.

## Work sessions

### 1. Audit both run specifications (2 hours)

- [ ] You: compare the two full-run configurations field by field, permitting only the intended instruction-source and output-identity differences.
- [ ] Confirm both start from the same pretrained checkpoint, use the same source episodes and shared training seed, and keep publishing/tracking disabled.
- [ ] Agent: prepare explicit launch and supported resume commands, local checkpoint locations, and structured progress/resource logs.

### 2. Launch and inspect the canonical control (3 hours)

- [ ] Launch the canonical-instruction arm after checking the measured budget and output paths; long computer runtime is outside this session's active hours.
- [ ] Inspect early losses, finite gradients, trainable modules, learning-rate progression, memory, and actual update counts.
- [ ] Preserve its periodic checkpoints and source/processor identities; do not judge instruction-following improvement from the training curve alone.

### 3. Launch and inspect paraphrase adaptation (3 hours)

- [ ] Start the paraphrase arm independently from the same pretrained model, never from the trained canonical control.
- [ ] Verify actual training batches use only the assigned canonical/training-paraphrase labels and no validation/final wording.
- [ ] Check matched optimization/sample budgets and retain checkpoints at the planned intervals; if a recipe change is necessary, do not continue an unequal comparison.

### 4. Audit training evidence independently, then review (2 hours)

- [ ] For the first hour, close the agent and compare one checkpoint interval from each arm using actual loss, learning rate, update count, and sample metadata.
- [ ] Explain at least two reasons an apparent difference might not translate into better closed-loop behavior.
- [ ] In the second hour, review the audit with the agent and investigate anomalies without evaluating final-test cases.

### 5. Verify complete, reloadable training outputs (2 hours)

- [ ] Confirm both arms reach the planned 10,000 updates and retain the five planned periodic checkpoints, configuration, optimizer state, and processors.
- [ ] Reload a saved checkpoint from each arm and run a development rollout, recording any genuine load or execution failure.
- [ ] Prepare the fixed development validation cases for Week 10 selection; keep all final evaluation results unavailable until selection is frozen.

## Evidence and completion checks

- [ ] Both arms have matched initialization, data exposure, normalization, optimization budget, and intended language differences.
- [ ] Each completed run has reloadable checkpoints and sufficient metadata to explain or resume its actual execution.
- [ ] You can interpret the diagnostics without treating lower loss as proof of better language grounding.

## Explain without the agent

1. Why must the paraphrase arm not initialize from the already fine-tuned control?
2. Which settings besides prompt wording could explain a difference between the two runs?
3. What must you do if one arm only finishes part of its planned optimization budget?

## Suggested request to the coding agent

> Launch and monitor the two frozen training arms, explain anomalies, preserve exact run metadata, and do not change the recipe or select models using final-test outcomes.

## Ready for the next week

Proceed to checkpoint selection when both matched runs are complete and reloadable. If measured computer time overruns the calendar, carry the work forward without silently shrinking its budget.

