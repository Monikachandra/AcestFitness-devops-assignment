pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "aceest-fitness:latest"
        SONAR_SCANNER_HOME = tool 'SonarQubeScanner'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m pytest tests/ --cov=app --cov-report=xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('sonar-vm') {
                    sh "${SONAR_SCANNER_HOME}/bin/sonar-scanner \\
                        -Dsonar.projectKey=aceest-fitness \\
                        -Dsonar.sources=app.py \\
                        -Dsonar.python.coverage.reportPaths=coverage.xml \\
                        -Dsonar.host.url=http://localhost:9000 \\
                        -Dsonar.login=${SONAR_TOKEN}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                    docker stop aceest-app || true
                    docker rm aceest-app || true
                '''
                sh "docker run -d -p 5000:5000 --name aceest-app ${DOCKER_IMAGE}"
            }
        }

        stage('API Smoke Tests') {
            steps {
                sh '''
                    echo "Waiting for container to start..."
                    sleep 5
                    curl -f http://localhost:5000/ || exit 1
                    curl -f http://localhost:5000/programs || exit 1
                '''
            }
        }
    }

    post {
        always {
            sh '''
                echo "Cleaning up workspace..."
                docker stop aceest-app || true
                docker rm aceest-app || true
            '''
            cleanWs()
        }
        success {
            echo "CI/CD Pipeline executed successfully!"
        }
        failure {
            echo "CI/CD Pipeline failed. Please check the logs."
        }
    }
}
