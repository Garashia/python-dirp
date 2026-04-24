# Release flow (0.1.0+)

## Preconditions

- Project name in `pyproject.toml` is `py-dirp`
- `dirp_core` submodule is initialized
- PyPI/TestPyPI project is created
- GitHub trusted publisher is configured for this repository

## 1) Validate on TestPyPI

1. Bump version in `pyproject.toml`
2. Push branch and confirm `Build Wheels` workflow succeeds
3. Run `Publish PyPI` workflow with `repository=testpypi`
4. Verify install:
   - `pip install -i https://test.pypi.org/simple/ py-dirp==<version>`
   - `python -c "import dirp; print(dirp.parse('app{src,bin}'))"`

## 2) Publish to PyPI

1. Tag release commit (`vX.Y.Z`)
2. Run `Publish PyPI` workflow with `repository=pypi`
3. Verify install:
   - `pip install py-dirp==<version>`
   - `python -c "import dirp; print(dirp.parse('app{src,bin}'))"`

## Notes

- Wheels are the primary distribution path (Go toolchain not required for end users).
- sdist remains as fallback for custom environments.
