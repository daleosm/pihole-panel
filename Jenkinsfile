pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'dpkg-deb --build $WORKSPACE' 
            }
        }
    }
}
