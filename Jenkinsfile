pipeline {
    agent any

    environment {
        AWS_REGION = 'ap-south-1'
        DOCKER_IMAGE_AUTH = 'smrithi-auth:latest'
        DOCKER_IMAGE_GAME = 'smrithi-game:latest'
        DOCKER_IMAGE_MEM = 'smrithi-memory:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Lint') {
            steps {
                sh 'pip install flake8'
                sh 'flake8 services/ --count --max-line-length=120 --statistics'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'pip install pytest pytest-cov'
                sh 'pytest --cov=services --cov-fail-under=80 tests/'
            }
        }

        stage('SAST Security Scan') {
            steps {
                sh 'pip install bandit'
                sh 'bandit -r services/ -ll'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker build -f services/auth_service/Dockerfile -t ${DOCKER_IMAGE_AUTH} .'
                sh 'docker build -f services/game_service/Dockerfile -t ${DOCKER_IMAGE_GAME} .'
                sh 'docker build -f services/memory_service/Dockerfile -t ${DOCKER_IMAGE_MEM} .'
            }
        }

        stage('CVE Vulnerability Scan') {
            steps {
                sh 'which trivy || true'
                sh 'trivy image --severity HIGH,CRITICAL --exit-code 0 ${DOCKER_IMAGE_AUTH}'
                sh 'trivy image --severity HIGH,CRITICAL --exit-code 0 ${DOCKER_IMAGE_GAME}'
                sh 'trivy image --severity HIGH,CRITICAL --exit-code 0 ${DOCKER_IMAGE_MEM}'
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh 'docker-compose down || true'
                sh 'docker-compose up -d --build'
            }
        }
    }
}
