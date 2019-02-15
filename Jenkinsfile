// update with lintian stage on .deb file
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'dpkg-deb --build $WORKSPACE PiHole-Panel_master/PiHole-Panel-latest.deb' 
            }
        }
    }
}
