# python-dirp publish playbook (copy-paste)

This document reflects the current repository workflows:

- `.github/workflows/wheels.yml`
- `.github/workflows/publish.yml`

## Current behavior (important)

- `Build Wheels` builds wheel artifacts on Windows/Linux/macOS for CI verification.
- `Publish PyPI` currently publishes **sdist only** (`python -m build --sdist`).
- `Publish PyPI` cleans `dist/` first (`rm -rf dist`) to avoid mixed-version uploads.

Because publish is sdist-only, end users may need Go/cgo toolchains when installing from source.

## Preconditions

- `pyproject.toml` has project name `py-dirp`
- `dirp_core` submodule is available
- Trusted Publisher is configured on both:
  - TestPyPI (`test.pypi.org`)
  - PyPI (`pypi.org`)
- Publisher values must exactly match:
  - Owner: `Garashia`
  - Repository: `python-dirp`
  - Workflow: `publish.yml`
  - Branch: `main`

## 0) Version bump

Edit `pyproject.toml`:

- `version = "X.Y.Z"`

Commit and push to `main`.

## 1) CI artifact validation (`Build Wheels`)

On GitHub Actions, confirm `Build Wheels` succeeds:

- `build-wheels (ubuntu-latest)`
- `build-wheels (windows-latest)`
- `build-wheels (macos-latest)`
- `build-sdist`

If any fail, fix before publish.

## 2) Publish to TestPyPI (required)

Run workflow:

- Workflow: `Publish PyPI`
- Input: `repository=testpypi`

Expected result: workflow success.

## 3) Test install from TestPyPI

Use a clean venv:

```bash
python -m venv .venv-test
. .venv-test/bin/activate  # Windows PowerShell: .\.venv-test\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple py-dirp==X.Y.Z
python -c "import dirp; print(dirp.parse('app{src,bin}'))"
```

If this fails, stop and fix before PyPI production publish.

## 4) Publish to PyPI (production)

Run workflow:

- Workflow: `Publish PyPI`
- Input: `repository=pypi`

Then optionally tag:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

## 5) Production verification

```bash
python -m venv .venv-prod
. .venv-prod/bin/activate  # Windows PowerShell: .\.venv-prod\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install py-dirp==X.Y.Z
python -c "import dirp; print(dirp.parse('app{src,bin}'))"
```

Check project page:

- `https://pypi.org/project/py-dirp/`

## Troubleshooting quick notes

- `invalid-publisher`
  - Trusted Publisher mismatch on PyPI/TestPyPI.
  - Re-check owner/repo/workflow/branch exact values.
- `linux_x86_64 wheel unsupported`
  - Expected if trying to upload non-manylinux wheel.
  - Current publish is sdist-only by design.
- Mixed versions in upload
  - `publish.yml` already cleans `dist/`; ensure workflow uses latest `main`.
