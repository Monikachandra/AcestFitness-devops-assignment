# ACEest Fitness & Gym DevOps Project

This repository contains the complete DevOps CI/CD pipeline assignment for ACEest Fitness & Gym. The setup includes a Flask application moving through testing, containerization, and deployment via Jenkins and GitHub Actions.

Everything is configured specifically to run inside the CodeArgo RDP VM.

### Project Components

- **Flask App**: A small API with a health check and fitness program endpoints.
- **Tests**: Pytest suite for verifying the endpoints.
- **Docker**: Container configuration to package the application.
- **GitHub Actions**: Automated linting and testing on code push.
- **Jenkins Pipeline**: The primary CI/CD pipeline covering build, test, SonarQube analysis, Docker packaging, and smoke tests.
- **SonarQube**: Code quality checks configured via `sonar-project.properties`.

### Directory Layout

```text
.
├── .github/workflows/main.yml
├── tests/test_app.py
├── app.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
├── sonar-project.properties
└── README.md
```

### Local Setup (run on localhost)

#### 1) Create and activate a virtual environment

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### 2) Install dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

#### 3) Run the application
```bash
python app.py
```

The app will start on:
- http://localhost:5000
- http://127.0.0.1:5000


Test the endpoints:
- `curl http://localhost:5000/` (Health check)
- `curl http://localhost:5000/programs` (Returns Beginner, Fat Loss, and Muscle Gain programs)

To run the unit tests:

```bash
pytest tests/
```

2. **Running with Docker**

```bash
docker build -t aceest-fitness:latest .
docker run -d -p 5000:5000 --name aceest-app aceest-fitness:latest
docker run --rm aceest-fitness:latest python -m pytest tests/
```

### CI/CD Pipelines

**Jenkins (http://localhost:8080)**

The Jenkins pipeline executes a series of automated continuous integration tasks to validate and deploy the code. The process starts by retrieving the latest source from GitHub. Then, it creates a dedicated Python virtual environment to execute the PyUnit test coverage. Once the tests pass, it triggers a static code analysis using SonarQube based on the configurations defined in `sonar-project.properties`.
 The new container is then deployed and subjected to basic curl smoke tests against the root and programs endpoints. 
Finally, the pipeline tears down the running test container and removes the local virtual environment to ensure a clean workspace for the next run.


**GitHub Actions**

This pipeline adds an extra layer of validation. On every push to GitHub, it runs `flake8` to check for syntax errors, builds the Docker image, and runs `pytest` inside the container. This ensures the code is healthy before it reaches the Jenkins pipeline.
