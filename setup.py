from __future__ import annotations

import importlib.util
from pathlib import Path
from setuptools import setup
from setuptools.dist import Distribution
from setuptools.command.build_py import build_py as _build_py

ROOT = Path(__file__).resolve().parent


class BinaryDistribution(Distribution):
    """Treat package as platform-specific so wheel uses platlib."""

    def has_ext_modules(self) -> bool:
        return True


def _build_go_shared_library() -> None:
    script_path = ROOT / "python" / "build_go_lib.py"
    spec = importlib.util.spec_from_file_location("build_go_lib", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load build helper: {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.build_go_shared_library(ROOT)


class build_py(_build_py):
    def run(self) -> None:
        _build_go_shared_library()
        super().run()


try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
except Exception:  # pragma: no cover
    _bdist_wheel = None


if _bdist_wheel is not None:
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self) -> None:
            super().finalize_options()
            # Wheel contains platform-specific shared library.
            self.root_is_pure = False

        def run(self) -> None:
            _build_go_shared_library()
            super().run()

    cmdclass = {"build_py": build_py, "bdist_wheel": bdist_wheel}
else:
    cmdclass = {"build_py": build_py}


setup(cmdclass=cmdclass, distclass=BinaryDistribution)
