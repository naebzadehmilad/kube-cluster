import  os,logging,colorlog
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
def playbook():
     os.system(' apt update ; apt install software-properties-common -y ;  apt-add-repository --yes --update ppa:ansible/ansible && apt install ansible -y ')

     if os.system('ansible-playbook -vvv  --flush-cache   playbook/playbook-swapoff.yml -i ansible/hosts'):
         logging.info('ansible-playbook -vvv  --flush-cache   playbook/playbook-swapoff.yml')
     else:
        logging.error('ansible-playbook -vvv  --flush-cache   playbook/playbook-swapoff.yml')
        exit(1)
     if os.system('ansible-playbook -vvv  --flush-cache   playbook/playbook-disable-swap-fstab.yml -i ansible/hosts'):
        logging.info('ansible-playbook -vvv  --flush-cache   playbook/playbook-disable-swap-fstab.yml')
     else:
         logging.error('ansible-playbook -vvv  --flush-cache   playbook/playbook-disable-swap-fstab.yml')
         exit(1)
     if os.system(' apt install python3-pip -y && pip3 install jinja2 configparser -i ansible/hosts'):
        logging.info('apt install python3-pip -y && pip3 install jinja2 configparser')
     else:
        logging.error('apt install python3-pip -y && pip3 install jinja2 configparser')
        exit(1)
     if os.system('ansible-playbook -vvv  --flush-cache playbook/playbook-install-etcd.yml -i ansible/hosts'):
        logging.info('ansible-playbook -vvv  --flush-cache playbook/playbook-install-etcd.yml ')

     else:
        logging.error('ansible-playbook -vvv  --flush-cache playbook/playbook-install-etcd.yml ')
        exit(1)
     if   os.system('ansible-playbook -vvv  --flush-cache  playbook/playbook-install-master.yml -i ansible/hosts'):
         logging.info('ansible-playbook -vvv  --flush-cache  playbook/playbook-install-master.yml ')

     else:
         logging.error('ansible-playbook -vvv  --flush-cache  playbook/playbook-install-master.yml ')
         exit(1)

     if os.system('ansible-playbook -vvv  --flush-cache   playbook/playbook-install-worker.yml -i ansible/hosts'):
         logging.info('ansible-playbook -vvv  --flush-cache   playbook/playbook-install-worker.yml')

     else:
         logging.error('ansible-playbook -vvv  --flush-cache   playbook/playbook-install-worker.yml ')
         exit(1)

     if os.system('ansible-playbook -vvv  --flush-cache   playbook/playbook-install-haproxy.yml -i ansible/hosts'):
         logging.info('ansible-playbook -vvv  --flush-cache   playbook/playbook-install-haproxy.yml ')

     else:
         logging.error('ansible-playbook -vvv  --flush-cache   playbook/playbook-install-haproxy.yml ')
         exit(1)

playbook()
