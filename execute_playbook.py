import  os
def playbook():
    os.system(' apt update ; apt install software-properties-common -y ;  apt-add-repository --yes --update ppa:ansible/ansible && apt install ansible -y ')
    os.system('sudo add-apt-repository ppa:deadsnakes/ppa ; apt install python3.7 -y && python3.7 --version')
    os.system(' apt install python3-pip -y && pip3 install jinja2 configparser ')
    os.system('ansible-playbook -vvv  --flush-cache playbook/playbook-install-etcd.yml ')
    os.system('ansible-playbook -vvv  --flush-cache  playbook/playbook-install-master.yml ')import  os,logging,colorlog
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
def playbook():
     os.system(' apt update ; apt install software-properties-common -y ;  apt-add-repository --yes --update ppa:ansible/ansible && apt install ansible -y ')

     if os.system('ansible-playbook -vvv  --flush-cache   playbook/playbook-swapoff.yml '):
         logging.info('ansible-playbook -vvv  --flush-cache   playbook/playbook-swapoff.yml')
     else:
        logging.error('ansible-playbook -vvv  --flush-cache   playbook/playbook-swapoff.yml')
        exit(1)
     if os.system('ansible-playbook -vvv  --flush-cache   playbook/playbook-disable-swap-fstab.yml '):
        logging.info('ansible-playbook -vvv  --flush-cache   playbook/playbook-disable-swap-fstab.yml')
     else:
         logging.error('ansible-playbook -vvv  --flush-cache   playbook/playbook-disable-swap-fstab.yml')
         exit(1)
     if os.system(' apt install python3-pip -y && pip3 install jinja2 configparser '):
        logging.info('apt install python3-pip -y && pip3 install jinja2 configparser')
     else:
        logging.error('apt install python3-pip -y && pip3 install jinja2 configparser')
        exit(1)
     if os.system('ansible-playbook -vvv  --flush-cache playbook/playbook-install-etcd.yml '):
        logging.info('ansible-playbook -vvv  --flush-cache playbook/playbook-install-etcd.yml ')

     else:
        logging.error('ansible-playbook -vvv  --flush-cache playbook/playbook-install-etcd.yml ')
        exit(1)
     if   os.system('ansible-playbook -vvv  --flush-cache  playbook/playbook-install-master.yml '):
         logging.info('ansible-playbook -vvv  --flush-cache  playbook/playbook-install-master.yml ')

     else:
         logging.error('ansible-playbook -vvv  --flush-cache  playbook/playbook-install-master.yml ')
         exit(1)

     if os.system('ansible-playbook -vvv  --flush-cache   playbook/playbook-install-worker.yml '):
         logging.info('ansible-playbook -vvv  --flush-cache   playbook/playbook-install-worker.yml')

     else:
         logging.error('ansible-playbook -vvv  --flush-cache   playbook/playbook-install-worker.yml')
         exit(1)

     if os.system('ansible-playbook -vvv  --flush-cache   playbook/playbook-install-haproxy.yml '):
         logging.info('ansible-playbook -vvv  --flush-cache   playbook/playbook-install-haproxy.yml')

     else:
         logging.error('ansible-playbook -vvv  --flush-cache   playbook/playbook-install-haproxy.yml')
         exit(1)

playbook()
    os.system('ansible-playbook -vvv  --flush-cache   playbook/playbook-install-worker.yml ')
playbook()
