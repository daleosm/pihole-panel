// update with lintian stage on .deb file
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'rm $WORKSPACE/*.deb' 
                sh 'rm $WORKSPACE/uninstall_old.sh' 
                sh 'rm $WORKSPACE/mainwindow.png'
                sh 'rm $WORKSPACE/LICENSE'
                sh 'rm $WORKSPACE/VERSION'
                sh 'rm $WORKSPACE/README.md'
                
                sh 'dpkg-buildpackage --build $WORKSPACE /var/lib/jenkins/workspace/PiHole-Panel_master/PiHole-Panel-latest.deb' 
            }
        }
    }
}
