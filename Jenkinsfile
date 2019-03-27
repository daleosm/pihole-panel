// update with lintian stage on .deb file
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh "ls ${WORKSPACE}/ | egrep -v 'DEBIAN|usr' | xargs rm -rf"
                sh "ls ${WORKSPACE}/data | egrep -v 'usr' | xargs rm -rf"
                sh 'dpkg-deb --build ${WORKSPACE}/ PiHole-Panel-latest.deb' 
            }
        }
    }
}
