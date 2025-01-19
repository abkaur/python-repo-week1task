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
                        docker build -t abkaur95/week2task:1.0.1 -f Dockerfile .
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
                            docker push abkaur95/week2task:1.0.1
                        '''
                    }
                }
            }
        }
        stage('Update Deployment in K8s') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'githubcredentials', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                        sh '''
                            # Set up git configuration
                            git config --global user.email "kaurab@sheridancollege.ca"
                            git config --global user.name "abkaur"

                            # Clone the manifest repository with credentials
                            rm -rf week2task
                            git clone https://$GIT_USERNAME:$GIT_PASSWORD@github.com/abkaur/week2task.git

                            # Navigate to the k8s directory
                            cd week2task/k8s

                            # Update the image in deployment.yaml
                            sed -i 's|image:.*|image: abkaur95/week2task:1.0.1|' deployment.yaml

                            # Commit and push the changes
                            git add deployment.yaml
                            git commit -m "Update image to abkaur95/week2task:1.0.1"
                            git push https://$GIT_USERNAME:$GIT_PASSWORD@github.com/abkaur/week2task.git
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
            echo 'Pipeline completed successfully! Image pushed to Docker Hub and deployment.yaml updated.'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
