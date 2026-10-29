# Development environments and cross-computer handoff

[English](ENVIRONMENT.en.md) | [简体中文](ENVIRONMENT.zh-CN.md)

[Project architecture](IMPLEMENTATION_PLAN.en.md#2-system-implementation) | [Weekly guides](../weekly-plan/README.en.md) | [Week 1 learning guide](../weekly-plan/week-01.en.md)

The agent owns every setup, transfer, execution, diagnostic and evidence-review step in this guide. User review is optional. Lack of target access leaves target checks pending while independent implementation continues.

## Current verification boundary

Windows x64 is the authoring environment. Ubuntu/WSL2 x86-64 on the separate RTX 5080 computer is the execution environment. Python 3.12 is required in both. A passing authoring check says nothing about target CUDA, rendering, inference, or video playback.

The package installs and the real authoring CLI smoke checks pass on Windows. The dependency graph resolves into `uv.lock`; this is a resolved lock, not evidence that the Linux packages install or execute successfully. Target installation, EGL rendering, checkpoint inference, and MP4 playback remain unverified. Week 1 remains incomplete until target evidence exists.

## Dependencies and portable files

`pyproject.toml` declares lightweight authoring dependencies separately from the Linux-only `runtime` extra. Runtime resolution follows LeRobot 0.6.1, hf-libero 0.1.4, PyTorch 2.10.0 / torchvision 0.25.0 from the CUDA 12.8 index, and TorchCodec 0.10.0. TorchCodec's matching PyTorch version matters independently of CUDA availability. The lock covers Windows AMD64 and Linux x86-64; other architectures are outside this initial setup.

Transfer the source tree, `pyproject.toml`, `uv.lock`, `.python-version`, `configs/`, `tests/`, and documentation to a checkout inside the target's Linux filesystem, such as `~/projects/vla-grounding-proj`. Include new files when transferring uncommitted work. Rebuild `.venv`, `.cache`, and `.runtime` on each machine; these directories are ignored and contain platform-specific binaries or absolute paths. Keep `artifacts/` local or transfer selected evidence separately. Never execute the Windows virtual environment from WSL or copy it to the target.

The application configuration contains no machine-specific absolute paths. Snapshot manifests and LIBERO configuration are generated on the target and intentionally contain its actual local paths. Use the same source and lock on both machines. Do not develop against the target's live virtual environment through a copied Windows interpreter.

## Handoff for every execution visit

Use this procedure for all twelve milestones, using available authorized target access. If access is unavailable, prepare the exact handoff and keep execution pending until access or an unavoidable user action is available. The commands below cover Week 1 and the Week 2 canonical pilot; manifest runners, training and analysis commands remain later work. The agent prepares the handoff record explicitly until the relevant runner records this provenance automatically.

1. **Prepare on the coding computer.** Review `git status --short`, `git --no-pager diff`, and required untracked files. Run applicable authoring checks below. Choose a unique handoff identity and record the intended milestone, configuration paths, exact target commands, expected outputs, and pending runtime checks. The agent implements every required component, including the first episode loop and inspection logic.
2. **Freeze a portable source snapshot.** Include `src/`, `tests/`, `configs/`, `pyproject.toml`, `uv.lock`, `.python-version`, `.gitignore`, `AGENTS.md`, `README.md`, `doc/`, `weekly-plan/`, and any later required project scripts. Record the base Git revision, if present, plus a relative-path file list and SHA-256 for every included file. A Git revision alone does not identify dirty work. New untracked code/configuration belongs in the snapshot; ignored environments, caches, generated runtime paths, datasets, checkpoints and run outputs do not. Do not create a commit just to transfer work; a plain Git pull or archive of HEAD does not include current uncommitted changes.
3. **Copy and verify on the run computer.** Transfer through an available file-transfer method to a separate, clearly named source directory under the target's WSL Linux filesystem. Preserve file bytes and compare the complete file list and hashes before using it. `Get-FileHash -Algorithm SHA256 <file>` on Windows and `sha256sum <file>` in Linux provide per-file checks. Keep the handoff record beside the run artifacts. Do not merge a new snapshot into an actively running checkout or overwrite target-only edits; first return and reconcile those edits on the coding computer.
4. **Prepare the target environment.** Confirm hostname, `pwd -P`, interpreter, backend, configuration and lock identity. Follow the target setup/check sequence below for the first visit; after source/dependency changes, synchronize the target project environment from the transferred lock and run the affected smallest real check. Keep base LIBERO and LIBERO-plus separate. Recreate `.runtime` paths and asset links locally; previously copied absolute paths are provenance, not reusable runtime settings.
5. **Execute in dependency order.** Run the weekly target checks before larger jobs. Keep source/configuration unchanged during a run, and record exact invocation, run identity, source/lock/config hashes, actual machine/backend, exit status, stdout/stderr, and expected-versus-produced outputs. A local code correction needs a new handoff snapshot and affected target checks. Resume only a compatible unchanged run specification; do not change code or conditions under an existing run identity.
6. **Return and inspect evidence.** Copy the complete required evidence bundle below, retaining relative paths, a file list and hashes; verify receipt before analysis. Keep original reports untouched, including target absolute paths. Portable analysis resolves copied files from the local run root with an explicit path mapping where an existing report uses target paths. Do not import the simulator merely to read results. Play videos, inspect errors and coverage, and compare snapshot identities before updating bilingual checklists.

| Material | Transfer and ownership |
| --- | --- |
| Source, configuration and shared lock | Coding computer → target; reviewed immutable handoff snapshot |
| `.venv`, `.cache`, `.runtime`, generated LIBERO config and links | Rebuild/resolve on each target setup; never copy the Windows environment |
| Pinned model/data/assets and derived training copies | Download/prepare on target; preserve revisions, split maps and hashes; large files need not return for ordinary review |
| Results, manifests, JSON diagnostics, camera images, selected tensors, logs, videos and coverage | Target → coding computer, under the same run identity and directory structure |
| Adapter/checkpoint weights, optimizer state and processors | Retain on target with verified identities; transfer explicitly for backup or reproduction when needed, rather than copying the live training directory |

Return evidence by milestone: Week 1 inventory and CUDA/render/policy reports plus images/video; Weeks 2–3 pilot traces, reset comparisons and horizon measurements; Weeks 4–6 task/state catalogs, manifests, real episode results, predicate checks and resume/coverage evidence; Week 7 backend/variant/anchor manifests and pilot images; Weeks 8–9 split maps, loader comparisons, trainable-parameter and training logs, checkpoint identities and reload rollouts; Week 10 validation selection and complete final records with coverage; Week 12 fresh-environment comparison records. Retain full evidence on the target even when only selected large trajectories/videos are copied for a particular audit. Final analysis still needs all final result records, and an audit must retrieve any referenced artifact it uses.

If target access is unavailable, prepare the source, configuration, predictions and run procedure locally; leave real-run exercises and target checks pending. Missing returned evidence is an incomplete handoff. A mismatched hash requires correcting the transfer or identifying a new snapshot before execution or analysis. Diagnose installation/runtime failures from the actual target log and return the fix through the same cycle.

## Authoring setup

Use an actual Python 3.12 interpreter, not an unconfigured Windows Store alias. If `uv` is already available, run `uv sync --locked --extra tools` in this checkout. Otherwise bootstrap only the declared tooling in a project environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install ".[tools]"
.\.venv\Scripts\uv.exe sync --locked --extra tools
```

The bootstrap gets uv into the project environment; the following locked sync makes the dependency versions match the shared lock. This does not install the Linux runtime extra on Windows.

Run from the repository root:

```powershell
.\.venv\Scripts\python.exe -m vla_grounding.authoring --config configs/week-01.json --output artifacts/authoring/check-01.json
.\.venv\Scripts\python.exe tests/smoke_authoring.py --config configs/week-01.json
.\.venv\Scripts\ruff.exe check src tests
.\.venv\Scripts\ruff.exe format --check src tests
```

Reports are exclusive creations: choose a fresh output file for each check. The command smoke test uses temporary real files and subprocesses, without mocking CUDA or the simulator. Its Windows boundary check runs only on Windows. On other machines it still checks authoring behavior, invalid external configuration, and report preservation.

These checks cover the current lightweight authoring package. Later analysis may run here only after its required dependencies are declared in project configuration and the shared lock. JSON, images and videos can be reviewed without the ML runtime; `.npz`/tensor inspection needs its actual loader dependencies or must be performed on the target with a returned summary. Do not install the Linux runtime extra on the coding computer to satisfy an analysis import.

## Target setup: commands awaiting verification

Complete the target inventory in Week 1 Session 1 first. The following is the candidate setup for Ubuntu 24.04 with Python 3.12. Replace the example checkout path below with your verified handoff directory. Record the actual distribution before installing OS packages. Review differences if your Ubuntu release is different.

```bash
sudo apt-get update
sudo apt-get install -y python3.12-venv build-essential ffmpeg libegl1 libgl1 libgles2 libglib2.0-0
cd ~/projects/vla-grounding-proj
python3.12 -m venv .venv
.venv/bin/python -m pip install '.[tools]'
.venv/bin/uv sync --locked --extra tools --extra runtime --no-dev
```

Use the Windows host NVIDIA driver following the [official WSL guidance](https://docs.nvidia.com/cuda/wsl-user-guide/index.html). Python wheels supply their CUDA runtime; this setup does not require installing a Linux NVIDIA display driver. `uv.lock` fixes Python packages, while OS packages and the host driver must be recorded from the actual target. Keep LIBERO-plus in a different environment later.

Run these stages in order, from the target checkout root. Keep a common development run directory and use new directories for reruns:

```bash
.venv/bin/vla-target-check --config configs/week-01.json --output artifacts/week-01/run-01/cuda.json
.venv/bin/vla-fetch-assets --config configs/week-01.json --output artifacts/week-01/run-01/assets.json
.venv/bin/vla-render-smoke --config configs/week-01.json --assets artifacts/week-01/run-01/assets.json --output-dir artifacts/week-01/run-01/render
.venv/bin/vla-policy-smoke --config configs/week-01.json --assets artifacts/week-01/run-01/assets.json --output-dir artifacts/week-01/run-01/policy
```

1. **CUDA check:** rejects another platform, a Windows-mounted checkout, another GPU, insufficient configured disk space, or unavailable CUDA. It performs a matrix multiplication on the selected GPU and saves interpreter, kernel, driver, memory, disk, and key package information. This is a CUDA gate, not the whole Week 1 gate.
2. **Asset fetch:** downloads simulator assets, policy weights and saved processors, plus VLM configuration/tokenizer files. The policy commit is fixed in `configs/week-01.json`. The other initial references are resolved to full commit hashes before download; reuse the resulting manifest, rather than resolving `main` again for the same run. No demonstration dataset or separate VLM weights are needed for this smoke check. This step uses network access and Hub progress bars, with bounded retries and warnings for transport/HTTP failures.
3. **Rendering check:** runs a fresh task reset without loading the policy. Inspect `image.png` (main camera), `image2.png` (wrist camera), and `observation.npz`. PNGs use the upstream 180-degree orientation correction; saved raw image arrays retain their native orientation. The eight-value state in this file is already constructed by the environment processor, before policy normalization.
4. **Policy check:** saves `prediction.npz`, `executed-actions.npz`, `smoke.mp4`, and `smoke.json`. It loads the full checkpoint strictly from local snapshots, uses its saved normalizers and tokenizer settings, and runs LeRobot's upstream bounded rollout. It validates finite decoded actions before stepping and decodes the MP4 after writing. The agent must inspect playback or rendered video frames and document the review: successful decoding does not verify meaningful motion or correct orientation.

The smoke task, seed, image size, step budget, control frequency, GPU and download references are explicit in the shared configuration. Its short step budget is an interface diagnostic, not an evaluation horizon or task-success measurement. Do not reuse it for the main study's episode limits.

## Connector and evidence contract

`bootstrap.py` sets EGL, its device index, and an isolated `LIBERO_CONFIG_PATH` before simulator imports. It writes JSON-compatible YAML non-interactively. In hf-libero 0.1.4, `get_assets_path()` independently looks beside the installed module, so the bootstrap links the pinned snapshot into the **project virtual environment's** native assets location. It refuses to replace an existing directory or a link to a different snapshot. No vendor Python is patched. Recreate generated files when rebuilding the target environment; do not transfer them between machines.

Runtime connectors load only local snapshots after bootstrap and disable Hub network access, telemetry and external experiment tracking. Loading the full SmolVLA checkpoint supplies backbone weights; initializing its architecture from the pinned local VLM configuration avoids a redundant backbone-weight download. The saved policy processors retain normalization and action unnormalization. The camera rename mapping is explicit and checked against the pinned public feature contract.

The data path is raw HWC uint8 camera batches and native robot state → LeRobot image conversion and LIBERO orientation/pose processing → checkpoint rename, tokenization and normalization → SmolVLA chunk → checkpoint action decoding → simulator. Public state/action widths are eight/seven; internal model padding and image resizing happen inside upstream SmolVLA.

`prediction.npz` contains both raw cameras, native end-effector position/quaternion and gripper positions, processed policy tensors, a normalized predicted chunk, and its decoded first action. The command recreates the simulator and resets policy/processors and sampling seed before the upstream rollout. It checks that the saved first action matches the first executed action within numerical tolerance. `executed-actions.npz` contains the actual short rollout actions. Use `smoke.json` to recover instruction, mapping, action settings, configuration, revisions, hardware and artifact relationships. These are development artifacts, not experiment results or a frozen evaluation manifest.

The observation inspector and canonical episode loop are implemented. The inspector uses the runtime's existing NumPy dependency; the lightweight Windows project environment does not install the Linux runtime. A separate declared analysis environment is required for portable NPZ inspection. The [code guide](CODE_GUIDE.en.md) explains the current structures and is updated with each implementation.

## Week 1 audit and Week 2 pilot commands

Week 1 source now includes the previously missing [observation inspector](../src/vla_grounding/inspection.py). Both render/policy smoke commands save `inspection.json` automatically. For a separate audit in an environment with NumPy installed:

```bash
.venv/bin/vla-inspect-arrays --input artifacts/week-01/run-01/policy/prediction.npz --output artifacts/week-01/run-01/policy/inspection-review.json
```

The [canonical episode command](../src/vla_grounding/episode.py) uses an explicit case rather than the short smoke horizon. Its input contract and queue/trace design are explained in the [code guide](CODE_GUIDE.en.md#week-1-inspection-and-week-2-episode-implementation). Run it only after the real Week 1 target gates pass. The three supplied cases are development inputs, with target-resolved state evidence still pending.

The following **target-only commands are unverified here**. Each smoke command executes `vla_grounding.episode` in a real subprocess and audits its returned chunks/actions/frames; use fresh output directories.

```bash
.venv/bin/python tests/smoke_episode.py --config configs/week-01.json --case configs/week-02-case-00.json --assets artifacts/week-01/run-01/assets.json --output-dir artifacts/week-02/run-01/pilot-00
.venv/bin/python tests/smoke_episode.py --config configs/week-01.json --case configs/week-02-case-01.json --assets artifacts/week-01/run-01/assets.json --output-dir artifacts/week-02/run-01/pilot-01
.venv/bin/python tests/smoke_episode.py --config configs/week-01.json --case configs/week-02-case-02.json --assets artifacts/week-01/run-01/assets.json --output-dir artifacts/week-02/run-01/pilot-02
```

Direct command contract: `vla-run-episode --config <config.json> --case <case.json> --assets <assets.json> --output-dir <fresh-directory>`. This is one canonical development episode, with no batch mode, resumption or changed-goal scoring.

A completed run has `episode.json`, state records, per-step NPZ/JSON, full predicted chunks and a video. `request.json` remains unchanged and initially incomplete; only the final result marks completion. On an infrastructure exception retain the existing request/state/transitions and original error, and rerun in a fresh directory after correction. A timeout is a completed unsuccessful outcome; it does not invalidate the infrastructure.

Portable evidence checks in an environment with NumPy/Pydantic:

```bash
python tests/smoke_evidence.py --cases-dir configs
```

The normal project authoring smoke and Ruff checks pass on Windows. The additional portable evidence smoke passed using the bundled Python 3.12 / NumPy 2.3.5 interpreter with the source path explicit. This does not verify the target lock's NumPy build, CUDA or policy/simulator integration. New dependency resolution/download attempts timed out at the configured PyPI/PyTorch endpoints; no package pins, registry sources or lock contents were substituted. `uv lock --check --offline` validates the unchanged lock. Strict static type-checker execution is still pending an available configured tool; no such pass is claimed.

## Troubleshooting and completion

| Failure | Inspect and correct |
| --- | --- |
| Python alias or wrong interpreter | Locate Python 3.12; inspect `sys.executable`; invoke the checkout's environment explicitly. |
| Lock resolution or installation | Preserve the full error. Use the checked-in lock and its supported platforms; do not remove version pins to make installation appear successful. |
| CUDA failure | Compare target host `nvidia-smi`, WSL distribution/kernel and wheel CUDA; the coding machine's GPU is irrelevant. |
| Hub download failure | Preserve repository, revision, HTTP status/body and final exception. Fix connectivity/authentication, then create a fresh run manifest or reuse completed snapshots. |
| LIBERO config or asset conflict | Inspect the reported target paths and linked revision. Use a fresh project environment if those files belong to a different installation. |
| EGL or blank-camera failure | Inspect WSL GPU exposure, EGL system libraries, selected device and simulator assets before loading the policy. Do not substitute another rendering backend. |
| Feature or processor mismatch | Compare the local checkpoint config and both processor JSON files against the saved mapping. Retain the normalizer state files. |
| First-action mismatch | Investigate reset state, sampler seed and preprocessing; preserve the partial artifacts and error. Do not call it a verified trace. |
| MP4 failure | Inspect the original encoding/decoding exception and PyAV/FFmpeg installation. Keep partial files for diagnosis and rerun into a fresh output directory. |

Save exact commands and failures. Mark the corresponding bilingual weekly checklist complete only after its real evidence exists; include the agent's documented data-flow diagram, verified inspector, tensor explanation and visual playback/frame review alongside the machine-generated reports.

Sources: [published LeRobot 0.6.1](https://pypi.org/project/lerobot/0.6.1/), [published hf-libero 0.1.4](https://pypi.org/project/hf-libero/0.1.4/), [TorchCodec compatibility](https://github.com/meta-pytorch/torchcodec/releases/tag/v0.10.0), [pinned checkpoint processors](https://huggingface.co/lerobot/smolvla_libero/tree/a24f1f380461b665158d52acd140152c79e8b36d).
