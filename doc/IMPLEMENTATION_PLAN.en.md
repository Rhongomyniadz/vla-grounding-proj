# Implementation Plan

[English](IMPLEMENTATION_PLAN.en.md) | [简体中文](IMPLEMENTATION_PLAN.zh-CN.md)

This plan implements the project described in the [README](../README.md). It defines the intended system, experiments, learning responsibilities, and completion criteria. All implementation milestones are outstanding; no experiment results are claimed.

For detailed session tasks, learner exercises, and handoff checks, use the [weekly learning plans](../weekly-plan/README.en.md). This document remains the authoritative architecture and experiment specification.

## 1. Working method and ownership

Plan for twelve weeks at ten to fifteen hours per week on the separate RTX 5080 machine through WSL2. Reserve time for independent coding and interpretation alongside engineering and experiments.

### Responsibilities

| Component | Learner owns | Coding agent assists with |
| --- | --- | --- |
| Environment | Understanding the setup and verification commands | Dependency locking, CUDA/rendering diagnostics, setup scripts |
| Model and simulator connectors | Tracing inputs, outputs, and transformations | Library integration and relevant source explanations |
| Episode inference loop | First implementation of the outer loop | Working connectors, hints, review, integration checks |
| Language experiments | Comparisons, initial prompts, case construction | Configuration validation and execution infrastructure |
| Goal scoring | Outcome definitions and predicate selection | Simulator integration and termination review |
| Metrics | Success rates, paired comparisons, generalization gaps | Calculation review and uncertainty estimation |
| Dataset preparation and LoRA | Example inspection and intervention rationale | Preparation scripts and upstream training integration |
| Artifacts and visualization | Selecting evidence worth explaining | Serialization, video output, plotting infrastructure |
| Conclusions | First interpretation and defensible claims | Confounder analysis, alternative explanations, editing |

Aim loosely for 30–40% hands-on coding, concentrated in the core learning components. Code volume is not an acceptance metric.

### Feature workflow

1. **Understand and predict:** spend 15–30 minutes reading the relevant concepts or source. Explain inputs, outputs, expected behavior, and a prediction before experimenting.
2. **Implement a small feature:** the learner makes the first attempt at learner-owned logic. The agent provides interfaces, targeted hints, and review. For delegated engineering, give the agent a narrow task and explicit acceptance criteria.
3. **Inspect, explain, and modify:** run the feature, explain the important code, and make one meaningful change independently. The agent then supplies two or three understanding questions and one practical exercise.

The agent may continue independent infrastructure work during learner exercises. Routine delegated engineering does not require an approval checkpoint. For learner-owned components, the agent must leave the first attempt to the learner unless explicitly asked to take over.

Reserve one hour every week with the coding agent closed. Documentation, source code, the editor, and terminal remain available. At the next assisted session, explain the attempt and observations before requesting help.

A typical week allocates two hours to concepts, three to four to learner implementation, two to three to assisted engineering, two to four to experiments, and one to recall and planning. Long verified jobs may run unattended.

### Agent working instructions

- Explain unfamiliar concepts and important design choices before major features.
- Distinguish routine integration code from essential learning logic.
- Show actual inputs, outputs, tensor shapes, and data flow for model and evaluation code.
- Reuse established library APIs and implement small, independently testable changes.
- Explain debugging root causes and why the correction addresses them.
- Never invent results or silently change evaluation conditions.
- Follow the supplied repository coding, error-handling, documentation, testing, and commit rules.

## 2. System implementation

### Environment and reproducibility

Use Python 3.12 and LeRobot v0.6.1 as the initial baseline. Resolve compatible dependencies once, verify them on the target machine, and lock them. Inspect the pinned source when using an API; development documentation may describe newer behavior.

Maintain separate Python environments for base LIBERO and LIBERO-plus because both provide the `libero` import namespace. Pin the simulator fork and asset revisions independently. Keep code, environments, datasets, and assets inside WSL's Linux filesystem, with approximately 100 GB free storage.

The first environment check must verify:

1. WSL GPU access and a real PyTorch CUDA operation.
2. MuJoCo rendering for the main and wrist cameras.
3. Checkpoint, tokenizer, and processor loading.
4. Finite policy actions and successful simulator stepping.
5. MP4 writing and playback.

Start with the documented EGL rendering configuration. Fail with a specific diagnostic if it does not work; do not silently substitute a backend or machine. Follow NVIDIA's [WSL driver guidance](https://docs.nvidia.com/cuda/wsl-user-guide/index.html), which uses the Windows host GPU driver.

Measure peak memory, training-update duration, and episode duration before estimating full experiment cost. No paid compute or automatic uploads are included. Disable automatic model publishing and external experiment tracking.

Resolve model, tokenizer, dataset, and asset references to immutable revisions before the first measured run. Save the resolved dependency versions, configuration, revisions, hashes, hardware details, and rendering backend with each experiment.

### Architecture and interfaces

Build one small Python package with five responsibilities:

| Responsibility | Behavior |
| --- | --- |
| Environment connector | Construct simulations, restore initial states, step actions, evaluate predicates, close resources |
| Policy connector | Load checkpoint/processors, prepare observations, reset policy state, generate actions |
| Experiment runner | Execute explicit episode manifests and save results |
| Dataset preparation | Select demonstrations, create episode splits, produce instruction variants |
| Analysis | Calculate metrics, generate plots, export report tables |

Reuse LeRobot's loading, processors, dataset tools, LoRA support, and training loop. Keep custom code focused on experimental controls. Use typed, single-purpose functions for configuration, manifests, relabeling, metrics, and analysis; limit classes to external interfaces.

Provide separate commands for environment checks, manifest preparation, evaluation, dataset preparation, training each arm, and analysis. Commands take explicit configuration or manifest paths and must not rely on hidden experiment settings.

Use structured, runtime-validated records with required fields. Ignore unrelated extra fields from external data without weakening validation of required fields.

| Record | Required information |
| --- | --- |
| Experiment specification | Policy revision, backend, tasks, instruction conditions, initial states, seeds, rollout limits |
| Episode specification | Stable ID, scene, instruction, requested goal, initial-state reference, policy sampling seed |
| Episode result | Completion status, requested-goal success, first completed goal, steps, timing, artifact references |
| Run manifest | Resolved configuration, dependency/model/data/asset revisions, hashes, hardware, rendering details |

Save per-episode results, compressed trajectories, and rollout videos. Trajectories must expose observations, instructions, predicted action chunks, and executed actions for inspection. Derive CSV summaries from saved results.

Use structured logging and `tqdm` progress indicators. Network operations get bounded retries with warnings, then raise the last error. Configuration, decoding, and simulator errors stop the run with context. A timeout is a valid unsuccessful episode; an infrastructure exception makes the experiment incomplete. Resume only unfinished episodes under the same manifest, without duplicate results.

### Perception-to-action contract

Validate both camera observations, the eight-dimensional robot state, tokenized language and attention mask, predicted chunks, and seven-dimensional executed actions. Explicitly configure relative control mode, image resolution/orientation, preprocessing, normalization, and action decoding.

Read the downloaded checkpoint's feature names and use LeRobot's explicit rename mapping where environment and policy keys differ. Verify actual tensors and internal padding rather than assuming every intermediate has the public interface dimensions.

Retain the checkpoint's action chunk settings for the main study. Reset cached policy state and its action queue between episodes. Keep preprocessing, normalization, action execution horizon, and decoding identical across compared policies.

**Learner exercise:** write the outer single-episode loop. In a separate development experiment, change how many predicted actions execute before requesting another chunk; predict and measure inference frequency, runtime, and behavior. Do not carry this exploratory change into the frozen main experiment without explicitly revising its configuration.

## 3. Experimental protocol

### A. Establish the baseline

Start with one LIBERO-Spatial task and three episodes to verify the pipeline. Save successful and unsuccessful videos and trace the instruction-to-action path.

Freeze four primary LIBERO-Object tasks by full task name, recording the IDs resolved from the pinned benchmark:

| Task name | Alternative target in that same scene |
| --- | --- |
| `pick_up_the_alphabet_soup_and_place_it_in_the_basket` | Cream cheese |
| `pick_up_the_cream_cheese_and_place_it_in_the_basket` | Alphabet soup |
| `pick_up_the_tomato_sauce_and_place_it_in_the_basket` | Butter |
| `pick_up_the_butter_and_place_it_in_the_basket` | Tomato sauce |

Verify the required objects and goal regions in the pinned task definitions. Do not replace poorly performing tasks after inspecting results. Investigate interface and execution errors if baseline behavior is consistently unsuccessful before expanding the experiment.

### B. Evaluate language behavior

For each primary task, reserve five initial states for development and twenty different states for final evaluation. Persist their identities and state hashes. Match simulator initial states and policy sampling seeds across instruction conditions and policies; the same integer environment seed alone is insufficient.

Use six final conditions:

| Condition | Instruction and scoring |
| --- | --- |
| Original | Benchmark wording; score the original goal |
| Paraphrase 1 | Held-out lexical variation; score the original goal |
| Paraphrase 2 | Held-out sentence structure; score the original goal |
| Paraphrase 3 | Held-out contextual phrasing; score the original goal |
| Changed target | Request the paired alternative object; score that alternative goal |
| Empty instruction | Empty task content through normal tokenization; score the original goal diagnostically |

The learner writes the initial prompts and explains their semantic equivalence. Freeze separate training, validation, and final-test templates before adaptation. Verify that target and destination remain unambiguous and survive tokenization without truncation.

For changed-target trials, keep the physical scene fixed and change only the instruction supplied to the policy. Use LIBERO's existing predicates to evaluate the requested alternative. Original-goal completion must not terminate the alternative-goal trial. Record both eventual requested-goal success and the first object placed in the basket, including ambiguous simultaneous outcomes.

Do not swap to another benchmark task for this comparison: distractors and layouts may differ. Verify that neither requested goal is already satisfied at reset.

**Learner exercises:** implement case construction and requested-goal selection. Inspect one original/changed-target video pair and distinguish incorrect selection, manipulation failure, and scoring error.

### C. Evaluate environmental robustness

In the separate LIBERO-plus environment, evaluate camera viewpoints and object layouts. Before scoring policies, select ten variants per primary task per dimension without replacement using seed 42. Freeze names, metadata, initial-state references, and sampling seeds. Resolve runtime IDs from the installed suite rather than assuming metadata IDs match runtime indices.

Run one fixed episode per variant for each policy: eighty perturbed episodes per policy. Also run twenty clean anchor episodes per primary task within this backend: eighty anchor episodes per policy. Construct anchors from the pinned original task definitions and initial states through the environment connector.

Compare policies on identical cases. Match physical states for camera comparisons where supported and verify the unchanged scene components. Layout cases use their specified altered states. Keep simulator/backend identity visible in all results and do not describe every layout comparison as an exactly paired clean-state experiment.

Use bootstrap resampling over variant cases within task and dimension. Present this as a sampled project study, not a reproduction of the complete LIBERO-plus benchmark.

**Learner exercise:** inspect perturbations, identify what changed, and explain which comparisons support causal interpretation.

### D. Prepare demonstrations and adapt the policy

Compare pretrained SmolVLA, original-instruction fine-tuning, and paraphrase fine-tuning. Use demonstrations from the four selected tasks in the pinned LIBERO dataset.

Split complete episodes 70% training, 15% validation, and 15% held-out, stratified by task with seed 42. Never split frames from one demonstration across sets. Preserve mappings to original episode identities.

Create the training split once, then make two project-owned copies. Keep numeric observations, actions, frame counts, episode ordering, and normalization identical. Retain canonical wording for the control; distribute adaptation episodes approximately evenly across canonical wording and four training paraphrases. Give each demonstration one consistent instruction throughout.

Use LeRobot's dataset tools. Its task-modification operation edits data in place, so relabel only the project-owned copy, never the downloaded source. Verify through the real loader that both arms differ only in language. Preserve checkpoint normalization statistics explicitly in both training arms and their saved processors.

Use the following shared initial recipe:

| Setting | Choice |
| --- | --- |
| Initialization | Same pretrained LIBERO checkpoint and processors |
| Adaptation | LoRA, rank 16, alpha 16 |
| Targets | LeRobot's SmolVLA default PEFT targets |
| Backbone | Frozen vision and language backbone |
| Batch size | 4 |
| Precision | BF16 through the supported trainer/Accelerate interface |
| Learning rate | `1e-4` |
| Schedule | 500 warmup updates; cosine decay to `1e-5` |
| Training budget | 10,000 optimizer updates per arm |
| Checkpoint interval | 2,000 updates |
| Training seed | 42 for both arms |

Run a 100-update smoke check, inspect trainable parameters and finite losses, save, reload, and execute a rollout. Diagnose failures and explicitly revise the shared recipe before either full run. Both arms must retain identical sample exposure and optimization budgets.

Select each arm's checkpoint using mean success on canonical instructions and one validation-only paraphrase across the development states. Break ties in favor of the earlier checkpoint. Freeze both selections before final evaluation; never select using final-test results.

**Learner checkpoint:** explain what LoRA changes, which parameters stay frozen, why additional canonical training is needed as a control, and why lower training loss does not prove improved instruction following.

### E. Measure and interpret results

The learner first implements and manually verifies basic metrics against a small set of real episodes:

- Success rate by task, condition, and policy.
- Paraphrase gap: paraphrase success minus original-instruction success.
- Changed-target success and first-object selection.
- Paired correctness: the original instruction selects A and the changed instruction selects B from the same initial scene.
- Intervention gain: paraphrase adaptation minus original-instruction fine-tuning.

Define strict paired selection using the first completed object goal. Record simultaneous goals separately instead of assigning an arbitrary first object. Report eventual requested-goal success separately so an unwanted first action is visible.

With agent guidance, calculate 95% bootstrap intervals using 2,000 resamples. Resample initial-state groups within each task, preserving all paraphrases and paired policy outcomes for a state. Aggregate with equal task weight. Interpret results as conditional on four selected tasks and one training seed per adaptation arm.

Also report robustness success relative to clean anchors, inference latency, rollout duration, peak GPU memory, and training cost. Interpret empty-instruction performance alongside changed-goal behavior; neither diagnostic alone establishes language use.

Review failures using a small taxonomy: wrong object, failed grasp, dropped object, placement error, timeout, and visually induced failure. Record unknown causes explicitly. Keep infrastructure errors separate. The learner writes the first interpretation; the agent challenges confounders and alternative explanations before editing conclusions.

### Final evaluation budget

| Evaluation | Episodes per policy |
| --- | ---: |
| Four tasks × twenty states × six language conditions | 480 |
| Camera/layout variants | 80 |
| Clean anchors in the robustness environment | 80 |
| Total | 640 |

Three policies produce 1,920 final episodes, excluding development checks and checkpoint-selection runs. Estimate wall-clock requirements from measured throughput before scheduling them.

## 4. Twelve-week milestones

| Week | Deliverable | Learner implementation or understanding checkpoint |
| --- | --- | --- |
| 1 | Verified WSL/CUDA/rendering environment | Explain observations, robot state, end-effector actions, and control frames |
| 2 | Single-episode rollout and video | Write the outer loop and trace instruction-to-action data flow |
| 3 | Reliable resets and saved trajectories | Run the action-horizon exercise; diagnose one rollout |
| 4 | Validated manifests and reproducible runner | Construct matched cases; explain why seeds alone are insufficient |
| 5 | Paraphrase and changed-target evaluator | Write prompts, requested-goal selection, and paired comparisons |
| 6 | Baseline language results and uncertainty estimates | Implement metrics, verify them manually, and explain limitations |
| 7 | Camera/layout robustness panel | Inspect perturbations and independently classify several failures |
| 8 | Dataset splits, relabeled copies, LoRA smoke checkpoint | Inspect demonstration/action alignment and justify the intervention |
| 9 | Two completed fine-tuning runs | Compare diagnostics and distinguish loss reduction from behavioral improvement |
| 10 | Selected checkpoints and complete final evaluation | Apply the selection rule and audit recorded outcomes |
| 11 | Figures, failure analysis, report draft | Write the first interpretation, including evidence against the hypothesis |
| 12 | Reproduced experiment and finished portfolio | Independently modify core code and explain the complete system |

Do not add a dashboard, another model family, or another simulator during this schedule. Use available time to strengthen understanding, debugging, and reproducibility.

## 5. Validation and completion criteria

### Software verification

Use a minimal set of real integration checks:

1. Render, preprocess, predict, step, and save a playable rollout with validated shapes and finite values.
2. Restore the same simulator state twice and compare state/observations within a documented tolerance.
3. Validate known negative and positive states for both goals, including continued execution after original-goal completion in changed-target trials.
4. Load both training copies through LeRobot and verify identical numeric data and intended language differences.
5. Train, save, reload, and execute a real rollout.
6. Run a small manifest, resume it, and regenerate consistent summaries without duplicate episodes.

Run linting and strict type checking before completing implementation milestones. Do not add tests that merely assert prompt wording or configuration text.

### Independent learning verification

With the agent closed, the learner must be able to:

- Trace language, images, state, preprocessing, predicted chunks, and simulator actions.
- Explain action horizons, coordinate conventions, normalization, and policy reset behavior.
- Explain which question each language comparison answers and its remaining confounders.
- Calculate and interpret the principal metrics.
- Diagnose a failure from saved observations, actions, and video.
- Explain adaptation outcomes using behavioral evidence rather than training loss alone.
- Modify a core component and verify its effect independently.

### Portfolio completion

Deliver verified setup/run instructions, locked dependencies, frozen manifests, machine-readable results, all three policy comparisons, plots with uncertainty estimates, annotated success/failure videos, and one report covering method, evidence, limitations, and the next experiment. Reproduce a representative small experiment in a fresh environment.

Improvement is a hypothesis, not a completion requirement. A reproducible negative result with a defensible explanation meets the research goal.

Holdouts are relative to this project's adaptation and tuning process; do not claim they were unseen during checkpoint pretraining. There is no physical hardware, reinforcement learning, LLM planning, paid cloud compute, or automatic publication in the initial scope. Keep changes uncommitted unless explicitly asked to commit.
