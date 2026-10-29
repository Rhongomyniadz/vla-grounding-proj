"""Prepare the pinned LIBERO installation before its first interactive import."""

import json
import os
import sys
from importlib.metadata import distribution
from pathlib import Path

from vla_grounding.assets import Snapshot
from vla_grounding.runtime import require_target_platform


def prepare_simulator(workspace: Path, assets: Snapshot, cuda_device: int) -> Path:
    """Configure EGL and bind frozen assets using LIBERO's local-assets interface.

    hf-libero 0.1.4 reads assets beside its installed module, independently of
    config.yaml. A symlink in this project's virtual environment supplies that
    supported local layout without editing vendor Python or downloading main.
    """
    require_target_platform(workspace)
    if any(name in sys.modules for name in ("libero", "mujoco", "OpenGL")):
        raise RuntimeError(
            "Prepare LIBERO paths and EGL before importing libero, mujoco, or OpenGL."
        )
    prefix = Path(sys.prefix).resolve()
    if prefix != (workspace / ".venv").resolve():
        raise RuntimeError(f"Use this checkout's .venv interpreter; current prefix={prefix}")
    package = distribution("hf-libero")
    if package.version != "0.1.4":
        raise RuntimeError(f"Expected hf-libero==0.1.4; installed={package.version}")
    root = Path(package.locate_file("libero/libero")).resolve()
    if not root.is_relative_to(prefix):
        raise RuntimeError(f"LIBERO must be installed in the project environment: {root}")
    snapshot = Path(assets.path).resolve()
    for name in ("articulated_objects", "scenes", "stable_hope_objects", "stable_scanned_objects"):
        if not (snapshot / name).is_dir():
            raise FileNotFoundError(
                f"Incomplete LIBERO asset snapshot {assets.revision}: {snapshot / name}"
            )
    local_assets = root / "assets"
    if local_assets.is_symlink():
        if local_assets.resolve() != snapshot:
            raise RuntimeError(
                f"LIBERO assets already point elsewhere: {local_assets} -> {local_assets.resolve()}"
            )
    elif local_assets.exists():
        raise FileExistsError(
            f"Existing LIBERO assets cannot be replaced automatically: {local_assets}"
        )
    else:
        local_assets.symlink_to(snapshot, target_is_directory=True)
    paths: dict[str, str] = {
        "benchmark_root": str(root),
        "bddl_files": str(root / "bddl_files"),
        "init_states": str(root / "init_files"),
        "datasets": str(workspace / ".runtime" / "datasets"),
        "assets": str(snapshot),
    }
    Path(paths["datasets"]).mkdir(parents=True, exist_ok=True)
    for name, value in paths.items():
        if not Path(value).is_dir():
            raise FileNotFoundError(f"LIBERO {name} directory is missing: {value}")
    config_dir = workspace / ".runtime" / "libero"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "config.yaml"
    content = json.dumps(paths, indent=2) + "\n"
    if config_file.exists():
        if config_file.read_text(encoding="utf-8") != content:
            raise RuntimeError(
                f"Existing LIBERO configuration differs from this environment: {config_file}"
            )
    else:
        config_file.write_text(content, encoding="utf-8")
    os.environ["LIBERO_CONFIG_PATH"] = str(config_dir)
    os.environ["MUJOCO_GL"] = "egl"
    os.environ["PYOPENGL_PLATFORM"] = "egl"
    os.environ["MUJOCO_EGL_DEVICE_ID"] = str(cuda_device)
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    os.environ["WANDB_MODE"] = "disabled"
    return config_file
