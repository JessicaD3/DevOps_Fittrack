pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                pytest
                '''
            }
        }

        stage('Generate PDF') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                python -m app.pdf_report
                '''
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: '**/*.pdf', fingerprint: true
        }
    }
}
