pipeline {
    agent any

    environment {
        IMAGE_NAME = 'python-app'   // Name for the Docker image
        ECR_REPO_URL = '597088037401.dkr.ecr.us-east-1.amazonaws.com'  // Replace with your ECR repository URL
	ECR_REPO_NAME = 'yarin-project'
        AWS_REGION = 'us-east-1'  // Replace with your AWS region
    }

    stages {
        //stage('Checkout') {
         //   steps {
          //      // Checkout the source code from the SCM (e.g., GitHub)
           //     checkout scm
           // }
      //  }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    sh 'docker build -t $IMAGE_NAME .'
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    // Log in to AWS ECR
                    sh """
                    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO_URL
                    """
                }
            }
        }

        stage('Tag Docker Image') {
            steps {
                script {
                    // Tag the Docker image with the ECR repository URL
                    sh "docker tag $IMAGE_NAME:latest $ECR_REPO_URL/$ECR_REPO_NAME:latest"
                }
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                script {
                    // Push the Docker image to ECR
                    sh "docker push $ECR_REPO_URL/$ECR_REPO_NAME:latest"
                }
            }
        }
    }

    post {
       
    }
}
