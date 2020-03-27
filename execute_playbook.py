import  os
def playbook():
    os.system(' apt update ; apt install software-properties-common -y ;  apt-add-repository --yes --update ppa:ansible/ansible && apt install ansible -y ')
    os.system('sudo add-apt-repository ppa:deadsnakes/ppa ; apt install python3.7 -y && python3.7 --version')
    os.system(' apt install python3-pip -y && pip3 install jinja2 configparser ')
    os.system('ansible-playbook -vvv  --flush-cache playbook/playbook-install-etcd.yml ')
    os.system('ansible-playbook -vvv  --flush-cache  playbook/playbook-install-master.yml ')
    os.system('ansible-playbook -vvv  --flush-cache   playbook/playbook-install-worker.yml ')
playbook()
