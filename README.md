# DD Recovery OS

[![CI Testing](https://github.com/EmmanuelDareus/dd-recovery-os/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/EmmanuelDareus/dd-recovery-os/actions/workflows/pytest.yml)

A small FastAPI prototype with a string-processing engine and an in-memory content-project tracker. Despite the repository name, the current code does not implement recovery or persistent storage features.

## What it does

- `POST /process` passes a string to `CoreEngine`, which returns the original string and its reversed form.
- `POST /content/project` creates a content project with a platform, stage, and empty asset list.
- `GET /content/projects` lists projects created during the current process.
- `POST /content/stage` changes a project's stage to `Scripting`, `Editing`, `Thumbnail`, `Ready`, or `Published`.
- `GET /` reports the API and engine status.

The project and engine state lives in memory and is lost when the process stops. There is no database, authentication, or asset persistence, so this is a local/demo starting point rather than a production-ready service.

## Requirements

The repository does not declare a Python support range or pin dependencies. Its GitHub Actions workflow and Dev Container specify Python 3.11; that is the only version currently configured by the project.

From the repository root, create and activate a virtual environment, then install the same packages used by CI:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi uvicorn pytest httpx
```

On macOS or Linux, activate the environment with:

```sh
source .venv/bin/activate
```

`requirements.txt` is currently empty, so it does not install or pin these packages.

## Run the API

From the repository root, start the FastAPI app:

```sh
python main.py
```

It starts Uvicorn with reload enabled at `http://127.0.0.1:8000`. FastAPI's interactive API documentation is available at `http://127.0.0.1:8000/docs`.

The Dev Container's current `postAttachCommand` instead runs `streamlit run app.py`, which starts a separate ToonFit demo and does not launch this API.

## Tests

Run the same test command used by GitHub Actions:

```sh
python -m pytest
```

The checked-in tests currently expect `status` and `processed_data` fields from `CoreEngine.process`, while the implementation returns `input`, `processed`, and `engine`. The API test also expects the input string unchanged, although the implementation reverses it. The test expectations therefore do not match the current implementation.

## Configuration and logs

`config.py` derives the project root from its own location and creates the `src/core`, `src/utils`, `src/integrations`, and `tests` directories when imported. The API's logger writes to standard output and appends to `logs/app.log`; it creates the `logs` directory if needed. The `/process` handler logs the submitted string, so do not send sensitive values to this demo.
