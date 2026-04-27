from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

from setuptools.dist import Distribution

ROOT = Path(__file__).resolve().parents[1]


class BinaryDistribution(Distribution):
    """Treat package as platform-specific so wheel uses platlib."""

    def has_ext_modules(self) -> bool:
        return True


def load_module(module_name: str, file_path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module: {file_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_go_shared_library() -> None:
    build_helper = ROOT / "python" / "build_go_lib.py"
    module = load_module("build_go_lib", build_helper)
    module.build_go_shared_library(ROOT)
