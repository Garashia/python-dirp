# py-dirp

`py-dirp` is a Python binding package for the Go implementation of `dirp`.

## Install

- End users: `pip install py-dirp`
- Development (from this repository root): `pip install -e .`

By default, package build automatically compiles the Go shared library.

## Use

```python
from dirp import parse, build

nodes = parse("app{src,bin}")
build("tmp-out", "app{src,bin}")
```

## Requirements for source builds

- Go toolchain in `PATH`
- C compiler for cgo (`CGO_ENABLED=1`)
- Initialized `dirp_core` submodule
