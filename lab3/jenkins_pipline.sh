#№1. download
python3 -m venv ./my_env
. ./my_env/bin/activate
cd ./lab3	
python3 -m ensurepip --upgrade
pip3 install setuptools
pip3 install -r requirements.txt
python3 download.py
#-----------------------

#№2. train_model 
echo "Start train model"
cd /var/lib/jenkins/workspace/download/
. ./my_env/bin/activate
cd ./lab3
python3 train_model.py > best_model.txt
#------------------------

#3. deploy 
cd /var/lib/jenkins/workspace/download/
. ./my_env/bin/activate
cd ./lab3
export BUILD_ID=dontKillMe
export JENKINS_NODE_COOKIE=dontKillMe
path_model=$(cat best_model.txt)
mlflow models serve -m $path_model -p 5003 --no-conda &
#------------------------

#4. healthy (status service)
curl http://127.0.0.1:5003/invocations -H"Content-Type:application/json"  --data '{"inputs": [[0.038075906, 0.050680119, 0.061696207, 0.021872354, -0.044223498, -0.034820763, -0.043400846, -0.002592262, 0.019907487, -0.017646125]]}'


#pipeline
pipeline {
    agent any

    stages {
        stage('Download') {
            steps {
                
                build job: 'download'
            }
        }
        
        stage ('Train') {
            
            steps {
                build job: 'train_model'
            
            }
        }
        
        stage ('Deploy') {
            steps {
                build job: 'deploy'
            }
        }
        
        stage ('Status') {
            steps {
                build job: 'healthy'
            }
        }
    }
}

