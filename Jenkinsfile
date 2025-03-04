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
                sudo docker build -t saadgillani7/ml-app:v1.0.${BUILD_NUMBER} .
                sudo docker tag saadgillani7/ml-app:v1.0.${BUILD_NUMBER} saadgillani7/ml-app:latest
                '''
            }
        }
        
        stage('Run Tests in Container') {
            steps {
                sh 'sudo docker run --rm saadgillani7/ml-app:v1.0.${BUILD_NUMBER} python -m pytest tests/'
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-jenkins', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                    echo $PASSWORD | sudo docker login -u $USERNAME --password-stdin
                    sudo docker push saadgillani7/ml-app:v1.0.${BUILD_NUMBER}
                    sudo docker push saadgillani7/ml-app:latest
                    sudo docker logout
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