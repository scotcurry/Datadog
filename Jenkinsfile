pipeline {
    agent any

    environment {
        DATADOG_API_KEY = credentials('DD_API_KEY')
        DATADOG_APP_KEY = credentials('DD_APP_KEY')
        DD_API_KEY = credentials("DD_API_KEY")
        DD_APPLICATION_KEY = credentials("DD_APP_KEY")
        DOCKERHUB_CREDENTIALS = credentials('docker-hub')
        GITHUB_URL = "github.com/scotcurry/Datadog"
    }
    stages {
        stage ('Github Checkout') {
            steps {
                checkout scmGit(
                  branches: [[name: "master"]],
                  userRemoteConfigs: [[url: 'https://github.com/scotcurry/Datadog.git']]
                )
            }
        }
        stage ('Get Current Version') {
            steps {
                script {
                    def current_version_local = sh(returnStdout: true, script: '/usr/local/microsoft/powershell/7/pwsh ./BuildCurrentVersion.ps1')
                    current_version_local = current_version_local.trim()
                    env.current_version = current_version_local
                    echo "Current Version: ${current_version}"
                }
            }
        }
        stage ('Get SHA Value') {
            steps {
                script {
                    git_sha = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
                    echo "Git SHA: ${git_sha}"
                }
            }
        }
        stage ('Install Requirements.txt') {
          steps {
            sh "/usr/bin/python3 -m venv ./venv"
            sh "./venv/bin/pip3 install -r requirements.txt"
          }
        }
        stage ('Run Unit Tests') {
            steps {
                sh "./venv/bin/pytest ./unittests/"
            }
        }
        stage ('Update Docker-Compose YAML') {
            steps {
                sh "mkdir ./tmp"
                sh "sed 's/datadogcurryware:latest/datadogcurryware:${current_version}/g' ./Containers/docker-compose-template.yaml > ./tmp/docker-compose-image-version.yaml"
                sh "sed 's/<DATADOG_VERSION>/${current_version}/g' ./tmp/docker-compose-image-version.yaml > ./tmp/docker-file-version.yaml"
                sh "sed 's/<GIT_SHA>/${git_sha}/g' ./tmp/docker-file-version.yaml > ./tmp/docker-compose-gitsha.yaml"
                sh "sed 's/<DD_API_KEY>/${DATADOG_API_KEY}/g' ./tmp/docker-compose-gitsha.yaml > ./tmp/docker-compose.yaml"
                sh "cp ./tmp/docker-compose.yaml /Users/scot.curry/Desktop/docker-compose.yaml"
            }
        }
        stage ('Build Docker Container') {
            steps {
                sh '/usr/local/bin/docker build --tag docker.io/scotcurry4/datadogcurryware:${current_version} --build-arg DD_GIT_REPOSITORY_URL="${GITHUB_URL}" --build-arg DD_GIT_COMMIT_SHA="$(git rev-parse HEAD)" --file ./Containers/Dockerfile .'
            }
        }
        stage ('Docker Hub Login') {
          steps {
            sh 'echo $DOCKERHUB_CREDENTIALS_PSW | /usr/local/bin/docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
          }
        }
        stage ('Push Docker Container') {
            steps {
                sh "/usr/local/bin/docker push scotcurry4/datadogcurryware:${current_version}"
            }
        }
        stage ('Build / Update Datadog Service Catalog') {
            steps {
                sh '/opt/homebrew/bin/terraform init'
                sh '/opt/homebrew/bin/terraform plan -var datadog_app_key=${DATADOG_APP_KEY} -var datadog_api_key=${DATADOG_API_KEY}'
                sh '/opt/homebrew/bin/terraform apply -var datadog_app_key=${DATADOG_APP_KEY} -var datadog_api_key=${DATADOG_API_KEY} -auto-approve'
            }
        }
    }
    post {
        always {
          sh "rm -rf ./tmp"
          sh "rm -rf ./venv"
        }
    }
}