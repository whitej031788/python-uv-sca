# python-uv demo

Minimal project to test SCA parsing of `uv.lock` and alternative lockfiles.

## Using uv

Assuming you have `uv` installed (https://github.com/astral-sh/uv):

```bash
# Create a new virtual env and sync dependencies
uv venv .venv
source .venv/bin/activate
uv pip compile pyproject.toml -o uv.lock || true
uv pip sync uv.lock

# Run server
uvicorn app:app --reload
```

If your SCA tool can read `uv.lock`, scan now.

## Alternative lockfiles

If your SCA tool cannot parse `uv.lock`, generate other formats:

### requirements.txt (from installed env)
```bash
pip freeze > requirements.txt
```

### pip-tools style lock (if installed)
```bash
pip install pip-tools
pip-compile pyproject.toml -o requirements.txt
```

### Poetry
```bash
pip install poetry
poetry init --no-interaction --name python-uv-demo --dependency fastapi==0.114.0 --dependency uvicorn==0.30.6 --dependency requests==2.32.3 --dependency pydantic==2.8.2 --dependency pytest==8.3.2
poetry lock
```
This creates `poetry.lock`.

### Pipenv
```bash
pip install pipenv
pipenv install fastapi==0.114.0 uvicorn==0.30.6 requests==2.32.3 pydantic==2.8.2 pytest==8.3.2
# Generates Pipfile and Pipfile.lock
```

## Test
```bash
pip install pytest
pytest -q
```
