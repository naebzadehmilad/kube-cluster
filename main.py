import time , colorlog,logging
colorlog.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
from config import *
if etcd == ['127.0.0.1', '127.0.0.2'] and masternodes == ['127.0.0.3', '127.0.0.4']:
    logging.info('please change kube.cfg config and execute script\n')
    exit(1)
try:
    time.sleep(1)
    logging.info('hosts file is running \n')
    from hosts import *
except:
    logging.error('hosts file error')
    exit(1)
try:
    time.sleep(1)
    logging.info('createplaybook file is running \n')
    from createplaybook import *
except:
    logging.error('createplaybook file error')
    exit(1)
try:
    time.sleep(1)
    logging.info('init_ansible file is running \n')
    from init_ansible import *
except:
    logging.error('init_ansible file error ')
    exit(1)

try:
    time.sleep(1)
    logging.info('execute_playbook file is running \n')
    from execute_playbook import *
except:
    logging.error('execute_playbook file error')
    exit(1)
try:
    time.sleep(1)
    logging.info('init_etcd file is running \n')
    from init_etcd import *
except:
    logging.error('init_etcd file error')
    exit(1)
try:
    time.sleep(1)
    logging.info('init_haproxy file is running \n')
    from init_haproxy import *
except:
    logging.error('init_haproxy file error')
    exit(1)
try:
    time.sleep(1)
    logging.info('setup_masternodes file is running \n')
    from setup_masternodes import *
except:
    logging.error('setup_masternodes file error')
    exit(1)
