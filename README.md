# ML-CICD-pipeline
Basic ML CI/CD Pipeline implementation

## jenkins
docker run -d -p 8070:8080 -p 50000:50000 jenkins/jenkins:lts

### airflow
docker compose up -d

### dvc 
make gdrive service account
connect gdrive public folder with it
git init
dvc remote list
dvc remote remove myremote
dvc remote list
dvc remote add -d gdrive_remote gdrive://1qIvgWtt3ZJ0cLFO9TTa5Iq0QCP0wQzjV
dvc remote modify gdrive_remote gdrive_use_service_account true
dvc remote modify gdrive_remote gdrive_service_account_json_file_path src/dvc.json
dvc push
dvc repro
dvc push
dvc dag
dvc pull

### MLFLOW

mlflow ui
python mlflow_.py