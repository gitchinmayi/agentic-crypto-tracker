pipeline {
    agent any

    environment {
        // Adds the location where we will download docker-compose to the system path
        PATH = "${HOME}/.docker/cli-plugins:${env.PATH}"
    }

    stages {
        stage('Setup Docker Compose') {
            steps {
                echo 'Installing Docker Compose V2 locally for this session...'
                sh '''
                    mkdir -p ~/.docker/cli-plugins/
                    curl -SL https://github.com/docker/compose/releases/download/v2.26.1/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
                    chmod +x ~/.docker/cli-plugins/docker-compose
                '''
                sh 'docker compose version'
            }
        }

        stage('Build Docker Images') {
            steps {
                echo 'Checking workspace files...'
                sh 'ls -la' // This is the most important debug line
                echo 'Building images...'
                sh 'docker compose -f docker-compose.yml build'
            }
        }
        stage('Run Containers') {
            steps {
                echo 'Starting application...'
                // Use --force-recreate to ensure fresh containers
                sh 'docker compose up -d --force-recreate'
                sh 'docker compose ps'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution finished.'
        }
    }
}
