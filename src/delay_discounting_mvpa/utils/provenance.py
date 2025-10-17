import os
import json
import socket
import subprocess
from datetime import datetime
import argparse


def get_git_commit_hash() -> str:
    """Return the short git commit hash for the current repo."""
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "unknown"


def is_git_dirty() -> bool:
    """Return True if there are uncommitted changes in the repo."""
    try:
        result = subprocess.check_output(
            ["git", "status", "--porcelain"], stderr=subprocess.DEVNULL
        ).decode().strip()
        return bool(result)
    except Exception:
        return False


def write_provenance(output_dir: str, analysis_name: str, extra_info: dict | None = None):
    """Write a provenance file to the output directory."""
    os.makedirs(output_dir, exist_ok=True)
    provenance_path = os.path.join(output_dir, f"z_provenance_{analysis_name}.json")

    data = {
        "analysis": analysis_name,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "git_commit": get_git_commit_hash(),
        "git_dirty": is_git_dirty(),
        "hostname": socket.gethostname(),
    }

    if extra_info:
        data.update(extra_info)

    with open(provenance_path, "w") as f:
        json.dump(data, f, indent=2)

    return provenance_path


# Allow running from command line
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Write provenance file to output dir")
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--analysis_name", required=True)
    parser.add_argument("--extra_info", type=json.loads, default="{}")
    args = parser.parse_args()

    write_provenance(args.output_dir, args.analysis_name, args.extra_info)
