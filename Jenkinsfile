// update with lintian stage on .deb file
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'rm /var/lib/jenkins/workspace/PiHole-Panel_master/*.deb' 
                sh 'rm /var/lib/jenkins/workspace/PiHole-Panel_master/uninstall_old.sh' 
                sh 'rm /var/lib/jenkins/workspace/PiHole-Panel_master/mainwindow.png'
                sh 'rm /var/lib/jenkins/workspace/PiHole-Panel_master/LICENSE'
                sh 'rm /var/lib/jenkins/workspace/PiHole-Panel_master/VERSION'
                sh 'rm /var/lib/jenkins/workspace/PiHole-Panel_master/README.md'
                
                sh 'dpkg-deb --build $WORKSPACE /var/lib/jenkins/workspace/PiHole-Panel_master/PiHole-Panel-latest.deb' 
            }
        }
    }
}
