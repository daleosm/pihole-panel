// update with lintian stage on .deb file
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh "rm -f ${WORKSPACE}/PiHole-Panel-latest.deb"
                sh "ls ${WORKSPACE}/ | egrep -v 'DEBIAN|usr' | xargs rm -rf"
                sh 'dpkg-deb --build $WORKSPACE' 
            }
        }
    }
}
