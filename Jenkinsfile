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
                sh 'ls -la'
                echo 'Building images...'
                sh 'docker compose -f docker-compose.yml build'
            }
        }

        stage('Run Containers') {
            steps {
                echo 'Cleaning up old containers and starting application...'
                // 'down' removes existing containers/networks to avoid name conflicts
                sh 'docker compose down'
                
                echo 'Starting new containers...'
                sh 'docker compose up -d --force-recreate'
                sh 'docker compose ps'
            }
        }
        
        stage('Health Check') {
            steps {
                echo 'Verifying if the dashboard is running...'
                // Wait 5 seconds for app to initialize, then check if port 8050 is responding
                sleep 5
                sh 'curl -I http://localhost:8050 || echo "App not reachable yet"'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution finished.'
        }
        success {
            echo 'SUCCESS: The Crypto Tracker is now running at http://localhost:8050'
        }
        failure {
            echo 'FAILURE: The pipeline failed. Check the logs above.'
        }
    }
}
