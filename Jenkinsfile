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
                        docker build -t abkaur95/week2task:1.0.0 -f Dockerfile .
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
                            docker push abkaur95/week2task:1.0.0
                        '''
                    }
                }
            }
        }
        stage('Update Deployment in K8s') {
            steps {
                script {
                    sh '''
                        git config --global user.email "kaurab@sheridancollege.ca"
                        git config --global user.name "abkaur"
                    '''

                    // Clone the repository and navigate to the directory
                    sh '''
                        rm -rf week2task
                        git clone https://github.com/abkaur/week2task.git
                        cd week2task/K8s
                    '''
                    
                    // Check if the image in deployment.yaml matches the new image
                    def imageUpdated = sh(script: '''
                        cd week2task/K8s
                        if grep -q "image: $DOCKER_IMAGE" deployment.yaml; then
                            echo "Image is already up-to-date."
                            exit 1
                        else
                            echo "Updating image..."
                            sed -i 's|image:.*|image: $DOCKER_IMAGE|g' deployment.yaml
                            git add deployment.yaml
                            git commit -m "Update image to $DOCKER_IMAGE"
                            git push
                            exit 0
                        fi
                    ''', returnStatus: true)
                    
                    if (imageUpdated != 0) {
                        echo "No update needed. Exiting..."
                        currentBuild.result = 'SUCCESS'
                        return
                    }

                    echo "Image updated successfully and pushed to the repository."
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
