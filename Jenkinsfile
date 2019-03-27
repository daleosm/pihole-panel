// update with lintian stage on .deb file
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'ls ${WORKSPACE}/ | egrep -v 'DEBIAN|usr' 
                sh 'ls ${WORKSPACE}/ | egrep -v 'DEBIAN|usr' | xargs rm -rf'
                sh 'dpkg-deb --build $WORKSPACE /var/lib/jenkins/workspace/PiHole-Panel_master/PiHole-Panel-latest.deb' 
            }
        }
    }
}
