# py-dirp

Python bindings for the Go implementation of `dirp`.

## Install

```bash
pip install py-dirp
```

## Usage

```python
from dirp import parse, build

nodes = parse("app{src,bin}")
build("tmp-out", "app{src,bin}")
```

## Development

This repository uses `dirp_core` as a submodule.

```bash
git submodule update --init --recursive
python -m pip install -U build
python -m build
```

For Windows-specific release/build guidance, see `WINDOWS_RELEASE_INSTRUCTIONS.md` (local note, ignored in git).
