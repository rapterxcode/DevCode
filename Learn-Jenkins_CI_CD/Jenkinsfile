pipeline {
    agent {
        node {
            label 'docker-agent-python'
        }
    }
    triggers {
        pollSCM '* * * * *'
    }
    stages {
        // It's good practice to explicitly check out your SCM
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                echo "Building.."
                sh '''
                    cd Learn-Jenkins_CI_CD/myapp
                    # Create a Python virtual environment if it doesn't exist
                    python3 -m venv venv || true
                    # Activate the virtual environment
                    source venv/bin/activate
                    # Install dependencies into the virtual environment
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Test') {
            steps {
                echo "Testing.."
                sh '''
                    cd Learn-Jenkins_CI_CD/myapp
                    # Activate the virtual environment for testing
                    source venv/bin/activate
                    # Run your Python scripts using the Python from the virtual environment
                    python hello.py
                    python hello.py --name=phonerapterx
                '''
            }
        }
        stage('Deliver') {
            steps {
                echo 'Deliver....'
                sh '''
                    echo "doing delivery stuff.."
                    # If your delivery steps require Python packages, activate the venv here too
                    # cd Learn-Jenkins_CI_CD/myapp
                    # source venv/bin/activate
                    # python your_delivery_script.py
                '''
            }
        }
    }
}