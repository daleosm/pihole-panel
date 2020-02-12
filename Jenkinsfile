pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '5', artifactNumToKeepStr: '5'))
    }

    stages {
        stage('Build') {
            steps {
                dir("pihole-panel") {
                    sh "apt update"
                    sh "apt install devscripts -y"
                    sh "debuild -us -uc"
                    /*
                        Sign and upload from workstation since instance is not online 24/7
                        and would require storing GPG passphrase in an unsecure manner.

                    sh 'dput ppa:daleosm/pihole-panel pihole-panel_[VERSION]_source.changes'
                    */
                }
            }
        }
    }
}
