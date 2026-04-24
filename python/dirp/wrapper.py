from __future__ import annotations

import ctypes
import json
import os
from pathlib import Path
from typing import Any

from .platform_lib import platform_library_names


class DirpError(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        category: str | None = None,
        pos: int | None = None,
        line: int | None = None,
        col: int | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.category = category
        self.pos = pos
        self.line = line
        self.col = col


def _resolve_lib_path() -> Path:
    env_path = os.getenv("DIRP_LIB_PATH")
    if env_path:
        p = Path(env_path).expanduser().resolve()
        if p.exists():
            return p
        raise FileNotFoundError(f"DIRP_LIB_PATH not found: {p}")

    base = Path(__file__).resolve().parent
    names = platform_library_names()
    for name in names:
        p = base / name
        if p.exists():
            return p

    names_text = ", ".join(names)
    raise FileNotFoundError(
        f"dirp shared library not found next to wrapper.py (expected one of: {names_text}). "
        "Set DIRP_LIB_PATH to override."
    )


_LIB = ctypes.CDLL(str(_resolve_lib_path()))
_LIB.ParseDirpJSON.argtypes = [ctypes.c_char_p]
_LIB.ParseDirpJSON.restype = ctypes.c_void_p
_LIB.BuildDirpFromDSLJSON.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
_LIB.BuildDirpFromDSLJSON.restype = ctypes.c_void_p
_LIB.FreeCString.argtypes = [ctypes.c_void_p]
_LIB.FreeCString.restype = None


def _call_json(func: Any, *args: bytes) -> dict[str, Any]:
    ptr = func(*args)
    if not ptr:
        raise RuntimeError("dirp returned NULL")
    try:
        raw = ctypes.cast(ptr, ctypes.c_char_p).value
        if raw is None:
            raise RuntimeError("dirp returned empty response")
        return json.loads(raw.decode("utf-8"))
    finally:
        _LIB.FreeCString(ptr)


def _raise_if_error(payload: dict[str, Any]) -> None:
    if payload.get("ok"):
        return
    err = payload.get("error") or {}
    raise DirpError(
        err.get("message", "dirp error"),
        code=err.get("code"),
        category=err.get("category"),
        pos=err.get("pos"),
        line=err.get("line"),
        col=err.get("col"),
    )


def parse(dsl: str) -> list[dict[str, Any]]:
    payload = _call_json(_LIB.ParseDirpJSON, dsl.encode("utf-8"))
    _raise_if_error(payload)
    return payload.get("nodes", [])


def parse_file(path: str) -> list[dict[str, Any]]:
    text = Path(path).read_text(encoding="utf-8")
    return parse(text)


def validate(dsl: str) -> None:
    _ = parse(dsl)


def build(root: str, dsl: str) -> None:
    payload = _call_json(
        _LIB.BuildDirpFromDSLJSON,
        root.encode("utf-8"),
        dsl.encode("utf-8"),
    )
    _raise_if_error(payload)
