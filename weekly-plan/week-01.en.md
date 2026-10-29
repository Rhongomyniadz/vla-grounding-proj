# Week 1: Environment and the perception-to-action pipeline

[English](week-01.en.md) | [简体中文](week-01.zh-CN.md)

[Weekly index](README.en.md) | [Implementation plan](../doc/IMPLEMENTATION_PLAN.en.md)

**Documentation:** Update the [bilingual code guide](../doc/CODE_GUIDE.en.md) with this week's design rationale, implemented structures and verification evidence.

**Goal:** Verify the RTX 5080/WSL2 runtime and explain what the robot observes and what the policy predicts.

**Start authoring when:** The planning documents and declared connector interfaces are available; target access is not required for the first authoring tasks.

**Run-computer prerequisite:** Access to the separate RTX 5080 host and its intended WSL2 distribution for inventory and runtime verification.

Planning estimate: 12 active hours across five sessions, including evidence review and documentation. GPU runtime is additional and must be measured.

## Implemented starting point and two-machine workflow

Read the [environment guide](../doc/ENVIRONMENT.en.md) for the authoritative setup, transfer steps, command sequence, artifact contract, and troubleshooting. The package, dependency lock, authoring/target checks, local asset download, simulator/policy connectors, and bounded upstream smoke command are implemented. Real authoring CLI checks pass on Windows. Target installation, CUDA, EGL, model inference and video playback remain pending; code availability does not complete those checklist items.

Use the shared handoff procedure linked below for transfer and target execution. Use the implemented observation inspector and Week 2 episode loop; verify them against real target artifacts when available.

## Current implementation and verification

The source audit is complete: configuration/setup declarations, authoring/target checks, immutable assets/bootstrap, simulator/policy connectors, camera/policy smoke, video decoding and the observation inspector are implemented. See [inspection.py](../src/vla_grounding/inspection.py), [its real-file smoke checks](../tests/smoke_evidence.py) and the [code explanation](../doc/CODE_GUIDE.en.md#week-1-inspection-and-week-2-episode-implementation).

Windows authoring smoke, array/JSON I/O checks, stop/case validation and Ruff pass. The array smoke used the available bundled Python/NumPy; a newly installed target environment and strict static type-checker run are not verified. Real GPU/CUDA/EGL/checkpoint/video evidence is absent because the target is inaccessible, so the overall Week 1 milestone remains open.

## Execution locations

Use the [shared handoff procedure](../doc/ENVIRONMENT.en.md#handoff-for-every-execution-visit); the session locations below govern the detailed steps.

1. **Prepare on the coding computer:** Install the lightweight authoring environment, review the implemented checks/connectors, document the data flow and implement the observation-inspection helper.
2. **Execute on the run computer:** Inventory the actual RTX 5080 host, then perform Linux installation and CUDA → asset fetch → camera render → policy smoke checks.
3. **Return for review:** Return the machine inventory, exact source/lock/config identities, all check reports, camera PNGs, prediction/action summaries and playable MP4. Inspect real arrays on the target unless their loader dependencies are declared locally.

Without target access, keep real-run checks pending, record the specific access or setup blocker, prepare the exact handoff and continue authoring that does not depend on target evidence.

## What to read and understand

Read in this order. Pending source is listed explicitly. Before completing this milestone, replace planned-code descriptions with exact implemented file/symbol links and add the relevant evidence reference.

| Order | Required reading |
| --- | --- |
| 1. Documents | [Environment guide](../doc/ENVIRONMENT.en.md): verification boundary, dependencies, authoring/target setup and evidence contract. [Code guide](../doc/CODE_GUIDE.en.md): design choices, repository structure and data flow. |
| 2. Current code | [config.py](../src/vla_grounding/config.py): `WeekOneConfig` / `read_config`; [authoring.py](../src/vla_grounding/authoring.py): `check_authoring`; [runtime.py](../src/vla_grounding/runtime.py): `require_target_platform` / `check_target`. |
| 3. Follow the calls | [assets.py](../src/vla_grounding/assets.py): snapshot records and download/read functions; [bootstrap.py](../src/vla_grounding/bootstrap.py): `prepare_simulator`; [pyproject.toml](../pyproject.toml) and [week-01.json](../configs/week-01.json): dependency/CLI split and explicit settings. |
| 4. Milestone code/evidence | [inspection.py](../src/vla_grounding/inspection.py): `inspect_array`, `inspect_archive`, `write_inspection`; [tests/smoke_evidence.py](../tests/smoke_evidence.py): real archive/CLI checks. Compare with `SimulatorConnector.validate_observation`. |

Understanding goals:

- Explain why an authoring pass and a resolved lock do not verify CUDA, cameras or policy execution.
- Trace requested asset reference → resolved SHA → target path → LIBERO setup, and explain why import order matters.
- Trace raw images/state/text to decoded actions and distinguish expected shapes from observed evidence.

## Prepare and learn

- Read the implementation plan's environment and perception-to-action sections, then inspect the pinned LeRobot installation and LIBERO interfaces.
- Learn observation, proprioception, end-effector pose, gripper command, relative control, action chunk, and model checkpoint.
- Sketch the path from two camera images, robot state, and instruction to an executed action. Mark preprocessing and action decoding.

## Reading route and expected understanding

- [Microsoft's WSL guide](https://learn.microsoft.com/en-us/windows/wsl/install): find how to distinguish WSL 1 and WSL 2. Your stopping point is being able to identify the distribution/version in actual host output.
- [NVIDIA's WSL guide](https://docs.nvidia.com/cuda/wsl-user-guide/index.html): read GPU driver setup and limitations. Explain which driver belongs on Windows and why a working Windows GPU does not prove your Python environment uses CUDA.
- [Pinned LeRobot environment](https://github.com/huggingface/lerobot/blob/v0.6.1/src/lerobot/envs/libero.py) and [SmolVLA processor](https://github.com/huggingface/lerobot/blob/v0.6.1/src/lerobot/policies/smolvla/processor_smolvla.py): locate observation formatting, language tokenization, normalization, and action unnormalization. You do not need to understand every model layer.

## Implementation tasks

The items below define the code and documentation deliverables for this week. Existing source should be completed or extended; future components remain planned until implemented. Keep experimental parameters authoritative in the linked implementation plan.

1. **Environment configuration and setup.** Complete the existing project-local dependency/configuration setup in `pyproject.toml`, `uv.lock` and `configs/week-01.json`. Keep Windows authoring dependencies separate from the WSL runtime; require explicit hardware, task, camera/control and revision inputs. Preserve installation failures and verify the actual target interpreter rather than treating lock resolution as installation evidence.
2. **Platform and CUDA checks.** Maintain the authoring and target-check commands as separate entry points. Validate required settings before importing ML dependencies, then verify target OS/filesystem, storage, package versions, expected GPU and a real CUDA operation. Save machine-specific reports that state exactly which checks passed and which remain unverified.
3. **Asset resolution and simulator bootstrap.** Complete immutable snapshot fetching with bounded network retries, structured warnings and required snapshot fields. Rebuild target-local LIBERO/EGL configuration and asset links before simulator imports; reject missing snapshots, conflicting paths and an incompatible interpreter instead of substituting another setup.
4. **Simulator and policy interfaces.** Complete checkpoint loading, explicit camera-key mapping, observation preparation, processor reset and action decoding using the pinned upstream APIs. Validate both views, robot state, language tensors, predicted chunks and executed actions at their boundaries. Keep the current bounded upstream smoke as an interface check.
5. **Observation inspection and evidence.** Use and verify the implemented inspection helper with explicit inputs and typed return records for shape, dtype, meaningful ranges and finite status. Apply it to real saved raw/processed arrays, treating tokens and masks separately from continuous tensors. Retain aligned camera images, diagnostic predictions, executed actions and an MP4 whose frames decode successfully.
6. **Verification and documentation.** Run the existing authoring CLI checks and the target CUDA → assets → camera → policy/video sequence when accessible. Inspect actual video content separately from decoding. Update the environment guide and code guide with verified commands, module/function roles, import order, tensor conversions and real evidence links; keep all unavailable target checks pending.

## Work sessions

### 1. Inventory the target machine and predict the data flow (2 hours)

**Location:** Coding computer: sketch the data flow. Run computer: collect the actual Windows-host and WSL inventory.

**Detailed procedure**

1. On the RTX 5080 Windows host, open PowerShell and run the following diagnostic commands. Record the actual GPU and Ubuntu distribution; do not reuse the inventory from another computer.

   ```powershell
   nvidia-smi
   wsl --list --verbose
   ```

2. Enter the intended Ubuntu distribution and run `uname -a`, `cat /etc/os-release`, `pwd -P`, `df -h .`, and `free -h`. Explain which outputs identify Linux, available resources, and the current filesystem.

3. Choose the runtime working directory inside the target WSL Linux filesystem. Your editor is on the coding computer: use the shared handoff procedure, confirm which source snapshot the execution terminal uses, and rebuild the target environment.

4. In the relevant paired document in `doc/`, draw boxes for observation, preprocessing, policy, decoded action, controller, and next observation. Under each arrow write what data crosses it.

**Expected output:** An actual machine inventory and a documented data-flow diagram, with unknown concepts explicitly marked.

**If this does not work:** If the distribution is not WSL2 or the GPU is not the intended one, fix that setup before downloading model assets.

**Session completion checklist**

- [ ] record the target GPU, available memory/storage, Windows/WSL/Ubuntu versions, and where Linux project files will live.
- [ ] document the observation-to-action path and explain each representation and transformation in the code guide.
- [x] inspect the pinned upstream setup requirements and propose the smallest simulation-only environment configuration.

### 2. Build and verify the base environment (3 hours)

**Location:** Coding computer: review dependencies and run authoring checks. Run computer: install the runtime and verify CUDA/assets/EGL.

**Detailed procedure**

1. Declare the simulation-only dependencies in project configuration, using the implementation plan's initial version baseline and the pinned source's compatibility constraints. Review the declared packages before resolving them.

2. Follow the environment guide's target installation section to create the project environment inside WSL, then inspect its interpreter path. Use its explicit `.venv/bin/` commands. The lock has resolved, but Linux installation is still a verification task; preserve any resolver or installation failure. A successful import on the coding machine is irrelevant.

3. After installing the declared dependencies, run these checks from the verified target checkout using its explicit interpreter:

   ```bash
   .venv/bin/python -c "import sys, torch; print(sys.executable); print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available())"
   .venv/bin/python -c "import torch; x=torch.ones((32,32),device='cuda'); print((x@x).mean().item()); print(torch.cuda.get_device_name(0))"
   ```

4. Run the implemented asset-fetch and render commands from the environment guide. Inspect the immutable asset manifest and generated LIBERO configuration before proceeding. The bootstrap configures paths and EGL before simulator imports; the render command produces both views without policy weights. Keep the camera images and report as evidence.

**Expected output:** The intended interpreter executes a real CUDA operation and the simulator produces two inspectable images.

**If this does not work:** Separate driver/WSL, Python-wheel, asset-path, and renderer failures. Do not hide a rendering failure by switching to CPU.

**Session completion checklist**

- [ ] implement reproducible dependency setup, CUDA checks, and headless rendering checks using the agreed versions and supported interfaces.
- [ ] run the checks inside WSL, inspect both camera images, and confirm that the reported device is the target RTX 5080.
- [ ] For any failure, save the exact command and error, identify the failing layer, and verify the root-cause correction before continuing.

### 3. Load the checkpoint and inspect a real prediction (3 hours)

**Location:** Run computer: load the checkpoint, inspect actual tensors and execute the policy smoke check; review returned summaries/video here.

**Detailed procedure**

1. Reuse the asset manifest created in Session 2, which records the checkpoint, VLM/tokenizer and simulator snapshots. Do not download moving references again for this run. Confirm local snapshot paths belong to the target before loading.

2. Print the checkpoint input/output feature names. Compare every required key against one real simulator observation and apply one explicit source-to-policy mapping.

3. Inspect the processed image tensors, state tensor, token IDs, and language mask. Write their actual shapes and ranges beside the raw representations; confirm the intended instruction survives tokenization.

4. Run the guide's implemented policy-smoke command, which reuses upstream rollout support as the initial interface check. Inspect `prediction.npz`, `executed-actions.npz`, and the short video together with `smoke.json`. The command checks the first decoded prediction against the first executed action. Treat this as an interface check, not a task-success measurement.

**Expected output:** One complete, traceable example from real raw inputs to an executed decoded action, plus a playable smoke video.

**If this does not work:** If shapes are plausible but motion is wrong, inspect camera order, state construction, action normalization, and control mode before changing the policy.

**Session completion checklist**

- [ ] expose checkpoint loading and observation preprocessing through small connectors; document the interface needed by Week 2's episode loop.
- [ ] inspect raw and processed image/state shapes, tokenizer output and mask, feature-name mapping, normalizers, predicted chunk, and executed-action dimensions.
- [ ] Use existing upstream smoke/evaluation support to obtain a prediction, step the simulator, and save a short playable video. Record resolved artifact revisions.

### 4. Implement the inspector and explain its output (2 hours)

**Location:** Coding computer: implement the inspection helper. Verify it on real returned arrays with declared dependencies, or transfer it and run it on the target; postpone verification until those arrays exist.

**Detailed procedure**

1. Start from a real saved observation and implement a small inspection helper with explicit inputs and return values.

2. Report shape, dtype, minimum/maximum where meaningful, and finite-value status. Treat text and masks separately from floating-point state/actions.

3. Write three observations in the relevant paired document in `doc/`: one representation that changes in preprocessing, one that preserves meaning, and one mismatch you would reject.

4. Review the evidence and strongest alternative explanation, correct any identified root cause, rerun affected checks and document the reasoning in the relevant bilingual `doc/` pair.

**Expected output:** A diagnostic and an explanation grounded in actual tensors, not a memorized architecture description.

**If this does not work:** If a representation is still unclear, inspect the processor path one field at a time and complete its code-guide explanation.

**Session completion checklist**

- [ ] write a small inspection function that reports shapes, dtypes, ranges, and finite-value checks for real observations.
- [ ] Use your inspection output to trace which representation changes at preprocessing and which quantities describe the robot rather than the scene.
- [ ] verify the reasoning and any correction, rerun affected checks, and update the bilingual design/code explanations with evidence references.

### 5. Collect evidence and prepare the next task (2 hours)

**Location:** Coding computer: review returned evidence and prepare the next handoff; any missing runtime check still runs on the target.

**Detailed procedure**

1. Collect the machine inventory, environment checker output, pinned revisions, camera images, processed-input summary, decoded action, and video under the same development run identity.

2. Replay the video with a normal player. Check that it contains actual simulator frames rather than an empty, frozen, or incorrectly oriented image.

3. Add only verified setup commands to the README; leave unresolved problems visible. Save conceptual explanations in the relevant paired document in `doc/` and implementation details in docstrings.

4. Before Week 2, explain which connector provides each operation needed by the episode loop and prepare the complete loop implementation and verification task.

**Expected output:** A reproducible environment evidence bundle and a precise Week 2 handoff.

**If this does not work:** A loaded model without working rendering or decoded simulator actions does not pass this week's gate.

**Session completion checklist**

- [ ] Save environment-check output, both camera examples, resolved versions, checkpoint identity, and the smoke video as development artifacts.
- [ ] Document only commands that actually worked; record unresolved compatibility questions instead of inventing a complete quickstart.
- [ ] Prepare the narrow Week 2 request: implement the complete episode loop, counters and recording in Week 2.

## Evidence and completion checks

- [x] Documentation ready: the paired design/code guide covers all implemented structures, rationale, interfaces and verification status.
- [ ] Authoring ready: this week's source/configuration and applicable local checks are included in the identified handoff.
- [ ] Target verified: the required real target evidence has returned and been reviewed against that handoff.
- [ ] CUDA execution, both camera renders, checkpoint loading, finite predictions, simulator stepping, and video playback have been verified.
- [ ] The code guide points to actual image, state, language, chunk and action representations in the saved example.
- [ ] The environment configuration and immutable artifact references can be recovered; failures are either resolved or explicitly outstanding.

## Optional review questions

1. How do robot state and camera observations provide different information?
2. Where does the instruction enter the pipeline, and which preprocessing could accidentally remove important words?
3. What does one action control, and why does seeing a valid prediction not yet prove task success?

## Delivery summary

> Set up and verify both project environments, dependencies, assets and connectors; implement the observation inspector; run the real target smoke checks and explain the complete data flow in the bilingual code guide.

## Ready for the next week

Independent authoring for later milestones may continue from agreed interfaces. The following gate applies to dependent execution and result claims.

Begin Week 2 when the environment can produce and execute a real policy action and save its observations. Resolve environment failures before debugging task behavior.

