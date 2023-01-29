pipeline {
  agent { node { label 'ubuntu' }}
  stages {
    stage('version') {
      steps {
        sh 'python3 --version'
      }
    }
    stage('hello') {
      steps {
        sh 'python3 test/test.py'
      }
    }
  }
}
