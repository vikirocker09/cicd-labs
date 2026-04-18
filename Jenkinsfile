pipeline {
    agent any
    environment {
        VENV_DIR        = 'venv'
        EMAIL_RECIPIENT = 'emmpower.2008@gmail.com'
    }
    stages {
        stage('Build') {
            steps {
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Test') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pip install pytest pytest-cov
                    pytest tests/ -v
                '''
            }
        }
        stage('Deploy') {
            when { branch 'main' }
            steps {
                echo 'Tests passed - Deploying to staging...'
                sh 'echo Deployment step here'
            }
        }
    }
    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
