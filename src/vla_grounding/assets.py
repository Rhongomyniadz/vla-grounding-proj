"""Resolve Hub references once and download immutable local snapshots."""

import argparse
import logging
import time
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from vla_grounding.config import read_config
from vla_grounding.evidence import write_report
from vla_grounding.runtime import require_target_platform


class Snapshot(BaseModel):
    """Required identity and target-local location of one external Hub snapshot."""

    model_config = ConfigDict(strict=True, frozen=True, extra="ignore")

    repo_id: str
    revision: Annotated[str, Field(pattern=r"^[0-9a-f]{40}$")]
    path: str


class AssetBundle(BaseModel):
    """Target-local immutable inputs to the simulator and policy connectors."""

    model_config = ConfigDict(strict=True, frozen=True, extra="ignore")

    policy: Snapshot
    vlm: Snapshot
    simulator: Snapshot


def download_snapshot(
    repo_id: str,
    revision: str,
    repo_type: Literal["model", "dataset"],
    cache_dir: Path,
    patterns: list[str],
) -> Snapshot:
    """Retry transient Hub failures three times, then preserve the final error."""
    import httpx
    from huggingface_hub import HfApi, snapshot_download
    from huggingface_hub.errors import HfHubHTTPError

    for attempt in range(1, 4):
        try:
            info = HfApi().repo_info(repo_id=repo_id, repo_type=repo_type, revision=revision)
            if info.sha is None:
                raise ValueError(f"Hub returned no commit SHA: repo={repo_id}, revision={revision}")
            snapshot = snapshot_download(
                repo_id=repo_id,
                repo_type=repo_type,
                revision=info.sha,
                cache_dir=str(cache_dir),
                allow_patterns=patterns,
            )
            return Snapshot(repo_id=repo_id, revision=info.sha, path=str(Path(snapshot).resolve()))
        except (httpx.TransportError, HfHubHTTPError) as error:
            error.add_note(f"repo_id={repo_id}, revision={revision}, attempt={attempt}/3")
            if attempt == 3:
                raise
            logging.getLogger(__name__).warning(
                "hub_download_retry",
                extra={
                    "repo_id": repo_id,
                    "revision": revision,
                    "attempt": attempt,
                    "error": str(error),
                },
            )
            time.sleep(attempt)
    raise RuntimeError(f"Snapshot download exhausted attempts for {repo_id}@{revision}")


def read_assets(path: Path) -> AssetBundle:
    """Validate an existing snapshot manifest without resolving moving references."""
    bundle = AssetBundle.model_validate_json(path.read_text(encoding="utf-8"))
    for snapshot in (bundle.policy, bundle.vlm, bundle.simulator):
        if not Path(snapshot.path).is_dir():
            raise FileNotFoundError(
                f"Snapshot missing on this target: {snapshot.path}. "
                "Run vla-fetch-assets on this machine; do not copy another machine's manifest."
            )
    return bundle


def main() -> None:
    """Fetch pinned policy weights, VLM metadata/tokenizer, and simulator assets."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    require_target_platform(Path.cwd())
    if args.output.exists():
        raise FileExistsError(
            f"Asset manifest already exists; reuse it or choose a new run: {args.output}"
        )
    config = read_config(args.config)
    cache = Path.cwd() / ".cache" / "hub"
    bundle = AssetBundle(
        simulator=download_snapshot(
            "lerobot/libero-assets", config.simulator_assets_revision, "dataset", cache, ["*"]
        ),
        policy=download_snapshot(
            "lerobot/smolvla_libero",
            config.policy_revision,
            "model",
            cache,
            ["*.json", "*.safetensors"],
        ),
        vlm=download_snapshot(
            "HuggingFaceTB/SmolVLM2-500M-Video-Instruct",
            config.vlm_revision,
            "model",
            cache,
            ["*.json", "*.txt", "*.model", "*.jinja"],
        ),
    )
    write_report(args.output, bundle.model_dump(mode="json"))
    print(f"Immutable revisions and target-local snapshot paths saved: {args.output}")


if __name__ == "__main__":
    main()
