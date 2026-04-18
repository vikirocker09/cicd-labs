pipeline {
    agent any
    environment {
        VENV_DIR        = 'venv'
        STAGING_HOST    = '172.31.39.230'
        DEPLOY_USER     = 'staging'
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
                echo "current branch: ${env.BRANCH_NAME}"
                echo 'Tests passed - Deploying to staging...'
                sh 'echo Deployment step here'
            }
        }
    }
    post {
    success {
        echo 'Pipeline succeeded!'
        emailext(
            to: 'emmpower.2008@gmail.com',
            subject: "SUCCESS: ${JOB_NAME} #${BUILD_NUMBER}",
            body: """
                Build Succeeded!
                Job: ${JOB_NAME}
                Build: #${BUILD_NUMBER}
                URL: ${BUILD_URL}
            """
        )
    }
    failure {
        echo 'Pipeline failed!'
        emailext(
            to: 'emmpower.2008@gmail.com',
            subject: "FAILED: ${JOB_NAME} #${BUILD_NUMBER}",
            body: """
                Build Failed!
                Job: ${JOB_NAME}
                Build: #${BUILD_NUMBER}
                URL: ${BUILD_URL}
            """
        )
    }
    always {
        sh 'rm -rf venv'
    }
}
}
