# Week 8: Demonstration data and a verified LoRA smoke run

[English](week-08.en.md) | [简体中文](week-08.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Documentation:** Update the [bilingual code guide](../doc/CODE_GUIDE.en.md) with this week's design rationale, implemented structures and verification evidence.

**Goal:** Prepare a fair language-only adaptation dataset and verify the training/checkpoint lifecycle before full runs.

**Start authoring when:** The dataset interfaces, template families and shared recipe are specified; split/relabeling and training integration can be written before target verification.

**Run-computer prerequisite:** Both evaluation backends work, development analysis is valid, and training/validation/final prompt families are already frozen.

Planning estimate: 12 active hours across five sessions, including evidence review and documentation. GPU runtime is additional and must be measured.

## Execution locations

Use the [shared handoff procedure](../doc/ENVIRONMENT.en.md#handoff-for-every-execution-visit); the session locations below govern the detailed steps.

1. **Prepare on the coding computer:** Prepare split/identity mapping, project-copy relabeling and equality checks plus the upstream trainer configuration; leave actual loader and training evidence pending.
2. **Execute on the run computer:** After both evaluation backends and development analysis pass, load pinned real demonstrations, materialize/compare both copies, run 100 updates, save/reload and execute a rollout.
3. **Return for review:** Return source/split hashes and counts, prompt assignments, numeric-equivalence checks, real processed-batch summaries, trainable parameters, finite-update logs, reload rollout and target timing/memory.

Without target access, keep real-run checks pending, record the specific access or setup blocker, prepare the exact handoff and continue authoring that does not depend on target evidence.

## What to read and understand

Read in this order. Pending source is listed explicitly. Before completing this milestone, replace planned-code descriptions with exact implemented file/symbol links and add the relevant evidence reference.

| Order | Required reading |
| --- | --- |
| 1. Documents | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md#d-prepare-demonstrations-and-adapt-the-policy): episode splits, language-only copies, normalization and shared LoRA recipe. [Code guide](../doc/CODE_GUIDE.en.md): policy loading and planned training. |
| 2. Current code | [policy.py](../src/vla_grounding/policy.py): `PolicyConnector.__init__`, saved processors and local base identity; [assets.py](../src/vla_grounding/assets.py): snapshot records. |
| 3. Follow the calls | [pyproject.toml](../pyproject.toml): declared runtime dependencies; revisit Week 5 prompt registry and Week 4 identity schemas after they exist. |
| 4. Milestone code/evidence | Split/lineage, project-copy relabeling, loader equivalence and trainer/LoRA configuration functions: planned; read actual code and pinned LeRobot dataset tools, PEFT targets and training entry point. |

Understanding goals:

- Explain complete-episode split isolation and source-to-derived ID mapping; distinguish demonstration and simulator-state holdouts.
- Trace one sample through instruction assignment, tokens, normalization and action targets; explain why changed-target relabeling is invalid supervision.
- Explain frozen versus trainable parameters, the canonical control, equal budgets and the 100-update save/reload/rollout evidence.

## Prepare and learn

- Read the implementation plan's dataset splits, normalization contract, and shared LoRA recipe; treat it as the parameter source of truth.
- Inspect a real demonstration's images, states, actions, timestamps, episode identity, and task instruction using LeRobot's loader.
- Learn behavior cloning/action prediction, frozen backbone versus trainable adapter parameters, and why changed-target instructions cannot relabel unchanged demonstrations.

## Reading route and expected understanding

- Read the [data and adaptation contract](../doc/IMPLEMENTATION_PLAN.en.md#d-prepare-demonstrations-and-adapt-the-policy). Use its recipe as the single parameter reference.
- Inspect [pinned dataset tools](https://github.com/huggingface/lerobot/blob/v0.6.1/src/lerobot/datasets/dataset_tools.py): find split behavior, episode reindexing, and the in-place `modify_tasks` updates.
- Read [SmolVLA PEFT guidance](https://huggingface.co/docs/lerobot/en/peft_training) with the installed policy's target-module implementation. Explain the low-rank update `W = W0 + (alpha/r) BA`, with frozen `W0` and trainable adapter factors.

## Implementation tasks

The items below define the code and documentation deliverables for this week. Existing source should be completed or extended; future components remain planned until implemented. Keep experimental parameters authoritative in the linked implementation plan.

1. **Pinned data inspection and lineage.** Integrate the real LeRobot loader for the selected task demonstrations and record the immutable dataset identity. Inspect image/state/action/time alignment and preserve original episode IDs, task identities and frame ranges so every derived sample can be traced to its source.
2. **Complete-episode splitting.** Implement deterministic task-stratified splitting using the authoritative protocol. Save a source-to-derived episode map and per-task membership/counts; reject overlap, missing identities and frame-level leakage. Keep demonstration holdouts distinct from simulator-state evaluation holdouts.
3. **Project-owned training copies.** Materialize one training split and derive canonical/paraphrase copies from it. Apply the frozen instruction assignment through supported dataset tools only to those copies, preserve one consistent instruction per episode and keep the downloaded source untouched.
4. **Language-only equivalence checks.** Compare both copies through the real loader, covering numeric observations/actions, frame counts, media, episode order, sample/chunk alignment and checkpoint normalization. Allow only the intended language metadata differences; verify actual processed batches consume the assigned text and exclude validation/final templates.
5. **Upstream LoRA integration.** Prepare explicit local training configuration using the shared recipe and pinned trainer/PEFT interfaces, including its supported BF16 mechanism. Audit trainable names/sizes, frozen backbone, optimizer/schedule, base/processor identity and disabled uploads/tracking rather than writing a separate training loop.
6. **Bounded training lifecycle and documentation.** Run the prescribed smoke updates, verify finite losses and intended parameter changes, save a checkpoint with processors, reload in a fresh process and execute a real development rollout. Measure update time/memory and document split/relabeling functions, equivalence logic, LoRA choices, checkpoint flow and any shared-recipe correction before full training.

## Work sessions

### 1. Inspect data and define splits (2 hours)

**Location:** Coding computer: design split/lineage logic. Run computer: inspect actual demonstrations and produce verified complete-episode splits.

**Detailed procedure**

1. Load the pinned source dataset and inspect actual episodes for every primary task, including instruction, cameras, state, action, frame index, and timestamp.

2. Choose a short interval and explain which observation conditions the supervised action and how an action chunk can approach an episode boundary.

3. Create the plan's task-stratified split at complete-episode granularity and save source-to-derived episode identity mappings.

4. Check disjoint membership, per-task counts, and label/task consistency. Keep demonstration holdouts distinct from simulator initial-state holdouts.

**Expected output:** A verified split map and a real sample whose observation/action alignment you can explain.

**If this does not work:** If episode IDs change during copying, compare source identity maps rather than treating reindexed IDs as evidence of different data.

**Session completion checklist**

- [ ] inspect examples from all four primary tasks and explain how state/image/action samples align over time.
- [ ] Use the pinned dataset revision to create the agreed task-stratified, complete-episode splits and preserve original episode identities.
- [ ] Verify no demonstration appears in multiple splits; distinguish demonstration holdouts from the separate simulator-state evaluation holdouts.

### 2. Prepare the two training copies (3 hours)

**Location:** Coding computer: implement assignment and comparison logic. Run computer: copy/relabel only project-owned data and verify both arms through the real loader.

**Detailed procedure**

1. Build one training split, then create the two project-owned arms from that same materialized split. Never relabel the downloaded source.

2. Assign canonical wording to the control and the planned mix of canonical/training paraphrases to the adaptation arm, approximately balanced within each task.

3. Use supported task editing so frame task indices and episode/task metadata remain consistent. Inspect through the real loader, not just a text file.

4. Compare numeric sample content, media, episode order, action chunks, and normalization identities across arms; allow only intended language metadata differences.

**Expected output:** Two loader-verified training arms with a demonstrated language-only difference.

**If this does not work:** An alternative-object instruction paired with the original object's action is incorrect supervision, not useful paraphrase augmentation.

**Session completion checklist**

- [ ] create project-owned copies from one training split and use supported LeRobot task-relabeling tools only on those copies.
- [ ] assign the canonical and four training paraphrase templates approximately evenly within each task while preserving one instruction per episode.
- [ ] Verify the two arms share numeric observations, actions, frames, order, and checkpoint normalization; no alternative-object instruction may be paired with the wrong demonstration.

### 3. Verify trainable parameters and checkpoint behavior (3 hours)

**Location:** Coding computer: prepare trainer configuration from pinned interfaces. Run computer: inspect parameters, run 100 updates and save/reload/roll out.

**Detailed procedure**

1. Configure the upstream trainer from the frozen recipe and inspect how the pinned version accepts the intended BF16 runtime; do not invent a newer-version flag.

2. List trainable parameter names and sizes. Check the selected adapters/projections and frozen backbone against the policy's actual PEFT target definition.

3. Run the bounded smoke training and inspect finite loss, gradients, optimizer steps, memory, and whether intended trainable parameters actually change.

4. Save and reload into a fresh process with the saved processors and exact base identity, then run a development episode. Loading weights alone is not the full checkpoint check.

**Expected output:** A real smoke checkpoint whose parameter selection, preprocessing, and execution are verified.

**If this does not work:** Do not demand every adapter gradient be nonzero on its first step; investigate overall intended updates, initialization, and loss instead.

**Session completion checklist**

- [ ] configure the pinned upstream trainer and LoRA support using the shared recipe, BF16 interface, explicit local outputs, and uploads disabled.
- [ ] inspect the trainable parameter list and confirm the intended backbone remains frozen; explain what the learning objective compares.
- [ ] Run the planned 100-update smoke check, save and reload a checkpoint, and execute a development rollout with the restored processors.

### 4. Audit a training example and document the findings (2 hours)

**Location:** Coding computer: independently trace returned sample/batch lineage. Loader or tokenizer inspection needs the target unless its dependencies are declared here.

**Detailed procedure**

1. Pick one sample from the adaptation copy. Find its original episode and the assignment that produced its text.

2. Trace the loaded instruction through tokenization and the numeric inputs/targets through the intended normalization.

3. Verify the requested object/destination describe the demonstration and that no future evaluation template entered training.

4. Review the evidence and strongest alternative explanation, correct any identified root cause, rerun affected checks and document the reasoning in the relevant bilingual `doc/` pair.

**Expected output:** A sample-level proof that text, numeric targets, normalization, and split membership agree.

**If this does not work:** Metadata looking correct does not prove the trainer consumes it; inspect an actual processed training batch.

**Session completion checklist**

- [ ] trace one sample from its source episode through relabeling, tokenization, normalization, and action target.
- [ ] Verify that its instruction describes the recorded action and that it belongs to the intended split.
- [ ] verify the reasoning and any correction, rerun affected checks, and update the bilingual design/code explanations with evidence references.

### 5. Freeze the shared training recipe (2 hours)

**Location:** Coding computer: audit evidence and prepare both full runs. Derive all cost estimates and any recipe changes from actual target measurements.

**Detailed procedure**

1. Retain source revisions, split maps, template assignments, loader comparisons, trainable-parameter evidence, and smoke-run metadata.

2. Estimate full training time from observed update duration after startup rather than from model size or another GPU's benchmark.

3. If memory/numerical issues require changing a setting, revise the shared recipe explicitly before either full arm starts and synchronize both architecture versions.

4. Freeze the training commands/configuration and prepare the same starting checkpoint for both full runs.

**Expected output:** A reproducible shared recipe backed by actual loader, gradient, checkpoint, and resource checks.

**If this does not work:** Do not silently reduce only one arm's batch size, update count, or normalization to make it run.

**Session completion checklist**

- [ ] Save split maps, source revisions, prompt assignments, copy-comparison evidence, normalization identities, and measured update/memory cost.
- [ ] If a resource or numerical issue requires changing the recipe, explicitly apply the same revision to both arms before either full run.
- [ ] Estimate the two full runs and checkpoint-selection evaluation cost from measurements; keep all final-test cases untouched.

## Evidence and completion checks

- [ ] Documentation ready: the paired design/code guide covers all implemented structures, rationale, interfaces and verification status.
- [ ] Authoring ready: this week's source/configuration and applicable local checks are included in the identified handoff.
- [ ] Target verified: the required real target evidence has returned and been reviewed against that handoff.
- [ ] Source-to-split mappings are disjoint by episode and both training arms differ only in intended language labels.
- [ ] Trainable modules, frozen parameters, normalization, and sample/action alignment have been inspected.
- [ ] A real 100-update checkpoint saves, reloads, and runs; the shared recipe and measured resource budget are frozen.

## Optional review questions

1. Why would changing the target object in a demonstration's text usually invalidate its action labels?
2. How can changing normalization confound a comparison that is intended to change only language?
3. What does a lower training loss demonstrate, and why does it not establish better goal selection?

## Delivery summary

> Prepare and verify both dataset copies and the upstream LoRA smoke run; inspect sample lineage and trainable parameters, verify reload/rollout and document all design choices.

## Ready for the next week

Independent authoring for later milestones may continue from agreed interfaces. The following gate applies to dependent execution and result claims.

Begin full training only after data equivalence, parameter selection, finite updates, checkpoint reload, and a real post-reload rollout are verified.

