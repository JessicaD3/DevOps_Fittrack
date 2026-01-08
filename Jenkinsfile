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
                "C:\\Users\\UTILISATEUR_2025\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m venv venv
                call venv\\Scripts\\activate
                "C:\\Users\\UTILISATEUR_2025\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install --upgrade pip
                "C:\\Users\\UTILISATEUR_2025\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                "C:\\Users\\UTILISATEUR_2025\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pytest
                '''
            }
        }

        stage('Generate PDF') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                "C:\\Users\\UTILISATEUR_2025\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m app.pdf_report
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
