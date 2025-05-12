# ML-CICD-pipeline
Basic ML CI/CD Pipeline implementation

## jenkins
docker run -d -p 8070:8080 -p 50000:50000 jenkins/jenkins:lts

### airflow
docker compose up -d

### dvc 

  145  git init
  146  dvc remote list
  148  dvc remote remove myremote
  149  dvc remote list
  150  dvc remote add -d gdrive_remote gdrive://Joq6kLb1Y8FmvCgGwcjJu8Hu8ZqQ5
  151  dvc remote modify gdrive_remote gdrive_use_service_account true
  156  dvc remote modify gdrive_remote gdrive_service_account_json_file_path src/dvc.json
  157  dvc push
  158  ls
  159  cd data
  160  dvc add .
  161  dvc add processed_data.csv
  162  dvc status
  163  dvc add processed_data.csv
  164  dvc add raw_data.csv
  165  dvc push
  166  dvc status
  167  dvc pull
  180  dvc repro
  181  dvc push
  182  dvc dag
