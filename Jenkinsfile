// update with lintian stage on .deb file
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'dpkg-deb --build $WORKSPACE /var/lib/jenkins/workspace/PiHole-Panel_master/PiHole-Panel-latest.deb' 
            }
        }
    }
}
