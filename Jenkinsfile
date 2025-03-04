pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Python Dependencies') {
            steps {
                sh '''
                # Install system dependencies
                sudo apt-get update
                sudo apt-get install -y python3-pip python3-pytest
                
                # Install required packages
                pip3 install flask pytest
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                # Run tests directly
                PYTHONPATH=. python3 -m pytest tests/
                '''
            }
        }
        
        stage('Build Application') {
            steps {
                sh '''
                # Train the model
                python3 src/model/train.py
                
                # Create deployment package
                mkdir -p deployment
                cp -r src/ deployment/
                cp model.pkl deployment/
                cp requirements.txt deployment/
                tar -czf ml-app-v1.0.${BUILD_NUMBER}.tar.gz deployment/
                '''
            }
        }
        
        stage('Deploy Application') {
            steps {
                sh '''
                # Create deployment directory
                DEPLOY_DIR=/var/lib/jenkins/deployed-apps/ml-app-v1.0.${BUILD_NUMBER}
                mkdir -p $DEPLOY_DIR
                
                # Copy deployment package
                cp ml-app-v1.0.${BUILD_NUMBER}.tar.gz $DEPLOY_DIR/
                
                # Extract for verification
                cd $DEPLOY_DIR
                tar -xzf ml-app-v1.0.${BUILD_NUMBER}.tar.gz
                
                echo "Deployed to $DEPLOY_DIR"
                '''
            }
        }
    }
    
    post {
        success {
            echo "Build successful! ML application deployed to /var/lib/jenkins/deployed-apps/ml-app-v1.0.${BUILD_NUMBER}"
            
            emailext (
                subject: "Pipeline Success: ML Application Deployment",
                body: "ML Application has been successfully deployed. Version: v1.0.${BUILD_NUMBER}",
                to: "saadgillani001@gmail.com"
            )
        }
        failure {
            echo "Build failed! Please check the logs for details."
            
            emailext (
                subject: "Pipeline Failed: ML Application Deployment",
                body: "ML Application deployment failed. Please check Jenkins logs for details.",
                to: "saadgillani001@gmail.com"
            )
        }
    }
}