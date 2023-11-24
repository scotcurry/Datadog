pipeline {
    agent any

    environment {
        DATADOG_API_KEY = credentials('DD_API_KEY')
        DATADOG_APP_KEY = credentials('DD_APP_KEY')
        DD_API_KEY = credentials("DD_API_KEY")
        DD_APPLICATION_KEY = credentials("DD_APP_KEY")
    }
    stages {
        stage ('Github Checkout') {
            steps {
                script {
                    git branch: 'master',
                    url: 'https://github.com/scotcurry/Datadog.git'
                }
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
                sh "sed 's/scotcurry4/datadogcurryware:latest/scotcurry4/datadogcurryware:${current_version}/g' ./Containers/docker-compose-template.yaml > ./tmp/docker-compose-file-version.yaml"
                sh "sed 's/<DATADOG_VERSION>/${current_version}/g' ./tmp/docker-compose-file-version.yaml > ./tmp/docker-compose-version.yaml"
                sh "sed 's/<GIT_SHA>/${git_sha}/g' ./tmp/docker-compose-version.yaml > ./tmp/docker-compose-gitsha.yaml"
                sh "sed 's/<DD_API_KEY>/${DATADOG_API_KEY}/g' ./tmp/docker-compose-gitsha.yaml > ./tmp/docker-compose.yaml"
                sh "cp ./tmp/docker-compose.yaml /Users/scot.curry/Desktop/docker-compose.yaml"
            }
        }
        stage ('Build Docker Container') {
            steps {
                sh "/usr/local/bin/docker build --tag docker.io/scotcurry4/datadogcurryware${current_version} --file ./Containers/Dockerfile ."
            }
        }
        stage ('Push Docker Container') {
            steps {
                sh "/usr/local/bin/docker push scotcurry4/datadogcurryware${current_version}"
            }
        }
    }
}