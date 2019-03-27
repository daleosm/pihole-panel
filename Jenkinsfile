// update with lintian stage on source files
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'dpkg-deb --build ${WORKSPACE}/Pihole-Panel PiHole-Panel-latest.deb'
            }
        }
    }
}
