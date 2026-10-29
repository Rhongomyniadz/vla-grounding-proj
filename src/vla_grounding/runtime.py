"""Check the Linux execution machine before simulator or policy allocation."""

import argparse
import platform
import shutil
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path

from vla_grounding.config import WeekOneConfig, read_config
from vla_grounding.evidence import JsonValue, write_report


def require_target_platform(workspace: Path) -> None:
    """Reject Windows Python and Windows-mounted target checkouts explicitly."""
    if sys.platform != "linux":
        raise RuntimeError(
            f"Run this command on the RTX 5080 machine inside Ubuntu/WSL2; "
            f"current platform={sys.platform}, executable={sys.executable}. "
            "Use vla-author-check on the coding machine."
        )
    if "microsoft-standard-WSL2" not in platform.release():
        raise RuntimeError(f"Expected the WSL2 Linux kernel; received {platform.release()}")
    if platform.machine() != "x86_64":
        raise RuntimeError(
            f"The target dependency lock requires x86_64; received {platform.machine()}"
        )
    if workspace.resolve().is_relative_to(Path("/mnt")):
        raise RuntimeError(
            f"Target checkout must be in the Linux filesystem: {workspace.resolve()}"
        )
    if sys.version_info[:2] != (3, 12):
        raise RuntimeError(f"Target runtime requires Python 3.12; received {sys.version}")


def check_target(config: WeekOneConfig, workspace: Path) -> dict[str, JsonValue]:
    """Execute real CUDA matrix multiplication and retain target machine evidence."""
    require_target_platform(workspace)
    free_gib = shutil.disk_usage(workspace).free / 1024**3
    if free_gib < config.minimum_free_disk_gib:
        raise RuntimeError(
            f"Workspace {workspace} has {free_gib:.1f} GiB free; "
            f"requires {config.minimum_free_disk_gib} GiB before model/assets installation."
        )
    if version("lerobot") != "0.6.1":
        raise RuntimeError(f"Expected lerobot==0.6.1; installed={version('lerobot')}")

    import torch

    if not torch.cuda.is_available():
        raise RuntimeError(
            f"CUDA unavailable in {sys.executable}; torch={torch.__version__}, "
            f"wheel CUDA={torch.version.cuda}. Check the Windows NVIDIA driver and WSL GPU access."
        )
    device = torch.device(f"cuda:{config.cuda_device}")
    actual_gpu = torch.cuda.get_device_name(device)
    if actual_gpu != config.expected_gpu:
        raise RuntimeError(
            f"Unexpected GPU at {device}: expected={config.expected_gpu}, actual={actual_gpu}."
        )
    matrix = torch.ones((32, 32), device=device)
    result = (matrix @ matrix).mean().item()
    torch.cuda.synchronize(device)
    if result != 32.0:
        raise ArithmeticError(f"CUDA matrix multiplication failed: expected=32.0, actual={result}")
    driver = subprocess.run(
        ["nvidia-smi", "--query-gpu=name,driver_version,memory.total", "--format=csv,noheader"],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    packages: dict[str, JsonValue] = {
        name: version(name)
        for name in ("lerobot", "hf-libero", "torch", "torchvision", "torchcodec", "mujoco")
    }
    return {
        "scope": "target-cuda-only",
        "python": sys.version,
        "executable": sys.executable,
        "kernel": platform.release(),
        "os_release": Path("/etc/os-release").read_text(encoding="utf-8"),
        "workspace": str(workspace.resolve()),
        "free_disk_gib": free_gib,
        "gpu": actual_gpu,
        "cuda_device": str(device),
        "wheel_cuda": torch.version.cuda,
        "cuda_result": result,
        "nvidia_smi": driver.stdout.strip(),
        "packages": packages,
        "rendering_verified": False,
        "policy_verified": False,
    }


def main() -> None:
    """Write CUDA evidence only after all target checks pass."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = check_target(read_config(args.config), Path.cwd())
    write_report(args.output, report)
    print(
        f"Target CUDA check passed; rendering and policy still require smoke checks: {args.output}"
    )


if __name__ == "__main__":
    main()
