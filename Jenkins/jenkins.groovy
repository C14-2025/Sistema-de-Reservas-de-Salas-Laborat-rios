pipeline {
    agent any

    tools {
        python "python3.10"
        nodejs "node18"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/C14-2025/Sistema-de-Reservas-de-Salas-Laborat-rios'
            }
        }

        stage('Backend - Instalar Dependências') {
            steps {
                dir('backend') {
                    sh 'python -m pip install --upgrade pip'
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Backend - Testes') {
            steps {
                dir('backend') {
                    sh 'pytest --junitxml=report.xml'
                }
            }
            post {
                always {
                    junit 'backend/report.xml'
                }
            }
        }

        stage('Frontend - Instalar Dependências') {
            steps {
                dir('frontend') {
                    sh 'npm install'
                }
            }
        }

        stage('Frontend - Testes') {
            steps {
                dir('frontend') {
                    sh 'npm test --watchAll=false --ci --json --outputFile=test-results.json'
                }
            }
        }

        stage('Frontend - Build') {
            steps {
                dir('frontend') {
                    sh 'npm run build'
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline finalizada com sucesso!"
        }
        failure {
            echo "Pipeline falhou!"
        }
    }
}
