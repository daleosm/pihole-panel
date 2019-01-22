pipeline {
    agent none 
    stages {
        stage('Build') { 
            agent {
                docker {
                    image 'ubuntu'
                }
            }
            steps {
                sh 'python3 pihole-panel/main.py' 
            }
        }
    }
}
