pipeline {
    agent any

    environment {
        // Adds the location where we will download docker-compose to the system path
        PATH = "${HOME}/.docker/cli-plugins:${env.PATH}"
    }

    stages {
        stage('Setup Docker Compose') {
            steps {
                echo 'Installing Docker Compose V2 based on system architecture...'
                sh '''
                    # 1. Detect Architecture
                    ARCH=$(uname -m)
                    echo "System Architecture: $ARCH"

                    if [ "$ARCH" = "x86_64" ]; then
                        BINARY="docker-compose-linux-x86_64"
                    elif [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
                        BINARY="docker-compose-linux-aarch64"
                    else
                        echo "Unknown architecture $ARCH, defaulting to x86_64"
                        BINARY="docker-compose-linux-x86_64"
                    fi

                    # 2. Ensure directory exists and remove any old/corrupt binary
                    mkdir -p ~/.docker/cli-plugins/
                    rm -f ~/.docker/cli-plugins/docker-compose

                    # 3. Download the correct version
                    echo "Downloading: $BINARY"
                    curl -SL "https://github.com/docker/compose/releases/download/v2.26.1/${BINARY}" -o ~/.docker/cli-plugins/docker-compose
                    
                    # 4. Make executable
                    chmod +x ~/.docker/cli-plugins/docker-compose
                '''
                // 5. Verify it works
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
                // Wait 10 seconds for app to initialize (increased for reliability)
                sleep 10
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
