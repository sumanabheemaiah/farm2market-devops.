# Farm2Market DevOps Project Handbook

**Beginner Project Documentation | Windows + VS Code**

**Project:** Farm2Market DevOps Deployment  
**Application:** Python FastAPI Inventory API  
**Containerization:** Docker  
**Version Control:** Git and GitHub  
**Continuous Integration:** GitHub Actions  
**Cloud Hosting:** Render  
**Testing:** pytest  
**Status:** Core learning project completed; optional improvements remain.

---

# 1. Project Overview

## 1.1 What is this project?

Farm2Market DevOps is a beginner-friendly project that takes a small Python web application through the main stages of a software delivery workflow.

We created an inventory API, tested its functionality, packaged it into a Docker container, automated testing using GitHub Actions, and deployed it to a cloud hosting platform.

The purpose is to learn how applications are built, tested, deployed, monitored, and troubleshot—not just how to write application code.

## 1.2 Why did we choose Farm2Market?

Farm2Market is a suitable project because it represents a practical application domain: connecting agricultural products with a marketplace.

An inventory application naturally involves products, quantities, availability, and potentially orders. These are easy concepts to understand while learning DevOps.

We deliberately created a small API rather than rebuilding the entire Farm2Market application. This let us focus on deployment and operations without introducing unnecessary complexity.

**Important distinction:** The current DevOps demo uses sample product data. It is not yet a complete marketplace, and it does not have a persistent inventory database or a full order-management system.

## 1.3 Business problem and technical objective

**Business context:** An inventory application needs to remain accessible and return reliable product information.

**Technical objective:** Demonstrate a repeatable workflow for packaging, testing, deploying, and troubleshooting a web service.

The project addresses these learning objectives:

- Verify that an application responds correctly.
- Detect errors through automated tests.
- Package software consistently using containers.
- Automate testing after code changes.
- Deploy a service to a cloud environment.
- Diagnose failures using logs, status checks, and health endpoints.

---

# 2. Project Architecture

The workflow we built is:

Developer → Git → GitHub → GitHub Actions → Render → Public API

Docker packages the application and its dependencies. GitHub Actions tests the code, while Render runs the deployed service.

## Components and responsibilities

| Component | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | Defines HTTP endpoints |
| Uvicorn | Runs the web application |
| pytest | Executes automated tests |
| Git | Tracks code changes |
| GitHub | Hosts the source code |
| GitHub Actions | Runs CI tests automatically |
| Docker | Packages the application into an image and container |
| Render | Hosts the public web service |
| Logs and health endpoint | Help verify service status and diagnose problems |

## What happens when a request arrives?

1. A user opens the public API URL.
2. The request reaches the deployed service on Render.
3. Render routes the request to the running application container.
4. Uvicorn receives the HTTP request.
5. FastAPI executes the matching endpoint.
6. The application returns a JSON response.
7. The request and application output may be reflected in available logs.

---

# 3. What Is DevOps?

DevOps is a set of practices that brings software development and IT operations closer together.

Developers build features, while operations practices help ensure those features can be tested, deployed, observed, and maintained reliably.

Our project demonstrates several DevOps concepts.

### Continuous Integration (CI)

CI means automatically checking code changes by running builds and tests.

In our project, GitHub Actions installs Python dependencies and runs pytest when changes are pushed to `main` or a pull request targets `main`.

### Continuous Delivery and Continuous Deployment (CD)

Continuous delivery automates the process of preparing and validating software for release. Continuous deployment goes further by automatically releasing qualifying changes to the target environment.

Our initial project has automated CI and a separate cloud deployment workflow. We have not yet configured a complete CI-to-CD pipeline with deployment gated on test success.

### Containerization

Containerization packages an application and its runtime dependencies into a portable image. A container is a running instance of that image.

### Application monitoring

Monitoring means observing an application's health and behaviour over time. Our project uses a health endpoint and deployment/runtime logs as basic diagnostic tools. It does not yet include a dedicated monitoring and alerting platform.

---

# 4. Understanding the Application

The application is defined in `main.py`.

It exposes three endpoints.

| Endpoint | Purpose | Expected response |
|---|---|---|
| `/` | Basic application response | Running message |
| `/health` | Simple health check | `{"status":"healthy"}` |
| `/products` | Sample inventory | Two sample products |

The application also provides `/docs`, which FastAPI generates automatically for interactive API testing.

## Why use FastAPI?

FastAPI is a Python framework for creating HTTP APIs. It is lightweight and provides automatic API documentation, making it useful for this learning project.

## What is Uvicorn?

Uvicorn is an ASGI server that runs the FastAPI application and listens for HTTP requests.

## What is a health endpoint?

A health endpoint provides a simple way to check whether a service responds as expected.

Our `/health` endpoint currently checks that the application can return a response. It does not verify database connectivity or every dependency, because the current demo has no database.

---

# 5. Automated Testing with pytest

We created `test_main.py` to check the application's expected behaviour.

The three tests verify:

1. The homepage returns HTTP 200 and the expected message.
2. The health endpoint returns HTTP 200 and the expected status.
3. The products endpoint returns HTTP 200 and the expected sample data.

## Commands used

Install testing dependencies:

```powershell
python -m pip install pytest httpx
```

Run the tests:

```powershell
python -m pytest -v
```

Expected successful output includes:

```text
test_main.py::test_home PASSED
test_main.py::test_health PASSED
test_main.py::test_products PASSED

3 passed
```

The actual duration may vary.

## Troubleshooting exercise

We temporarily changed the health endpoint to return:

```python
return {"status": "unhealthy"}
```

The health test failed because the test expected `"healthy"`.

The other two tests passed because their endpoints were unaffected.

We restored the correct response and reran the tests.

**What this taught us:** A test failure can identify a specific problem without implying that the entire application is broken. Re-running the tests after fixing the problem is a form of regression testing.

## About the dependency warning

During local testing, we observed a deprecation warning related to Starlette's test client and httpx.

A warning is not necessarily a failed test. The tests passed when their assertions were satisfied, but the dependency warning should be reviewed when maintaining the project. Do not blindly change dependencies without checking compatibility.

---

# 6. Git and GitHub

Git is a version-control system. It records changes to files and lets developers create commits.

GitHub hosts Git repositories online and provides collaboration features.

## Important commands

Initialize a repository:

```powershell
git init
```

Check changes:

```powershell
git status
```

Stage files:

```powershell
git add .
```

Commit changes:

```powershell
git commit -m "Describe the change"
```

Push to GitHub:

```powershell
git push
```

View commit history:

```powershell
git log --oneline
```

## Why did we create `.gitignore`?

The `.gitignore` file prevents unnecessary or private files from being tracked.

Our entries include:

```text
.venv/
__pycache__/
.pytest_cache/
*.pyc
.env
```

The virtual environment contains locally installed dependencies. The test cache and Python bytecode do not need to be committed.

The `.env` entry helps prevent accidental commits of environment configuration, but it does not remove a secret that was already committed. Secrets should never be committed to the repository.

---

# 7. Docker: Images and Containers

## What is Docker?

Docker is a platform for packaging and running applications in containers.

An image is the packaged template. A container is a running instance of that image.

We created a Docker image named `farm2market-api` with tag `1.0`.

## Dockerfile used in the project

The Dockerfile contains the instructions for building the image.

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

The final command supports Render's assigned `PORT` environment variable while defaulting to port 8000 for local use.

## Understanding the instructions

- `FROM`: Selects a Python base image.
- `WORKDIR`: Sets the working directory inside the image.
- `COPY`: Copies project files into the image.
- `RUN`: Executes commands during image creation.
- `EXPOSE`: Documents the application's container port.
- `CMD`: Defines the default command used to start the application.

## Docker commands used

Check Docker installation:

```powershell
docker --version
```

Test Docker:

```powershell
docker run hello-world
```

Build the application image:

```powershell
docker build -t farm2market-api:1.0 .
```

List images:

```powershell
docker images
```

Run the container:

```powershell
docker run -d --name farm2market-container -p 8000:8000 farm2market-api:1.0
```

List running containers:

```powershell
docker ps
```

List all containers, including stopped ones:

```powershell
docker ps -a
```

View application logs:

```powershell
docker logs farm2market-container
```

Stop the container:

```powershell
docker stop farm2market-container
```

Start the existing container:

```powershell
docker start farm2market-container
```

Restart the container:

```powershell
docker restart farm2market-container
```

## Understanding port mapping

The option `-p 8000:8000` maps port 8000 on the host machine to port 8000 inside the container.

This lets us access the application at:

`http://localhost:8000`

The container listens on `0.0.0.0` internally so Docker can route incoming connections to the application.

## Docker troubleshooting exercise

We stopped the container and attempted to open the health endpoint.

The request failed because the service was no longer running.

We used `docker ps -a` to inspect the container's status and `docker logs` to examine its output, then restarted the container.

This exercise demonstrated how container status and application logs help diagnose an unavailable service.

---

# 8. GitHub Actions: Continuous Integration

GitHub Actions runs automated workflows in response to events in a repository.

Our workflow is stored at:

`.github/workflows/tests.yml`

## Workflow configuration

```yaml
name: Farm2Market CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run automated tests
        run: python -m pytest -v
```

## How the workflow operates

1. A developer pushes code or opens a pull request targeting `main`.
2. GitHub starts a workflow run.
3. The runner checks out the repository.
4. Python 3.11 is configured.
5. Dependencies are installed.
6. pytest runs the automated tests.
7. GitHub reports whether the job succeeded or failed.

## How we verified it

We opened the repository's Actions tab and inspected the workflow run.

The test job displayed a green check mark, indicating that the job succeeded. The screenshot also displayed runtime deprecation and runner notices; those were warnings/notices rather than test failures.

## How to troubleshoot CI failures

1. Open the failed workflow run.
2. Select the failed job.
3. Open the failed step.
4. Read the error message and identify the failing command.
5. Reproduce the issue locally if possible.
6. Fix the problem and push a new commit.
7. Confirm that the new workflow run passes.

The workflow automates testing. It does not automatically guarantee that the application is secure, reliable, or ready for production.

---

# 9. Cloud Deployment with Render

Render hosts the application so that it can be accessed over the internet.

We selected Docker as the runtime and connected the GitHub repository to a Render web service.

## Why use a cloud hosting platform?

Cloud hosting allows an application to be deployed without managing a physical server or configuring a complete virtual machine manually.

It also provides deployment logs, service status, environment configuration, and a public URL.

## Deployment configuration

The relevant settings included:

- Repository: `farm2market-devops`
- Branch: `main`
- Runtime: Docker
- Dockerfile path: `./Dockerfile`
- Health-check path: `/health`

The service successfully deployed and displayed a live status in the Render dashboard.

## Public service URLs

Base URL:

https://farm2market-devops-1.onrender.com

Homepage:

https://farm2market-devops-1.onrender.com/

Health check:

https://farm2market-devops-1.onrender.com/health

Products:

https://farm2market-devops-1.onrender.com/products

Interactive API documentation:

https://farm2market-devops-1.onrender.com/docs

The health endpoint was verified to return:

```json
{
  "status": "healthy"
}
```

The products endpoint returns the two sample products configured in the application.

## Why did we modify the Dockerfile for Render?

The local container uses port 8000 by default. A cloud host may assign a port through the `PORT` environment variable.

The Dockerfile's startup command uses:

```dockerfile
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

This lets the application use the assigned port or fall back to 8000.

## Understanding free-tier limitations

The free hosting instance may spin down after inactivity. As a result, the first request after a period of inactivity can be delayed.

This does not necessarily indicate an application bug. When diagnosing a slow response, check the service status and logs before assuming the application has failed.

Hosting plans and limits can change, so check the provider's current terms when maintaining the project.

---

# 10. Application Monitoring and Troubleshooting

Monitoring and troubleshooting are related but different.

**Monitoring** is the ongoing observation of application health and behaviour.

**Troubleshooting** is the process of diagnosing and resolving a problem.

Our project gives us basic experience with:

- HTTP health checks.
- Automated tests.
- Docker container status.
- Docker logs.
- Cloud deployment status.
- Cloud runtime logs.
- Diagnosing a failed test and a stopped container.

## Troubleshooting scenarios

### Scenario A: The local API does not respond

Possible checks:

```powershell
docker ps -a
docker logs farm2market-container
```

Confirm that the container is running and that the expected port is mapped.

### Scenario B: A pytest test fails

Run:

```powershell
python -m pytest -v
```

Read the assertion failure and compare the expected result with the actual response.

### Scenario C: The cloud deployment fails

Check Render's deployment logs for Docker build failures, dependency installation errors, missing files, or application startup errors.

### Scenario D: The application is live but a request fails

Open the health endpoint and inspect runtime logs. Check the requested route, application response, port configuration, and any relevant exception messages.

### Scenario E: The cloud service responds slowly

Consider whether the free service has spun down. Check deployment status and runtime logs before making code changes.

## A systematic troubleshooting method

Use this sequence in interviews and real projects:

1. Reproduce the problem.
2. Determine its scope.
3. Inspect status, logs, and error messages.
4. Identify the likely root cause.
5. Apply the smallest appropriate fix.
6. Retest the affected functionality.
7. Check for regressions.
8. Document the cause and resolution.

---

# 11. Windows and Linux Commands

We developed the project on Windows using PowerShell.

Linux commands are also important in DevOps, especially when working with cloud servers and containers.

| Task | PowerShell | Linux |
|---|---|---|
| Current directory | `Get-Location` | `pwd` |
| List files | `Get-ChildItem` | `ls` |
| Search text in logs | `Select-String` | `grep` |
| Inspect processes | `Get-Process` | `ps` |
| Check Python version | `python --version` | `python3 --version` |

Docker Desktop ran Linux containers through its Linux backend. That does not mean we completed a full Linux server administration project. Learning SSH, permissions, system services, and resource inspection on Linux would be a useful next step.

---

# 12. Project Structure

The core project files are:

```text
farm2market-devops/
├── main.py
├── test_main.py
├── requirements.txt
├── Dockerfile
├── .gitignore
└── .github/
    └── workflows/
        └── tests.yml
```

The `.venv/` folder also exists locally, but it is excluded from version control.

## Purpose of each file

| File | Purpose |
|---|---|
| `main.py` | Defines the FastAPI application and endpoints |
| `test_main.py` | Contains automated API tests |
| `requirements.txt` | Lists Python dependencies |
| `Dockerfile` | Defines how to build the container image |
| `.gitignore` | Excludes local files and caches from Git |
| `tests.yml` | Defines the GitHub Actions CI workflow |

---

# 13. What Is Complete and What Is Not?

## Completed core objectives

- Built a working Python API.
- Created automated tests.
- Diagnosed and fixed an intentional test failure.
- Built and ran a Docker container.
- Inspected container status and logs.
- Configured Git and GitHub.
- Configured GitHub Actions CI.
- Verified a successful CI run.
- Deployed the application to Render.
- Verified the public health endpoint.
- Practised basic application and deployment troubleshooting.

## Improvements for a stronger portfolio project

### Priority 1: Reproducible dependencies

Pin dependency versions to versions that have been tested together. Consider generating a lock file and reviewing the earlier test-client deprecation warning.

### Priority 2: Real inventory persistence

Replace hard-coded product data with a database such as SQLite for local development and a suitable persistent database for hosted use.

### Priority 3: Stronger monitoring

Add structured logs, request/error metrics, and alerts for downtime. A health endpoint alone is not a complete monitoring system.

### Priority 4: Deployment automation

Configure a deployment pipeline that deploys only after the relevant tests pass. Verify the provider's deployment integration and safeguards before enabling automatic deployment.

### Priority 5: Container improvements

Add a Docker health check where appropriate, review image size, pin the base image to a suitable version, and scan dependencies and images for known vulnerabilities.

### Priority 6: Security

Validate input, handle exceptions properly, avoid exposing secrets, and configure authentication before exposing inventory-changing operations.

### Priority 7: Linux

Practise Linux commands, permissions, process management, SSH, environment variables, and service logs.

These are extensions. They do not invalidate the completed beginner project.

---

# 14. How to Describe This Project on Your Resume

**Farm2Market DevOps Deployment**

- Built and containerized a Python FastAPI inventory API using Docker.
- Implemented automated testing with pytest and configured a GitHub Actions CI workflow to validate code changes.
- Deployed the containerized service to Render and verified availability using HTTP health checks.
- Practised troubleshooting through application logs, container status checks, and automated test failures.

List the project under Projects, and include the GitHub repository and live service URLs if they are publicly accessible.

Avoid describing the project as a production-scale system or claiming that you implemented dedicated monitoring tools, a full Linux server, or automated cloud deployment unless you complete those extensions.

---

# 15. Interview Questions and Answers

### Q1. What did you build?

I built a beginner DevOps project around a Python FastAPI inventory API. I containerized the application with Docker, automated testing using GitHub Actions, and deployed it to Render.

### Q2. Why did you use Docker?

Docker packages the application and its dependencies into a consistent environment. This reduces differences between development and deployment environments.

### Q3. What is the difference between an image and a container?

An image is the packaged template used to run the application. A container is a running instance of that image.

### Q4. What does your CI pipeline do?

It checks out the code, configures Python, installs dependencies, and runs pytest when a push or relevant pull request triggers the workflow.

### Q5. How did you troubleshoot an issue?

I deliberately changed the health endpoint response so the corresponding test failed. I inspected the assertion error, identified the mismatch, restored the correct response, and reran the tests.

### Q6. How did you verify the cloud deployment?

I checked the Render deployment status, inspected the logs, and tested the public `/health` and `/products` endpoints.

### Q7. Did you use monitoring tools such as Grafana or Splunk?

Not in this project. I used basic health checks, automated tests, Docker logs, and Render deployment/runtime logs. Adding a dedicated monitoring platform is a possible extension.

### Q8. Did you implement CD?

I implemented CI with GitHub Actions and deployed the application separately through Render. A fully automated, test-gated CD pipeline remains a future improvement.

### Q9. Why did you choose Farm2Market?

It provided a familiar inventory-related use case for practising the software delivery lifecycle without making the application itself too complex.

### Q10. What would you improve next?

I would add a persistent database, stronger logging and monitoring, pinned dependencies, security improvements, and a deployment pipeline that runs only after the required tests pass.

---

# 16. Final Summary

The project demonstrates a basic software delivery lifecycle:

**Develop → Test → Package → Automate CI → Deploy → Verify → Troubleshoot**

The key learning outcome is understanding how these components work together, not merely memorizing commands.

You can use this handbook to recreate the project, explain each technology in an interview, troubleshoot common failures, and plan the next iteration.

**Project status:** Core beginner DevOps project completed. Advanced monitoring, production hardening, persistent storage, and fully automated CD remain optional extensions.
