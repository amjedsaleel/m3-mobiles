pipeline {
    agent any
    // tools {
    //     jdk 'jdk17'
    //     nodejs 'node:16.17.0'
    // }
    environment {
        SCANNER_HOME = tool 'sonar-scanner'
        CURRENT_WORKSPACE = pwd()
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
                sh '${CURRENT_WORKSPACE}/venv/bin/pip install -r requirements.txt'
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
                sh 'trivy fs --format template --template "@/usr/local/share/trivy/templates/html.tpl" --ignore-unfixed -o trivy-fs-report.html .'
            }
        }
        stage('Docker build') {
            steps {
                sh 'docker build -t  amjedsaleel/m3-mobile:${BUILD_NUMBER} .'
            }
        }
        stage('Trivy image scan') {
            steps {
                sh 'trivy image --format template  --template "@/usr/local/share/trivy/templates/html.tpl" --ignore-unfixed -o trivy-image-report.html amjedsaleel/m3-mobile:${BUILD_NUMBER}'
            }
        }
        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', passwordVariable: 'PASSWORD', usernameVariable: 'USERNAME')]) {
                    sh 'docker login -u $USERNAME -p $PASSWORD'
                }
                sh 'docker push amjedsaleel/m3-mobile:${BUILD_NUMBER}'
                sh 'docker logout'
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
                attachmentsPattern: 'trivy-fs-report.html,trivy-image-report.html'
            
        }
    }
}
