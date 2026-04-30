pipeline {
    agent any

    stages {
        stage('Start Download') {
            steps {
                build job: 'download'
            }
        }

        stage('Train') {
            steps {
                build job: 'train model'
            }
        }

        stage('Deploy') {
            steps {
                build job: 'deploy'
            }
        }

        stage('Healthy') {
            steps {
                build job: 'healthy'
            }
        }
    }
}
