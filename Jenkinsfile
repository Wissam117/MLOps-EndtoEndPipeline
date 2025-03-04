pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t saadgillani7/ml-app:v1.0.${BUILD_NUMBER} .
                docker tag saadgillani7/ml-app:v1.0.${BUILD_NUMBER} saadgillani7/ml-app:latest
                '''
            }
        }
        
        stage('Run Tests in Container') {
            steps {
                sh 'docker run --rm saadgillani7/ml-app:v1.0.${BUILD_NUMBER} python -m pytest tests/'
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-jenkins', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                    echo $PASSWORD | docker login -u $USERNAME --password-stdin
                    docker push saadgillani7/ml-app:v1.0.${BUILD_NUMBER}
                    docker push saadgillani7/ml-app:latest
                    docker logout
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo "Build successful! Docker image saadgillani7/ml-app:v1.0.${BUILD_NUMBER} has been pushed."
        }
        failure {
            echo "Build failed! Please check the logs for details."
        }
    }
}
