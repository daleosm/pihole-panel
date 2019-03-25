// update with lintian stage on .deb file
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'rm /var/lib/jenkins/workspace/PiHole-Panel_master@tmp/*.deb' 
                sh 'rm /var/lib/jenkins/workspace/PiHole-Panel_master@tmp/uninstall_old.sh' 
                sh 'rm /var/lib/jenkins/workspace/PiHole-Panel_master@tmp/mainwindow.png'
                sh 'rm /var/lib/jenkins/workspace/PiHole-Panel_master@tmp/LICENSE'
                sh 'rm /var/lib/jenkins/workspace/PiHole-Panel_master@tmp/VERSION'
                sh 'rm /var/lib/jenkins/workspace/PiHole-Panel_master@tmp/README.md'
                
                sh 'dpkg-deb --build $WORKSPACE /var/lib/jenkins/workspace/PiHole-Panel_master/PiHole-Panel-latest.deb' 
            }
        }
    }
}
