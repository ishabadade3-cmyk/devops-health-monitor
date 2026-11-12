# DevOps Health Monitor

A beginner-friendly Flask project that demonstrates the path from source code to automated tests and a Docker image. GitHub Actions runs the tests and builds the image when code is pushed to `main` or a pull request targets `main`.

> **Scope:** This project builds and tests a Docker image. It does not publish the image to Docker Hub or deploy to a cloud server.

## What problem does it solve?

It gives a small web service a clear health-check URL and a repeatable way to verify and package changes. In a larger system, a monitor or load balancer can call the health URL to check whether the service responds.

## Project objectives

- Serve a simple status dashboard and a JSON health endpoint.
- Test the important HTTP behavior with pytest.
- Package the service in a small Linux container that runs as a non-root user.
- Use GitHub Actions to test the application and build the Docker image on code changes.
- Practice Git, GitHub, logs, and health-check concepts without a complicated cloud setup.

## Technology stack

| Tool | Purpose |
| --- | --- |
| Python 3.12 | Application language |
| Flask | Web framework and `/health` endpoint |
| Gunicorn | Production-style WSGI server inside the container |
| Pytest | Automated tests |
| Docker | Reproducible application container |
| Git and GitHub | Source history and collaboration |
| GitHub Actions | Automated test and image-build workflow |
| PowerShell | Windows command line |

## How it fits together

The browser requests the Flask homepage, while a health checker can request `GET /health`. Pytest exercises both routes. A push or pull request to `main` starts GitHub Actions; the workflow installs the Python dependencies, runs pytest, and builds a Docker image. The workflow does not deploy the image.

## Project structure

```text
devops-health-monitor/
├── app.py
├── test_app.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── README.md
├── static/
│   └── style.css
├── templates/
│   └── index.html
└── .github/
    └── workflows/
        └── ci.yml
```

## Run locally on Windows

Install Python 3.12 and Git if they are not already installed. In PowerShell, move into the project directory:

```powershell
cd C:\path\to\devops-health-monitor
```

Create and activate a virtual environment. It keeps this project's Python packages separate from other projects:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the environment's Python directly as shown below, or temporarily allow scripts in the current PowerShell process with `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.

Install application and test dependencies:

```powershell
python -m pip install -r requirements-dev.txt
```

Start the local development server:

```powershell
python app.py
```

Open [http://localhost:5000](http://localhost:5000) for the dashboard and [http://localhost:5000/health](http://localhost:5000/health) for the health response. Stop the local server with **Ctrl+C**.

The same commands can be run without activating the environment:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe app.py
```

## Run automated tests

With the virtual environment active:

```powershell
python -m pytest -v
```

Or call pytest through the environment explicitly:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

The tests verify that the homepage responds successfully and includes the project name, and that `/health` returns HTTP 200 with the expected JSON.

## Build and run with Docker

Make sure Docker Desktop is installed and its Linux engine is running. From the project directory, build the image:

```powershell
docker build -t devops-health-monitor:1.0 .
```

Run the container in the foreground and map host port 8080 to container port 5000:

```powershell
docker run --rm -p 8080:5000 devops-health-monitor:1.0
```

Visit [http://localhost:8080](http://localhost:8080) and [http://localhost:8080/health](http://localhost:8080/health). The container runs Gunicorn as the unprivileged `appuser`; Docker's health check calls `/health`. Stop it with **Ctrl+C**.

To see health and application output from another PowerShell window:

```powershell
docker ps
docker inspect --format='{{.State.Health.Status}}' <container-id>
docker logs <container-id>
```

`docker run --rm` removes the container after it stops. Omit `--rm` if you want to inspect a stopped container later.

## Git and GitHub

The local Git repository and GitHub remote are already configured for this project. For future changes:

```powershell
git status
git add .
git commit -m "Describe the change"
git push origin main
```

`git status` shows which files changed, `git add` stages selected changes, `git commit` saves a local snapshot, and `git push` sends commits to GitHub. Never commit passwords, tokens, or `.env` files; `.gitignore` excludes local environments, caches, and secret environment files.

The configured remote is `https://github.com/ishabadade3-cmyk/devops-health-monitor`. Repository visibility is managed on GitHub; check it before pushing if the source should be private.

## GitHub Actions

The workflow is `.github/workflows/ci.yml`. It runs for pushes to `main` and pull requests targeting `main`. Its steps:

1. Check out the repository.
2. Set up Python 3.12 and cache pip downloads.
3. Install `requirements-dev.txt`.
4. Run `python -m pytest -v`.
5. Build a Docker image tagged with the commit SHA.

To inspect a run, open the repository on GitHub, select **Actions**, and choose the workflow run. A green check means the workflow steps succeeded; a red cross means a step needs attention. The tests run before the image build, so a failed test stops the job before the build. The workflow only builds the image; it does not push or deploy it.

## Monitoring, health checks, and logs

- **Health check:** `/health` is a quick application-level HTTP response. Docker also uses it to set the container's health state.
- **Application monitoring:** Observes application behavior, such as whether this service answers health requests. This project demonstrates a simple check, not a full monitoring platform.
- **Infrastructure monitoring:** Observes the machine or platform running the service, for example CPU, memory, disk, and network availability. It is not configured here.
- **Logging:** Records events and errors. Application messages go to standard output/error so they can be viewed with `docker logs`.

An HTTP 200 health response does not prove that every external dependency or the underlying host is healthy; this example has no external dependencies to check.

## Common errors

| Error | What to try |
| --- | --- |
| `python` or `py` is not recognized | Install Python 3.12 and reopen PowerShell. Check with `py --version`. |
| `ModuleNotFoundError: No module named 'flask'` | Activate `.venv`, then run `python -m pip install -r requirements-dev.txt`. Make sure VS Code uses `.venv\Scripts\python.exe`. |
| PowerShell refuses to activate `.venv` | Run the explicit `.venv\Scripts\python.exe` commands above, or set the execution policy for the current process only. |
| Port 5000 or 8080 is already in use | Stop the other process, or use another host port, for example `-p 8081:5000`. |
| Docker says it cannot connect to the daemon | Start Docker Desktop, wait for the Linux engine to report running, then retry `docker info`. |
| Container starts but the page is unavailable | Check `docker ps` and `docker logs <container-id>`, confirm the port mapping, and make sure the container is healthy. |
| Git push is rejected or authentication fails | Check `git status` and `git remote -v`; sign in through Git Credential Manager or your approved GitHub authentication method. Do not paste credentials into chat. |
| A GitHub Actions run fails | Open the failed run under **Actions**, expand the first failing step, and use its error output to diagnose the cause. |

## Limitations and future improvements

This is a learning example: it has no database, authentication, deployment target, image registry publishing, HTTPS termination, or external monitoring service. The dashboard's “Running” label describes the web page being served; use `/health` for the actual HTTP check.

Possible next steps are to add a deployment workflow after choosing a hosting platform, publish versioned images to a registry, add integration checks, and monitor host metrics with a dedicated platform. Add secrets only through the hosting or GitHub Actions secret manager, never in source code.

## Two-minute project demonstration

> “This is DevOps Health Monitor, a small Flask service with a dashboard and a `/health` endpoint. The health endpoint returns a status and message in JSON, which makes it easy for a person or a monitoring system to check whether the app responds.
>
> I use pytest to check the homepage and exact health response. Docker packages the app with its dependencies and runs it as a non-root user using Gunicorn. The image includes a Docker health check, and I can inspect application output with `docker logs`.
>
> GitHub Actions automates the repeatable checks. When I push to `main` or open a pull request targeting `main`, it checks out the code, installs Python 3.12 dependencies, runs the tests, and builds a Docker image tagged with the commit SHA. A failing test stops the pipeline before the image is built.
>
> This is CI: continuous integration, not automatic production deployment. A future improvement would be to select a hosting platform and add a separate deployment workflow, then add external monitoring and alerts.”

## DevOps concepts demonstrated

- **Version control:** Git records changes; GitHub hosts the repository.
- **Automated testing:** pytest checks expected behavior consistently.
- **Containerization:** Docker packages an app and its runtime dependencies.
- **Continuous integration:** GitHub Actions automatically tests each qualifying change.
- **Health checks and logs:** `/health` reports basic app availability; container logs expose application output.
- **Deployment boundary:** Building an image is not the same as publishing or deploying it.
