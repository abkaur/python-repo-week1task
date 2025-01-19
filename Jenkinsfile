pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/abkaur/python-repo-week1task.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                pip3 install --user -r python_web_application/requirements.txt
                '''
            }
        }
        stage('Run Tests') {
            steps {
                sh '''
                export PATH=$PATH:/var/lib/jenkins/.local/bin
                pytest python_web_application/tests/
                '''
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image with a tag
                    sh '''
                    docker build -t abkaur95/week2task:latest -f Dockerfile .
                    '''
                }
            }
        }
        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                        docker push abkaur95/week2task:latest
                        '''
                    }
                }
            }
        }
    }
    post {
        always {
            cleanWs() // Clean up the workspace
        }
        success {
            echo 'Pipeline completed successfully! Image pushed to Docker Hub.'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
