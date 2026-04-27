from __future__ import annotations

import sys
from pathlib import Path
from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

ROOT = Path(__file__).resolve().parent
COMMON = ROOT / "os" / "common.py"
WINDOWS = ROOT / "os" / "windows.py"
LINUX = ROOT / "os" / "linux.py"
MACOS = ROOT / "os" / "macos.py"

import importlib.util

common_spec = importlib.util.spec_from_file_location("setup_os_common", COMMON)
if common_spec is None or common_spec.loader is None:
    raise RuntimeError(f"failed to load setup common module: {COMMON}")
common = importlib.util.module_from_spec(common_spec)
common_spec.loader.exec_module(common)

platform_modules = {
    "windows": WINDOWS,
    "linux": LINUX,
    "macos": MACOS,
}

selected_platform = "unknown"
for name, module_path in platform_modules.items():
    spec = importlib.util.spec_from_file_location(f"setup_os_{name}", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load platform module: {module_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if mod.is_target_platform(sys.platform):
        selected_platform = name
        break


class build_py(_build_py):
    def run(self) -> None:
        common.build_go_shared_library()
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
            common.build_go_shared_library()
            super().run()

    cmdclass = {"build_py": build_py, "bdist_wheel": bdist_wheel}
else:
    cmdclass = {"build_py": build_py}


setup(cmdclass=cmdclass, distclass=common.BinaryDistribution)
