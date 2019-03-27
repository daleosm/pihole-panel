// update with lintian stage on source files
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh "ls ${WORKSPACE}/ | egrep -v 'DEBIAN|usr' | xargs rm -rf"
                sh 'dpkg-deb --build ${WORKSPACE}/ ../PiHole-Panel-latest.deb'
                sh 'cd ../'
                sh 'mv PiHole-Panel-latest.deb ${WORKSPACE}/'
            }
        }
    }
}
