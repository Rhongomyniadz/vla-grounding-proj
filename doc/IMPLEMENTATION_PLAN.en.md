# Implementation Plan

[English](IMPLEMENTATION_PLAN.en.md) | [简体中文](IMPLEMENTATION_PLAN.zh-CN.md)

This plan implements the project described in the [README](../README.md). It defines the intended system, experiments, agent responsibilities, and completion criteria. Week 1 inspection and Week 2 canonical episode source are available, but target verification and all overall milestones remain outstanding; no experiment results are claimed.

For detailed agent tasks, optional review questions, and handoff checks, use the [weekly execution plans](../weekly-plan/README.en.md). This document remains the authoritative architecture and experiment specification.

## 1. Working method and ownership

The agent owns all project work: environment setup, dependency management, implementation, research choices within this protocol, prompt construction, data preparation, execution, debugging, validation, analysis, interpretation, documentation and reproduction. This includes the first implementation of every core component. The user may review decisions and evidence or change priorities; personal coding, manual execution, first attempts and understanding exercises are not delivery prerequisites.

Use the twelve milestones as dependency-ordered work packages. Weekly session estimates are planning aids for agent work, not a required user time commitment or a prediction of GPU runtime. Implement on the current Windows coding computer and execute on the separate RTX 5080 computer through WSL2. Schedule long jobs from real throughput measurements.

### Two-computer development and execution

| Work | Agent on the Windows coding computer | Agent on the RTX 5080 / Ubuntu / WSL2 computer |
| --- | --- | --- |
| Implementation | Inspect pinned source; implement all connectors and core logic; maintain configuration and bilingual explanations | Execute the transferred source snapshot; collect diagnostics for corrections |
| Setup and checks | Install the project authoring environment; run configuration, lint, format, typing and portable checks | Set up WSL/project dependencies and assets; verify CUDA, EGL, simulator/policy integration, timing and memory |
| Data and training | Implement splits, relabeling, training configurations and launch/resume procedures | Download pinned data; verify real loaders; materialize copies; train; save and reload checkpoints |
| Analysis and delivery | Inspect returned evidence; calculate metrics; explain results; produce figures, reports and the portfolio | Produce runtime-only diagnostics, missing real rollouts and fresh-environment reproduction evidence |

Implement interface-independent work ahead of target access. Weeks 1–8 can prepare connectors, the episode loop, case/goal logic, manifests, metrics and training integration; Weeks 9–12 can prepare launch audits, selection/coverage logic, report structure and reproduction procedures. Source inspection and static checks establish implementation readiness only. Do not fabricate observations, placeholder successes, runtime IDs, state hashes, timing estimates or experiment results.

Keep two progress states in each weekly checklist: **authoring ready** means source/configuration, bilingual explanations and applicable local checks are ready for handoff; **target verified** means the required real integration evidence exists and the agent has reviewed it. The overall milestone is complete only when all required evidence and documentation exist. Later authoring may start from agreed interfaces before an earlier runtime gate passes; dependent execution and interpretation still obey the prerequisites.

The agent owns the [environment guide's handoff procedure](ENVIRONMENT.en.md#handoff-for-every-execution-visit): transfer a reviewed source snapshot including required untracked files, identify it by content hashes, rebuild target-local environments/paths, execute it unchanged, and return commands, exit status/errors, machine details, source/config/lock identities and real evidence. Use available authorized access to operate the target directly. If access or an OS-level action is unavailable, state the precise missing capability, prepare the exact action and expected evidence, and request only the unavoidable user intervention. Implementation and verification ownership remain with the agent. Keep dependent checks pending and continue independent work.

Execute pending work in this order: Week 1 environment checks → Weeks 2–3 episode/reset checks → Weeks 4–6 runner/scoring/metrics checks → Weeks 7–8 robustness/data/training smoke checks → Week 9 full training → Week 10 selection then final evaluation → Weeks 11–12 interpretation and fresh target-environment reproduction. Begin each batch with its smallest real development check before longer jobs.

### Responsibilities

| Component | Agent deliverable | Explanation and evidence |
| --- | --- | --- |
| Environment | Set up both project environments, lock dependencies, fetch assets and diagnose CUDA/rendering | Dependency/platform separation; exact commands, versions and real checks |
| Model and simulator connectors | Implement loading, preprocessing, decoding, reset and resource management | Module/class/function roles, tensor contracts and upstream API choices |
| Episode inference loop | Implement the complete outer loop, counters and aligned recording | Lifecycle, action queue, stopping rules and a real traced episode |
| Language experiments | Choose protocol-compliant wording; build/freeze cases and splits; execute comparisons | Semantic equivalence, pairing controls, tokenization and prompt-split evidence |
| Goal scoring | Define outcomes and implement requested-goal predicates/termination | Original versus requested goal, first-goal ties and real-state truth tables |
| Metrics | Implement and reconcile rates, gaps, paired comparisons and uncertainty | Equations, denominators, equal task weighting and real-record examples |
| Dataset preparation and LoRA | Inspect data, create both copies, integrate training and run both arms | Language-only intervention, split lineage, frozen/trainable parameters and reload checks |
| Artifacts and visualization | Save evidence, generate figures and annotate selected videos | Identity/path contracts, coverage and links from results to artifacts |
| Conclusions and reproduction | Write both report languages, examine alternatives and reproduce the system | Supported claims, negative evidence, limitations and fresh-environment comparison |

### Feature workflow

1. **Inspect and explain:** read existing code and pinned APIs, choose the smallest compatible design, and document purpose, rationale, interfaces and planned verification in the relevant bilingual files in `doc/`.
2. **Implement completely:** the agent writes all required code, configuration, setup and execution tooling, including core experimental logic. Reuse existing library support and scope changes to the milestone.
3. **Run and diagnose:** perform applicable local checks and real target checks, preserve actual failures, fix root causes and rerun affected verification. Keep unavailable checks visibly pending.
4. **Document and deliver:** update the code guide to describe the actual structure, link evidence and commands, synchronize both languages and weekly status, and provide a concise explanation for review.

Do not wait for learner code, a closed-agent exercise, a first interpretation or a routine approval checkpoint. Each weekly plan assigns the user a code/document reading syllabus with concrete understanding goals. Personal coding and extra exercises are optional; agent execution does not wait for the reading to finish. Preserve existing user attempts without requiring new ones.

### Design and code explanation contract

Maintain [CODE_GUIDE.en.md](CODE_GUIDE.en.md) and [CODE_GUIDE.zh-CN.md](CODE_GUIDE.zh-CN.md) as the current explanation of the implemented code. Update this pair in the same change as each implementation; an undocumented new or changed structure is unfinished work.

Cover every project-owned module, command, data model, connector/class, function and nontrivial control/data-flow structure. Explain its responsibility, source location, inputs/outputs, relationships, validation/error behavior and verification status. For each material design choice, explain why it fits the project, the relevant tradeoff and why upstream functionality is reused or custom logic is needed. Use concrete examples and actual tensor shapes when available; distinguish expected contracts from measured evidence.

Keep experiment specifications authoritative here, setup instructions in [ENVIRONMENT.en.md](ENVIRONMENT.en.md), and structure/rationale in the code guide; cross-link instead of duplicating specifications or creating per-change logs. Keep function details in English docstrings and explain how functions fit together in the guide. Mark future components as planned until their source exists. Add another paired topic only when a distinct architectural concept needs its own document, linking it from the guide and README.

### Agent working instructions

- Explain design choices and unfamiliar concepts in bilingual `doc/` files as part of delivery.
- Implement core logic and routine engineering; keep user review optional.
- Show actual inputs, outputs, tensor shapes and data flow when runtime evidence is available; label unverified contracts.
- Reuse established library APIs and small, single-purpose functions.
- Explain debugging root causes and why the correction addresses them.
- Never invent results or silently change evaluation conditions.
- Follow repository coding, error-handling, documentation, testing and commit rules.

## 2. System implementation

### Environment and reproducibility

Use Python 3.12 and LeRobot v0.6.1 as the initial baseline. Resolve compatible dependencies once, verify them on the target machine, and lock them. Inspect the pinned source when using an API; development documentation may describe newer behavior.

The [environment guide](ENVIRONMENT.en.md) defines the implemented Week 1 dependency lock, separate Windows authoring and WSL2 execution environments, the handoff procedure for every milestone, connector setup, and evidence commands. Local authoring checks pass; target installation and runtime validation remain outstanding. Code and the shared lock move between machines; virtual environments, caches, and generated absolute-path configuration are rebuilt on the target. Keep portable configuration, manifests, metrics, and result readers importable without eagerly loading the Linux simulator or model stack; load those dependencies at their connector boundary. Declare any later portable analysis dependencies in project configuration before using them on the coding computer.

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
| Run manifest | Resolved configuration, source-snapshot and lock/config hashes, dependency/model/data/asset revisions, hardware, rendering details, run-relative artifact references |

Save per-episode results, compressed trajectories, and rollout videos. Trajectories must expose observations, instructions, predicted action chunks, and executed actions for inspection. Derive CSV summaries from saved results. Keep portable task/state/revision identities separate from target-local resolved paths. Preserve original runtime reports when copying evidence; resolve analysis artifact paths against the copied run root rather than rewriting provenance or expecting target absolute paths to exist on Windows.

Use structured logging and `tqdm` progress indicators. Network operations get bounded retries with warnings, then raise the last error. Configuration, decoding, and simulator errors stop the run with context. A timeout is a valid unsuccessful episode; an infrastructure exception makes the experiment incomplete. Resume only unfinished episodes under the same manifest, without duplicate results.

### Perception-to-action contract

Validate both camera observations, the eight-dimensional robot state, tokenized language and attention mask, predicted chunks, and seven-dimensional executed actions. Explicitly configure relative control mode, image resolution/orientation, preprocessing, normalization, and action decoding.

Read the downloaded checkpoint's feature names and use LeRobot's explicit rename mapping where environment and policy keys differ. Verify actual tensors and internal padding rather than assuming every intermediate has the public interface dimensions.

Retain the checkpoint's action chunk settings for the main study. Reset cached policy state and its action queue between episodes. Keep preprocessing, normalization, action execution horizon, and decoding identical across compared policies.

**Agent task:** implement and document the outer single-episode loop. In a separate development experiment, change how many predicted actions execute before requesting another chunk; predict and measure inference frequency, runtime, and behavior. Do not carry this exploratory change into the frozen main experiment without explicitly revising its configuration.

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

The agent writes the initial prompts and documents their semantic equivalence. Freeze separate training, validation, and final-test templates before adaptation. Verify that target and destination remain unambiguous and survive tokenization without truncation.

For changed-target trials, keep the physical scene fixed and change only the instruction supplied to the policy. Use LIBERO's existing predicates to evaluate the requested alternative. Original-goal completion must not terminate the alternative-goal trial. Record both eventual requested-goal success and the first object placed in the basket, including ambiguous simultaneous outcomes.

Do not swap to another benchmark task for this comparison: distractors and layouts may differ. Verify that neither requested goal is already satisfied at reset.

**Agent tasks:** implement and document case construction and requested-goal selection. Inspect one original/changed-target video pair and distinguish incorrect selection, manipulation failure, and scoring error.

### C. Evaluate environmental robustness

In the separate LIBERO-plus environment, evaluate camera viewpoints and object layouts. Before scoring policies, select ten variants per primary task per dimension without replacement using seed 42. Freeze names, metadata, initial-state references, and sampling seeds. Resolve runtime IDs from the installed suite rather than assuming metadata IDs match runtime indices.

Run one fixed episode per variant for each policy: eighty perturbed episodes per policy. Also run twenty clean anchor episodes per primary task within this backend: eighty anchor episodes per policy. Construct anchors from the pinned original task definitions and initial states through the environment connector.

Compare policies on identical cases. Match physical states for camera comparisons where supported and verify the unchanged scene components. Layout cases use their specified altered states. Keep simulator/backend identity visible in all results and do not describe every layout comparison as an exactly paired clean-state experiment.

Use bootstrap resampling over variant cases within task and dimension. Present this as a sampled project study, not a reproduction of the complete LIBERO-plus benchmark.

**Agent task:** inspect perturbations, identify what changed, and document which comparisons support causal interpretation.

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

**Agent explanation:** document what LoRA changes, which parameters stay frozen, why additional canonical training is needed as a control, and why lower training loss does not prove improved instruction following.

### E. Measure and interpret results

The agent implements basic metrics and verifies their arithmetic against a small set of real episodes, documenting a worked example:

- Success rate by task, condition, and policy.
- Paraphrase gap: paraphrase success minus original-instruction success.
- Changed-target success and first-object selection.
- Paired correctness: the original instruction selects A and the changed instruction selects B from the same initial scene.
- Intervention gain: paraphrase adaptation minus original-instruction fine-tuning.

Define strict paired selection using the first completed object goal. Record simultaneous goals separately instead of assigning an arbitrary first object. Report eventual requested-goal success separately so an unwanted first action is visible.

The agent calculates 95% bootstrap intervals using 2,000 resamples. Resample initial-state groups within each task, preserving all paraphrases and paired policy outcomes for a state. Aggregate with equal task weight. Interpret results as conditional on four selected tasks and one training seed per adaptation arm.

Also report robustness success relative to clean anchors, inference latency, rollout duration, peak GPU memory, and training cost. Interpret empty-instruction performance alongside changed-goal behavior; neither diagnostic alone establishes language use.

Review failures using a small taxonomy: wrong object, failed grasp, dropped object, placement error, timeout, and visually induced failure. Record unknown causes explicitly. Keep infrastructure errors separate. The agent writes the interpretation, evaluates confounders and alternative explanations, and documents the evidence and limits of each conclusion.

### Final evaluation budget

| Evaluation | Episodes per policy |
| --- | ---: |
| Four tasks × twenty states × six language conditions | 480 |
| Camera/layout variants | 80 |
| Clean anchors in the robustness environment | 80 |
| Total | 640 |

Three policies produce 1,920 final episodes, excluding development checks and checkpoint-selection runs. Estimate wall-clock requirements from measured throughput before scheduling them.

## 4. Twelve-week milestones

Authoring can advance independently where interfaces are known. The target-evidence column remains a dependency gate, regardless of the calendar or how much code is written. Detailed session locations and agent verification tasks are in each weekly pair.

| Week | Prepare on the coding computer | Required evidence and agent explanation |
| --- | --- | --- |
| 1 | Dependency/configuration setup, connectors, local checks, data-flow sketch | Verified WSL/CUDA/two-camera/policy/video path; explain actual representations |
| 2 | Complete episode loop, counters, recording integration | Three bounded pilot rollouts with aligned traces/videos; explain action flow |
| 3 | Explicit reset contract and isolated horizon-comparison setup | A/A and A/B/A checks plus horizon measurements; diagnose one trace |
| 4 | Case builder, manifest validation, runner/resume logic | Task/state catalog and eight-case interrupt/resume evidence |
| 5 | Prompt registry, language-case builder and goal selector | Real predicate/termination checks and same-scene language comparisons |
| 6 | Pure metrics, bootstrap/plot code | Return real development records, then verify metrics by hand and explain intervals on the coding computer |
| 7 | Isolated fork setup and variant/anchor manifest code | Verified backend isolation, real pilots and performance-independent frozen panel |
| 8 | Split/relabeling logic and shared upstream training configuration | Real loader equivalence, 100-update save/reload/rollout, measured costs |
| 9 | Audit/launch/resume procedures for both arms | Two complete comparable training runs; inspect returned diagnostics |
| 10 | Selection, final coverage and identity-audit logic | Validation-selected checkpoints, then 1,920 auditable final episodes |
| 11 | Report structure; analyze returned records on the coding computer | Traceable frozen results/videos; documented evidence-based interpretation and final figures |
| 12 | Reproduction procedure, portfolio and complete code-guide audit | Fresh target-environment representative rerun; verify returned evidence and understanding |

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

Run linting and strict type checking before completing implementation milestones. Do not add tests that merely assert prompt wording or configuration text. Run applicable portable checks on the coding computer; all simulator, CUDA, policy, real-loader and trainer checks run on the target. Match the returned evidence to the transferred source snapshot and keep unverified runtime items open. A clean local check or successful transfer does not satisfy a target integration gate.

### Explanation and documentation verification

The agent must deliver bilingual Markdown explanations in `doc/` that enable the user to:

- Trace language, images, state, preprocessing, predicted chunks, and simulator actions.
- Explain action horizons, coordinate conventions, normalization, and policy reset behavior.
- Explain which question each language comparison answers and its remaining confounders.
- Calculate and interpret the principal metrics.
- Diagnose a failure from saved observations, actions, and video.
- Explain adaptation outcomes using behavioral evidence rather than training loss alone.
- Locate every implemented structure and follow its design rationale, inputs/outputs, failure behavior and verification evidence.

The agent audits this coverage against the source tree and records unresolved runtime questions explicitly. User exercises and oral defenses are optional and are not completion gates.

### Portfolio completion

Deliver the synchronized design/code guide, verified setup/run instructions, locked dependencies, frozen manifests, machine-readable results, all three policy comparisons, plots with uncertainty estimates, annotated success/failure videos, and one report covering method, evidence, limitations, and the next experiment. Reproduce a representative small experiment in a fresh environment.

Improvement is a hypothesis, not a completion requirement. A reproducible negative result with a defensible explanation meets the research goal.

Holdouts are relative to this project's adaptation and tuning process; do not claim they were unseen during checkpoint pretraining. There is no physical hardware, reinforcement learning, LLM planning, paid cloud compute, or automatic publication in the initial scope. Keep changes uncommitted unless explicitly asked to commit.
