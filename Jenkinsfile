pipeline {
    agent any
    
    environment {
        DOCKER_HUB_CREDS = credentials('docker-jenkins')
        IMAGE_NAME = 'saadgillani7/ml-app'
        IMAGE_TAG = "v1.0.${BUILD_NUMBER}"
        ADMIN_EMAIL = 'saadgillani001@gmail.com'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
                sh 'docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest'
            }
        }
        
        stage('Run Tests in Container') {
            steps {
                sh 'docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python -m pytest tests/'
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                sh 'echo $DOCKER_HUB_CREDS_PSW | docker login -u $DOCKER_HUB_CREDS_USR --password-stdin'
                sh 'docker push ${IMAGE_NAME}:${IMAGE_TAG}'
                sh 'docker push ${IMAGE_NAME}:latest'
            }
        }
        
        stage('Cleanup') {
            steps {
                sh 'docker logout'
            }
        }
    }
    
    post {
        success {
            script {
                emailext(
                    subject: "Pipeline Success: ${currentBuild.fullDisplayName}",
                    body: "The pipeline has been successfully deployed.\nImage: ${env.IMAGE_NAME}:${env.IMAGE_TAG}",
                    to: "${env.ADMIN_EMAIL}",
                    from: "jenkins@example.com"
                )
            }
        }
        failure {
            script {
                emailext(
                    subject: "Pipeline Failed: ${currentBuild.fullDisplayName}",
                    body: "The pipeline has failed. Please check the logs.",
                    to: "${env.ADMIN_EMAIL}",
                    from: "jenkins@example.com"
                )
            }
        }
    }
}