pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "aceest-${env.BUILD_NUMBER}"
        SONAR_SCANNER_HOME = tool 'SonarQubeScanner' 
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test Config') {
            steps {
                sh '''
                    python3 -m venv venv
                    venv/bin/pip install --upgrade pip
                    venv/bin/pip install -r requirements.txt
                    venv/bin/python -m pytest tests/ --cov=app --cov-report=xml
                '''
            }
        }

        stage('SonarQube Static Analysis') {
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

        stage('Docker Build') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        stage('Run Container & Smoke Test') {
            steps {
                sh '''
                    docker stop aceest-app || true
                    docker rm aceest-app || true
                '''
                sh "docker run -d -p 5000:5000 --name aceest-app ${DOCKER_IMAGE}"
                
                sh '''
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
                echo "Cleaning up..."
                docker stop aceest-app || true
                docker rm aceest-app || true
                rm -rf venv
            '''
            cleanWs()
        }
        success {
            echo "CI/CD Pipeline ran perfectly!"
        }
        failure {
            echo "CI/CD Pipeline failed. Check the logs above."
        }
    }
}
