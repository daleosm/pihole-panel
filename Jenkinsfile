pipeline {
    agent none 
    stages {
        stage('Build') { 
            agent {
                dockerfile {
                    filename 'Dockerfile.build'
                }
            }
            steps {
                sh 'python3 pihole-panel/main.py' 
            }
        }
    }
}
