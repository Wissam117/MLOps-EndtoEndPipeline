pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                sh '''
                python -m venv venv || python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                python -m pytest tests/
                '''
            }
        }
        
        stage('Build Package') {
            steps {
                sh '''
                . venv/bin/activate
                python src/model/train.py
                tar czf ml-app-v1.0.${BUILD_NUMBER}.tar.gz src/ model.pkl requirements.txt
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                sh '''
                mkdir -p /var/lib/jenkins/deployed-apps/ml-app-v1.0.${BUILD_NUMBER}
                cp ml-app-v1.0.${BUILD_NUMBER}.tar.gz /var/lib/jenkins/deployed-apps/ml-app-v1.0.${BUILD_NUMBER}/
                '''
            }
        }
    }
    
    post {
        success {
            echo "Build successful! ML application deployed to /var/lib/jenkins/deployed-apps/ml-app-v1.0.${BUILD_NUMBER}"
        }
        failure {
            echo "Build failed! Please check the logs for details."
        }
    }
}