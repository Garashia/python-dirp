from __future__ import annotations

import os
import subprocess
import importlib.util
from pathlib import Path


def platform_library_name(root: Path) -> str:
    script_path = root / "python" / "dirp" / "platform_lib.py"
    spec = importlib.util.spec_from_file_location("platform_lib", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load platform helper: {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.default_platform_library_name()


def _validate_root(root: Path) -> None:
    main_c = root / "main_c.go"
    if not main_c.exists():
        raise RuntimeError(f"missing Go bridge entrypoint: {main_c}")
    if not (root / "dirp_core" / "go.mod").exists():
        raise RuntimeError("missing dirp_core/go.mod; submodule may not be initialized")


def build_go_shared_library(root: Path) -> Path:
    _validate_root(root)
    out_dir = root / "python" / "dirp"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / platform_library_name(root)

    env = os.environ.copy()
    env.setdefault("CGO_ENABLED", "1")

    cmd = [
        "go",
        "build",
        "-buildmode=c-shared",
        "-o",
        str(out_path),
        "main_c.go",
    ]
    try:
        subprocess.run(
            cmd,
            cwd=str(root),
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError("Go toolchain not found in PATH") from exc
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "failed to build Go shared library.\n"
            f"command: {' '.join(cmd)}\n"
            f"stdout:\n{exc.stdout}\n"
            f"stderr:\n{exc.stderr}"
        ) from exc

    return out_path
