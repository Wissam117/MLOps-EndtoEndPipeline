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
                # (Optional) Update package lists and install python3-venv if not already installed.
                sudo apt-get update -y
                sudo apt-get install -y python3-venv

                # Create a virtual environment
                python3 -m venv venv

                # Activate the virtual environment
                . venv/bin/activate

                # Upgrade pip, setuptools (to version 68 or later), and wheel.
                pip install --upgrade pip "setuptools>=68" wheel

                # Install required packages from requirements.txt using binary wheels only.
                pip install --only-binary :all: -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                # Activate the virtual environment and run tests
                . venv/bin/activate
                PYTHONPATH=. python3 -m pytest tests/
                '''
            }
        }
        
        stage('Build Application') {
            steps {
                sh '''
                # Activate the virtual environment
                . venv/bin/activate

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
                # Create deployment directory and copy package
                DEPLOY_DIR=/var/lib/jenkins/deployed-apps/ml-app-v1.0.${BUILD_NUMBER}
                mkdir -p $DEPLOY_DIR
                cp ml-app-v1.0.${BUILD_NUMBER}.tar.gz $DEPLOY_DIR/
                
                # Extract package for verification
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
