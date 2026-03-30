# ACEest Fitness & Gym - DevOps Pipeline Assignment

## Project Overview
This project demonstrates a complete end-to-end DevOps CI/CD workflow for **ACEest Fitness & Gym**. The project leverages a robust tech stack to ensure code integrity, consistent environments, automated testing, and rapid delivery. This repository encompasses application development, containerization, and continuous integration pipelines using both GitHub Actions and Jenkins, specifically designed for a remote VM-based environment (CodeArgo RDP).

## Features
- **Flask REST API**: Provides a health check endpoint and fitness program details.
- **Automated Testing**: Comprehensive assertions using `pytest`.
- **Docker Containerization**: Portable, lightweight Python-based container image.
- **GitHub Actions Pipeline**: Automated CI on push and pull requests.
- **Jenkins CI/CD Pipeline**: Full end-to-end pipeline running inside the VM.
- **SonarQube Quality Gate**: Static code analysis integration.

## Tech Stack
- **Application**: Python 3.9, Flask
- **Testing**: Pytest, Pytest-cov
- **Containerization**: Docker
- **Continuous Integration**: Jenkins, GitHub Actions
- **Static Code Analysis**: SonarQube
- **Version Control**: Git, GitHub

## Project Structure
```text
ACEest_Fitness_DevOps/
├── .github/
│   └── workflows/
│       └── main.yml
├── tests/
│   └── test_app.py
├── app.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
├── sonar-project.properties
└── README.md
```

## Setup Instructions (VM-Based Environment)

**IMPORTANT CONTEXT**: This project is designed exclusively for the remote VM (CodeArgo RDP) environment provided for the course. All executions stay within the VM. **Do NOT run this locally.** All references to "localhost" pertain to the VM environment.

### 1. Initial Authentication & Git Setup
Log in to the VM via your browser.
**Username**: `cloud` 
**Password**: `cloud`

Open a terminal inside the VM and configure your Git credentials:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 2. Version Control Initialization
Create your project repository locally inside the VM:
```bash
mkdir -p ~/ACEest_Fitness_DevOps
cd ~/ACEest_Fitness_DevOps

git init

git add .
git commit -m "Initial commit: App setup, Docker, and CI pipelines"
```
Create a GitHub repository and link it:
```bash
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY.git
git branch -M main
git push -u origin main
```

## Application Usage & Testing

### How to Run the Application (Locally in VM without Docker)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
**Sample API Outputs**:
- `curl http://localhost:5000/`
  *Response*: `{"status": "healthy", "message": "ACEest Fitness & Gym API is up and running!"}`
- `curl http://localhost:5000/programs`
  *Response*: `{"BG": {"calorie_factor": 26, "name": "Beginner"}, "FL": {"calorie_factor": 22, "name": "Fat Loss"}, "MG": {"calorie_factor": 35, "name": "Muscle Gain"}}`

### How to Run Tests
```bash
pytest tests/
```

### Docker Usage
If you prefer running via Docker in the VM:
```bash
docker build -t aceest-fitness:latest .

docker run -d -p 5000:5000 --name aceest-container aceest-fitness:latest

docker run --rm aceest-fitness:latest pytest tests/
```

## CI/CD Architecture

### Jenkins Pipeline Explanation
Jenkins runs locally inside the VM at `http://localhost:8080`.
The `Jenkinsfile` defines the following stages:
1. **Checkout**: Pulls the latest code.
2. **Build Environment**: Creates a Python virtual environment and installs dependencies.
3. **Run Tests**: Executes `pytest` and generates coverage metrics.
4. **SonarQube Analysis**: Uses SonarScanner to analyze code quality and pushes reports to `http://localhost:9000`.
5. **Build Docker Image**: Containerizes the tested Flask application.
6. **Run Container**: Runs the application on port 5000.
7. **API Smoke Tests**: Executes `curl` against the deployed endpoints.
8. **Cleanup**: Stops and removes the Docker container and cleans the workspace.

#### SonarQube Integration
- SonarQube runs inside the VM at `http://localhost:9000`.
- Generate a token in SonarQube (`Administration` -> `Security` -> `Users` -> `Tokens`).
- Add this token to Jenkins Credentials as a 'Secret text' with the ID `sonarqube-token`.
- Configure the SonarQube Server in Jenkins Global Configuration as `sonar-vm` with URL `http://localhost:9000`.
- Configure SonarScanner in Jenkins Global Tool Configuration as `SonarQubeScanner`.

### GitHub Actions Workflow Explanation
The `.github/workflows/main.yml` acts as the first layer of defense:
1. **Trigger**: Runs on any `push` or `pull_request` to `main`, `feature/*`, or `bugfix/*`.
2. **Build & Lint Stage**: Checks Python code for standard PEP-8 validation and syntax errors using `flake8`.
3. **Docker Build & Test Stage**: Builds the Docker container, and explicitly runs the Pytest suite *inside* the newly built container to guarantee artifacts are intact.

## Screenshots Documentation [PLACEHOLDER]
1. GitHub Actions Passing state.
2. Jenkins Pipeline Success Graph.
3. SonarQube Project Dashboard.
4. Output of endpoints using curl or browser.
