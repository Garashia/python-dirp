# python-dirp publish playbook

This document reflects:

- `.github/workflows/publish.yml`

`Publish PyPI` now builds and smoke-tests platform wheels (Windows/Linux/macOS), builds sdist, and publishes all artifacts together.

## Preconditions

- `pyproject.toml` project name is `py-dirp`
- `dirp_core` submodule is available
- Trusted Publisher is configured on both:
  - TestPyPI (`test.pypi.org`)
  - PyPI (`pypi.org`)
- Publisher values match exactly:
  - Owner: `Garashia`
  - Repository: `python-dirp`
  - Workflow: `publish.yml`
  - Branch: `main`

## 0) Version bump

- Update `pyproject.toml`: `version = "X.Y.Z"`
- Commit and push to `main`

## 1) Publish to TestPyPI (required)

Run workflow:

- Workflow: `Publish PyPI`
- Input: `repository=testpypi`

What the workflow does:

- Build wheels on `ubuntu-latest`, `windows-latest`, `macos-latest`
- Smoke test each built wheel (`import dirp` + parse sample)
- Build sdist
- Publish wheels + sdist to TestPyPI

If any build/smoke step fails, fix before production publish.

## 2) Quick install check from TestPyPI

```bash
python -m venv .venv-test
. .venv-test/bin/activate  # Windows PowerShell: .\.venv-test\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple py-dirp==X.Y.Z
python -c "import dirp; print(dirp.parse('app{src,bin}'))"
```

## 3) Publish to PyPI (production)

Run workflow:

- Workflow: `Publish PyPI`
- Input: `repository=pypi`

Optional tag:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

## 4) Production verification

```bash
python -m venv .venv-prod
. .venv-prod/bin/activate  # Windows PowerShell: .\.venv-prod\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install py-dirp==X.Y.Z
python -c "import dirp; print(dirp.parse('app{src,bin}'))"
```

Project page:

- `https://pypi.org/project/py-dirp/`

## Troubleshooting

- `invalid-publisher`
  - Trusted Publisher mismatch (owner/repo/workflow/branch).
- Wheel build or smoke-test failure on one OS
  - Check `Publish PyPI` logs for that matrix job and fix before publish.
