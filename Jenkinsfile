pipeline {
    agent {
        label 'vm' // Adjust this label based on the specific name of your VM node in Jenkins
    }

    triggers {
        pollSCM('* * * * *') // Triggers the pipeline when a push occurs by polling SCM every minute
    }

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

        stage('SonarQube Scan') {
            steps {
                sh '/opt/sonar-scanner/bin/sonar-scanner'
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    python3 -m venv venv
                    venv/bin/pip install --upgrade pip
                    venv/bin/pip install -r requirements.txt
                    venv/bin/flake8 app.py tests/ || true
                '''
            }
        }

        stage('Test') {
            steps {
                sh "venv/bin/python -m pytest tests/ --cov=app --cov-report=xml"
            }
        }

        stage('Export Docker Image') {
            steps {
                sh "docker save ${DOCKER_IMAGE} -o ${DOCKER_IMAGE}.tar"
            }
        }
    }

    post {
        always {
            sh '''
                echo "Post Actions: Cleaning up workspace..."
                docker rmi ${DOCKER_IMAGE} || true
                rm -rf venv
                rm -f ${DOCKER_IMAGE}.tar
            '''
            cleanWs()
        }
        success {
            echo "CI/CD Pipeline ran perfectly on VM instance!"
        }
        failure {
            echo "CI/CD Pipeline failed. Check the logs above."
        }
    }
}
