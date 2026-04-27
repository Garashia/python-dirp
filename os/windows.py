from __future__ import annotations


def is_target_platform(sys_platform: str) -> bool:
    return sys_platform.startswith("win")
