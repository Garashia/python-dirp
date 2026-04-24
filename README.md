# py-dirp

Python bindings for the Go implementation of `dirp`.

Go `dirp` upstream (pinned commit):
[Garashia/DIRP @ d8ac3c5](https://github.com/Garashia/DIRP/tree/d8ac3c501b69de5777ad5985c7b324d3aaea30dc)

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
