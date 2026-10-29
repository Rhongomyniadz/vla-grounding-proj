# Design choices and code structure

[English](CODE_GUIDE.en.md) | [简体中文](CODE_GUIDE.zh-CN.md)

This guide explains every current project-owned module and its structures. The agent updates both languages with each implementation change. Experiment parameters remain authoritative in the [implementation plan](IMPLEMENTATION_PLAN.en.md); setup commands and evidence transfer remain in the [environment guide](ENVIRONMENT.en.md). Detailed function semantics stay in English docstrings.

**Status:** Week 1 engineering exists and Windows authoring checks have passed. Target installation, CUDA, EGL, policy inference and visual video review remain unverified. The observation inspector and canonical single-episode loop are implemented; controlled manifests, alternative-goal scoring, metrics, data preparation and training integration remain planned. Expected shapes below are checked contracts, not reported target observations.

## 1. Design choices

| Choice | Rationale and tradeoff |
| --- | --- |
| One small `src/vla_grounding` package | Keeps experimental controls together without extra services or speculative abstractions. Split future modules by actual responsibility. |
| Separate Windows authoring and Linux runtime dependencies | Portable configuration/checks do not need the simulator or GPU stack. Target compatibility requires separate real checks. |
| Required configuration and project-local environments | Explicit inputs make runs inspectable. The shared lock records resolution; it does not prove target installation. |
| Validated records and small functions | Pydantic validates external records; TypedDict describes native data but does not validate it. Functions handle transformations; classes adapt stateful external systems. Schema classes describe records rather than an application object hierarchy. |
| Reuse LeRobot processors, checkpoint loading and rollout | Preserves normalization, tokenization, image/pose conventions and action queues. Requires pinned-source inspection and actual feature checks; the upstream smoke is not a controlled experiment runner. |
| Resolve references once; run from local snapshots | Immutable SHAs identify model/tokenizer/assets. Downloads need network access; runtime goes offline after bootstrap, and target paths must be rebuilt per machine. |
| Bootstrap before simulator imports | EGL and LIBERO configuration affect import-time behavior. The asset link stays inside the project environment and refuses conflicting installations. |
| Separate diagnostic prediction and execution | A chunk can be inspected without consuming its queue. Recreate/reset the simulator, policy and RNG before comparing the first actual action; this is not yet general explicit-state restoration. |
| Preserve evidence and fail explicitly | Exclusive output creation prevents overwrites. Partial artifacts remain diagnostic, not completion evidence. Network transport/HTTP failures get bounded retries and warnings; invalid configuration/integration raises. |
| Isolate base LIBERO and LIBERO-plus | They share an import namespace. The fork integration remains planned and must verify paths/imports plus clean anchors before robustness claims. |
| Current bilingual explanations | The user can follow source structure and decisions through documentation. New or changed structures require guide updates; cross-links avoid duplicated specifications. |

## 2. Repository structure

| Location | Responsibility |
| --- | --- |
| [pyproject.toml](../pyproject.toml) | Package metadata, dependencies, CLI entry points, supported resolution platforms and Ruff settings. |
| [uv.lock](../uv.lock), [.python-version](../.python-version) | Shared dependency resolution and interpreter selection; environments are rebuilt locally. |
| [configs/week-01.json](../configs/week-01.json) | Portable development-smoke inputs: hardware, task, camera/control and requested resource references. Moving VLM/assets references are resolved by fetching before runtime; this is not a frozen experiment manifest. |
| [src/vla_grounding/](../src/vla_grounding/) | Package implementation, explained below. |
| [tests/smoke_authoring.py](../tests/smoke_authoring.py) | Real installed-command smoke checks with temporary files/subprocesses, without a fake simulator. |
| [.gitignore](../.gitignore) | Excludes local environments, caches, generated runtime paths and artifacts from source handoff. |
| [doc/](./), [weekly-plan/](../weekly-plan/) | Current bilingual design/setup explanations; agent procedures, evidence and the user's weekly code/document reading syllabus. |

### Records and portable functions

| Source and structure | Inputs, outputs and relationships | Validation and design reason |
| --- | --- | --- |
| [config.py](../src/vla_grounding/config.py): `WeekOneConfig` | Development JSON → required settings used by checks/connectors. | Strict/frozen Pydantic record constrains task, shapes, control, hardware and revisions; ignores unrelated extra fields. |
| `read_config(path)` | File → validated `WeekOneConfig`. | Missing files/fields and incorrect types raise; no guessed settings. |
| [assets.py](../src/vla_grounding/assets.py): `Snapshot` | Repository ID, immutable 40-character SHA, target-local path. | Required strict/frozen record identifies one input snapshot; directory existence is checked when reading bundles. |
| `AssetBundle` | Named policy, VLM and simulator snapshots. | Keeps full weights, tokenizer/VLM metadata and simulator assets distinct. |
| `download_snapshot(repo_id, revision, repo_type, cache_dir, patterns)` | Explicit Hub request → downloaded `Snapshot` at the resolved SHA. | Resolves before downloading; transport/HTTP failures retry three times with structured warnings, then raise the last error with request context. Other errors propagate. |
| `read_assets(path)` | Saved JSON → validated `AssetBundle` whose directories exist. | Rejects missing target snapshots with a specific remediation message; never re-resolves moving references. |
| [evidence.py](../src/vla_grounding/evidence.py): `JsonValue`, `write_report(path, report)` | Recursive JSON type and mapping → new JSON file. | Creates parents, exclusively creates output, rejects NaN/Infinity. Protects prior evidence; does not implement experiment resume/coverage. |

### Command entry points and orchestration

Each `main()` accepts explicit required paths and coordinates one responsibility. Exact invocations belong to the environment guide.

| Command / source | Functions and behavior | Outputs and limits |
| --- | --- | --- |
| `vla-author-check` / [authoring.py](../src/vla_grounding/authoring.py) | `main()` → `check_authoring(config_path, output_path)`: require Python 3.12, validate settings and record interpreter/platform. | Authoring-only JSON with `target_runtime_verified=false`; no ML imports or inference claim. |
| `vla-target-check` / [runtime.py](../src/vla_grounding/runtime.py) | `main()` → `check_target(config, workspace)`. `require_target_platform(workspace)` first requires Linux/WSL2, supported architecture/Python and Linux filesystem. `check_target` checks disk, LeRobot version, CUDA/GPU identity and real matrix multiplication. | Machine/package/driver/CUDA report explicitly leaves rendering and policy unverified. Platform/device/numeric/command errors raise. |
| `vla-fetch-assets` / [assets.py](../src/vla_grounding/assets.py) | `main()` checks target/output, reads config and downloads simulator, full policy and selected VLM metadata/tokenizer files. | New immutable `AssetBundle` manifest; existing output is rejected. Large assets remain local to target. |
| `vla-render-smoke` / [render.py](../src/vla_grounding/render.py) | `main()` checks target/assets, bootstraps before runtime imports, resets and preprocesses one real observation. | Fresh directory with two oriented camera PNGs, `observation.npz` and `render.json`. No policy allocation; `finally` closes the simulator. |
| `vla-policy-smoke` / [smoke.py](../src/vla_grounding/smoke.py) | `main()` checks target/assets/bootstrap, captures a diagnostic prediction, recreates simulator and invokes bounded upstream `rollout` with processors/decoder/video callback. | Prediction/action arrays, MP4 and JSON. Checks finite actions and first-action agreement; task success is not measured and visual review begins incomplete. |
| [__init__.py](../src/vla_grounding/__init__.py) | Package marker/docstring without executable initialization or public structures. | Importing the package does not initialize the GPU/simulator. |

### External interfaces and native data structures

| Source and structure | Responsibility and contract | Rationale, validation and errors |
| --- | --- | --- |
| [bootstrap.py](../src/vla_grounding/bootstrap.py): `prepare_simulator(workspace, assets, cuda_device)` | Workspace + simulator snapshot + device → LIBERO config path; sets EGL, paths, offline mode and disabled tracking. | Requires correct project interpreter, pinned installation, complete assets and no earlier simulator imports. Links assets inside project environment and rejects conflicts. Files/environment changes are explicit external setup effects. |
| [simulator.py](../src/vla_grounding/simulator.py): `FloatArray`, `EnvironmentObservation` | Floating native-array and processed tensor/text mapping aliases. | Public types expose vendor data without introducing another format; this module requires runtime dependencies. |
| `EndEffector`, `Gripper`, `RobotState`, `CameraViews`, `RawObservation` | TypedDicts for native position/quaternion, gripper, both views and combined observations. | Describe required fields; actual reset validates array types/shapes/finite values. Unrelated simulator fields remain upstream-owned. |
| `environment_config(config, episode_length)` | `WeekOneConfig` → one-task upstream `LiberoEnv` with explicit camera mapping, relative control and length limit. | Reuses vendor configuration; current implementation supports base LIBERO only. |
| `require_camera(image, image_size)` | Native camera and resolution → validation or error. | Requires uint8 batch shape and rejects constant images. It cannot detect every visual defect. |
| `SimulatorConnector.__init__(config, episode_length)` | Creates one synchronous vector environment and its processors. | Owns simulator lifecycle at the external boundary. |
| `SimulatorConnector.reset(seed)` | Seed → validated native observation after upstream reset. | Checks both cameras and finite pose/gripper arrays. Upstream state index advances; explicit-state restoration is still planned. |
| `SimulatorConnector.prepare_observation(raw, instruction)` | Native observation + explicit text → LeRobot-processed observation. | Reuses image conversion/rotation and pose processing; requires finite eight-dimensional public state. |
| `SimulatorConnector.instruction()` | Environment → nonempty benchmark instruction. | Invalid text raises. Later language cases must supply their own explicit text and preserve intentional empty conditions. |
| `SimulatorConnector.close()` | Releases environment/EGL resources. | Orchestrators call it on normal completion and error cleanup. |
| [policy.py](../src/vla_grounding/policy.py): `ActionDecoder.__init__(processor)`, `ActionDecoder.__call__(action)` | Saved postprocessor + normalized action → decoded CPU command. | Rejects nonfinite inputs, processes a clone, requires finite `(1, 7)` output before stepping. |
| `PolicyConnector.__init__(assets, device)` | Local snapshots + device → strict full model and saved processors. | Checks public features, explicitly renames cameras, disables publishing and avoids downloading duplicate backbone weights. Incompatible interfaces raise. |
| `PolicyConnector.prepare_observation(observation)` | Environment-processed data → tokenized/normalized tensors. | Processes a copy and checks required image/state/token/mask shapes and finite values. Shapes alone do not prove meaningful untruncated text. |
| `PolicyConnector.predict_chunk(observation)` | Prepared tensors → finite normalized `(1, chunk_size, 7)` diagnostic chunk. | Uses inference mode and copied input; does not consume the action queue's first action. |
| `PolicyConnector.reset()` | Clears model queue/cache and both processor pipelines. | Required between episodes; caller also controls RNG and simulator state. |
| [video.py](../src/vla_grounding/video.py): `VideoRecorder.__init__(path, fps)` | Output/FPS → recorder with empty frame buffer. | Adapts the vendor render callback. Buffering fits the short smoke; long-run streaming is not implemented. |
| `VideoRecorder.capture(env)` | Real render callback → copied HWC RGB uint8 frame in buffer. | Checks rank/channels/dtype; copy prevents subsequent simulator mutation from changing saved frames. |
| `VideoRecorder.save()` | Buffered frames → new MP4 and decoded frame count. | Requires multiple frames/new output, writes via LeRobot and decodes every frame with PyAV; count must match. Motion/orientation require separate visual review. |

### Authoring integration checks

[tests/smoke_authoring.py](../tests/smoke_authoring.py) uses actual installed commands and files:

| Structure | Responsibility |
| --- | --- |
| `run_authoring(config, output, cwd)` | Run the package CLI outside the checkout in a real subprocess with explicit paths/timeout; return its completed process. |
| `check_cli_round_trip(config, directory)` | Require honest successful authoring evidence, then failure on repeated output without overwriting the original. |
| `check_rejected_configuration(config, directory)` | Supply an incorrectly typed seed; require field-specific failure, nonzero exit and no report. |
| `check_windows_boundary(config, directory)` | On actual Windows, require target execution to fail before ML loading at the platform boundary. |
| `main()` | Parse config, create temporary files, run checks and report success; run the Windows-specific check only on Windows. |

These checks cover command boundaries/evidence preservation. They do not replace real simulator, policy, loader or training integration.

### Week 1 inspection and Week 2 episode implementation

The Week 1 audit found the observation inspector missing. Its source and explanations now exist, alongside a complete Week 2 canonical pilot implementation. Local authoring and portable evidence checks pass; real target installation, the Week 1 GPU/camera/policy/video gate, all three Week 2 rollouts and real error-cleanup checks remain unverified. No target access is available. Infrastructure completion and successful behavior are different claims.

| Source / structure | Responsibility, contract and design |
| --- | --- |
| [inspection.py](../src/vla_grounding/inspection.py): `EvidenceArray`, `ArrayInspection` | NumPy evidence alias and a strict/frozen diagnostic record with name, shape, dtype, representation kind, numeric range, finite status and mask true count. No simulator/model import is needed, but NumPy must be installed. |
| `inspect_array(name, value)` | Return a summary without modifying its array. Float arrays must be finite; integer/token ranges are reported separately, boolean masks get true counts, text gets no numeric range. Empty/object/complex arrays raise explicit errors. |
| `inspect_arrays(arrays)`, `inspect_archive(path)` | Sort summaries deterministically; load real NPZ files with pickle disabled and inspect every array. An empty archive or unsafe/invalid content fails rather than producing a success report. |
| `write_inspection(source, output)`, `inspection.main()` | Write an exclusive JSON report; `vla-inspect-arrays --input ... --output ...` uses explicit paths. Render and policy smoke commands now produce `inspection.json` automatically. |
| [episode_records.py](../src/vla_grounding/episode_records.py): `EpisodeCase`, `StepSignals`, `EpisodeResult` | Portable strict/frozen input, native transition signals and completed-pilot result. Cases require ID, full task name, canonical text, explicit initial-state index, environment/policy seeds and step limit. Results expose stop reason, success, independent counters, time and artifact references. |
| `read_case(path)`, `stop_reason(signals, steps, max_steps)` | Validate external JSON before allocation. Decide success first, then native termination, truncation and explicit timeout; return no stop while an episode is ongoing. Invalid step accounting raises. A success on the final step stays a success. |
| [simulator.py](../src/vla_grounding/simulator.py): `environment_config(config, episode_length)`, `SimulatorConnector.__init__(config, episode_length)` | Require an explicit length separate from the short Week 1 smoke budget. Require one synchronous vector environment so terminal observations remain available until the next call. |
| `SimulatorConnector.reset_case(case)` | Validate the pinned wrapper, canonical task/text and initial-state table. Bounds-check the requested index before assigning the public `init_state_id`, preventing upstream modulo substitution. Reset, reject an already-satisfied goal and return copied selected/settled state arrays. Arbitrary serialized-state restoration and repeatability auditing remain Week 3 work. |
| `SimulatorConnector.state_identity(states)` | Hash dtype, shape and exact bytes for each captured state. These identities do not prove numeric repeatability. |
| `SimulatorConnector.reset(seed)`, `SimulatorConnector.validate_observation(raw)` | Reset both environment processors/counters and validate camera/pose/gripper contracts at reset and after every step. |
| `SimulatorConnector.step(action)` | Apply the environment postprocessor to a copied decoded action, validate it, execute once and return raw terminal observation, strict `StepSignals` and the actual executed command. Require the pinned NEXT_STEP path's boolean success/terminal arrays and finite scalar reward; no guessed success or fallback info format. Count actual executions. |
| [policy.py](../src/vla_grounding/policy.py): `RecordedSmolVLA`, `RecordedSmolVLA.reset()`, `RecordedSmolVLA._get_action_chunk(batch, noise, **kwargs)` | External adapter around the pinned SmolVLA. The upstream `select_action` calls protected `_get_action_chunk` rather than public `predict_action_chunk`. Observe that return once, validate the full chunk, copy it to CPU and count actual predictions. Keep the upstream queue and RNG behavior intact. This deliberate version coupling must be reviewed when upgrading LeRobot; RTC is rejected. |
| `PolicySelection`, `PolicyConnector.select_action(observation)` | Return the actual normalized queue action, a newly generated full chunk only when prediction occurred, and chunk index/offset. Clone processor inputs, count selection calls, use the real upstream queue and never request an extra diagnostic prediction. `PolicyConnector.reset()` resets all counts with model/processors. |
| [trajectory.py](../src/vla_grounding/trajectory.py): `save_arrays(path, arrays)` | Validate before exclusively writing a compressed NPZ. Object/nonfinite/empty evidence fails, and existing files remain untouched. This is per-episode evidence storage, not manifest resumption. |
| [evidence.py](../src/vla_grounding/evidence.py): `source_hashes(workspace)` | SHA-256 identities for current Python source, JSON configurations, package config, interpreter selection and dependency lock, including dirty/untracked source. Does not create a commit or replace the full handoff procedure. |
| [episode.py](../src/vla_grounding/episode.py): `run_episode(config, case, assets, output)`, nested `observation_arrays(raw)` | Own one complete synchronous pilot. Copy observations before stepping because vector buffers can be reused. Prepare text/tensors, select once, decode once, step once, capture a frame and persist each transition before continuing. Stop without another step/reset, validate independent counters/frame alignment, save/decode the video and close the simulator in `finally`. |
| `episode.main()` | Parse explicit config/case/assets/output, check the real target and bootstrap before runtime imports. Exclusively create a run, write `request.json` with configuration/runtime/assets/source identities, execute, then write `episode.json` only after successful evidence writing and cleanup. Exceptions preserve their original context and partial state/transition evidence; no completed record or automatic resume is created. |
| [tests/smoke_evidence.py](../tests/smoke_evidence.py): `check_archives`, `check_cases`, `main()` | Exercise real NPZ/JSON/subprocess I/O, mask/text handling, no input mutation, overwrite refusal, nonfinite rejection, actual case inputs, stop priority and Windows rejection before target work. Uses test arrays, not fabricated robot results. |
| [tests/smoke_episode.py](../tests/smoke_episode.py): `audit_episode`, `main()` | Execute the real target command, then reconcile every transition/action against its saved originating chunk, frame indices, completed coverage and prediction counts. This integration check exists but has not run here. |

The three [pilot case inputs](../configs/week-02-case-00.json) select indices 0, 1 and 2 of the pinned Spatial task 0 and retain its canonical wording. These are development inputs, not resolved/measured state identities. The target validates their task/text/index against its installed pinned data. The explicit pilot length is independent of `WeekOneConfig.smoke_steps` and is not the frozen final evaluation protocol.

### Episode lifecycle and artifact alignment

1. Target checks/bootstrap precede simulator/policy imports. Canonical case validation and state capture precede policy allocation.
2. Restore the requested benchmark index, reset environment processors, retain selected and post-settling state arrays, and check the goal is false.
3. Reset the policy/normalizers and sampling seed. Capture video frame 0.
4. For transition `i`, copy the raw input, retain processed tensors and exact instruction, select one queued action and decode exactly once. Record the full chunk only at a real new prediction.
5. Apply environment action processing and step once. Preserve terminal flags/reward, the actual control and the raw next observation. Capture video frame `i+1`.
6. Persist the NPZ and JSON for transition `i`. Stop decisions consume those actual signals; no next autoreset call follows a terminal event.
7. Save/decode the video and require `frames = actions + 1`. Require independently observed selection/execution counts to equal the transition count. Close the simulator before publishing completion.

| Artifact | Meaning |
| --- | --- |
| `request.json` | Immutable requested case, config, target/assets and selected source hashes; its initial `completed=false` stays unchanged. |
| `initial-state.npz` / `state.json` | Selected pre-settling and actual settled state, case and state hashes. |
| `chunks/NNNNNN.npz` | One full normalized prediction per actual model call; only the checkpoint horizon enters its queue. |
| `transitions/NNNNNN.npz` | Copied pre-step raw observation, processed policy tensors, next raw observation, normalized selected action, decoded action and actual executed action. |
| `transitions/NNNNNN.json` | Exact text, native signals, inference timing, chunk/offset link, arrays link and before/after frame indices. |
| `episode.mp4` / `inspection.json` | Decoded-count-verified video and first-transition array inspection; neither constitutes visual inspection or a task-success guarantee. |
| `episode.json` | Completed typed result; absent after an infrastructure exception. A completed timeout or failed terminal episode is a valid outcome. |

Episode duration measures the rollout loop including per-step evidence I/O, excluding model loading and final video encoding. This recorded-development timing is not an uninstrumented throughput benchmark.

Inference timing synchronizes CUDA around actual selection and includes chunk-evidence copying. Queued selections and new predictions are separately identifiable; there is no second sampling call. The current environment postprocessor is identity, and the target audit checks decoded/executed action equality. Changed-target goals, arbitrary-state restore, manifest resume, CSV aggregation and final metrics are intentionally still pending their later milestones.

## 3. Data flow and control flow

Portable path: `authoring.main → read_config → check_authoring → write_report`.

Runtime path: `read_config → check_target/require_target_platform → read_assets → prepare_simulator → runtime imports/connectors → operation → evidence → cleanup`. Asset download is a separate network-enabled stage before offline simulation. Bootstrap must precede simulator/OpenGL imports.

1. Simulator reset yields raw camera batches and position/quaternion/gripper components.
2. Environment preprocessing converts image layout/orientation and pose, and inserts the explicit instruction.
3. Policy preprocessing renames cameras, tokenizes text and applies saved normalization/device processing.
4. Diagnostic prediction exposes a normalized chunk. Actual upstream action selection also manages its action queue.
5. The decoder unnormalizes and validates the executed command; upstream rollout steps the environment.
6. The recorder captures real frames; orchestration writes arrays/reports and releases resources.

| Stage | Expected contract for current single-environment smoke |
| --- | --- |
| Raw views | Two uint8 `(1, 256, 256, 3)` batches, `image` / `image2` |
| Raw robot components | Position `(1, 3)`, quaternion `(1, 4)`, gripper `(1, 2)` |
| Public state | Finite `(1, 8)`; pose conversion explains why it is not the sum of raw widths |
| Policy views | Two `(1, 3, 256, 256)` tensors renamed `camera1` / `camera2` |
| Language | Tokens and attention mask `(1, L)`; `L` is the checkpoint tokenizer length |
| Predicted chunk | Finite normalized `(1, T, 7)`; `T` is checkpoint chunk capacity |
| Decoded command | Finite `(1, 7)` |

Internal resizing/padding belongs to upstream SmolVLA; public widths do not imply identical internal dimensions. The main-study horizon remains controlled by the implementation plan.

The smoke saves a prediction and first decoded action, then resets policy/processors, closes/recreates the simulator, resets RNG and runs upstream rollout. It requires the first actual action to match with `rtol=1e-4` / `atol=1e-5`. A mismatch raises for state/preprocessing/RNG diagnosis. This comparison is implemented but not yet verified on target.

`smoke.json` connects instruction, config, snapshot identities, rename mapping, chunk/horizon and run-relative artifacts. `human_video_inspection_complete` and `task_success_measured` start false. Preserve the report; record a subsequent agent visual review separately under the same run identity. Decoding an MP4 does not establish meaningful motion or success.

## 4. Planned components

These are responsibilities without project implementations yet; no future path/command is claimed to exist.

| Milestones | Agent implementation | Explanation required with implementation |
| --- | --- | --- |
| 3 | Arbitrary-state restoration and reset/horizon diagnostics | Every function/record, lifecycle/stopping rules, counters, mutable state, tolerances and real traces |
| 4–5 | Catalog, case builders, manifests/runner/resume, goal scoring | Identity, pairing, prompt splits, predicates, old-goal termination, first-goal ties, errors and artifacts |
| 6 | Metrics, grouped bootstrap, plotting | Equations, denominators, task weights, pair preservation, missing coverage and worked real examples |
| 7 | Isolated robustness backend, variants and anchors | Imports/paths, actual metadata mapping, sampling and physical/visual limits |
| 8–9 | Split/relabeling, trainer integration and launch/resume | Source lineage, loader equality, normalization, adapters/frozen parameters, budgets and reload evidence |
| 10 | Selection, final freeze and coverage | Validation-only rule/ties, immutable identities, retry/condition distinction and missing-result errors |
| 11–12 | Analysis/reporting, artifact review and reproduction | Traceable claims, uncertainty, failure evidence, portable paths, differences and guide coverage |

Replace planned entries with actual source links as implementations arrive. Update the corresponding weekly reading list with the exact files and symbols the user should read. Do not add placeholder code just to fill documentation.

## 5. Maintenance and acceptance

For each change, inventory source modules/functions/classes/records and compare them with both guide languages. Explain nontrivial loops/branches under their owning function, update contracts/rationale/examples/status and link real verification evidence with source/config/lock identities. Keep function details in docstrings and one current pair per architectural topic.

Software, evidence, reproduction and documentation remain delivery gates. The weekly syllabus tells the user what to read and understand; agent work does not wait for personal coding, manual execution or an oral defense.
