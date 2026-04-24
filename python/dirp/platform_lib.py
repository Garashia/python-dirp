from __future__ import annotations

import sys


def platform_library_names() -> list[str]:
    if sys.platform.startswith("win"):
        return ["dirp.dll", "libdirp.dll"]
    if sys.platform == "darwin":
        return ["libdirp.dylib"]
    return ["libdirp.so"]


def default_platform_library_name() -> str:
    return platform_library_names()[0]
