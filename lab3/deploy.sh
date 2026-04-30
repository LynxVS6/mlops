cd /var/lib/jenkins/workspace/download/
. ./my_env/bin/activate
cd ./lab3
export BUILD_ID=dontKillMe
export JENKINS_NODE_COOKIE=dontKillMe
path_model=$(cat best_model.txt)
mlflow models serve -m $path_model -p 5003 --no-conda &