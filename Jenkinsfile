pipeline {
    agent { label 'agent-1' }
    tools {
        jdk 'jdk17'
        nodejs 'node:16.17.0'
    }
    environment {
        SCANNER_HOME = tool 'sonar-scanner'
    }
    stages {
        stage('clean workspace') {
            steps {
                cleanWs()
            }
        }
        stage('Checkout from Git') {
            steps {
                git branch: 'main', url: 'https://github.com/amjedsaleel/m3-mobiles'
            }
        }
        stage("Sonarqube Analysis") {
            steps {
                script {
                    def scannerHome = tool 'sonar-scanner';
                    withSonarQubeEnv("sonarqube-sever") {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
        stage("Quality Gate") {
            steps {
              timeout(time: 1, unit: 'HOURS') {
                waitForQualityGate abortPipeline: true, credentialsId: 'sonarqube-tocken'
              }
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'python3 -m venv venv'
                sh '/home/jenkins-agent/workspace/workspace/m3-mobiles/venv/bin/pip install -r requirements.txt'
            }
        }
        
        stage('OWASP FS SCAN') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit', odcInstallation: 'DP-check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
        stage('TRIVY FS SCAN') {
            steps {
                sh 'trivy fs --format template --template "@/usr/local/share/trivy/templates/html.tpl" -o trivy-fs-report.html .'
            }
        }
        stage('Docker build') {
            steps {
                sh 'docker build -t  amjedsaleel/m3-mobile:${BUILD_NUMBER} .'
            }
        }
    }

    post {
        always {
            emailext subject: '$JOB_NAME',
                body: '$DEFAULT_CONTENT',
                replyTo: 'no-reply@white.com',
                attachLog: true,
                to: 'whitekail777@gmail.com',
                mimeType: 'text/html',
                attachmentsPattern: 'trivy-fs-report.html,index.html'
            
        }
    }
}