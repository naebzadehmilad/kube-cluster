import logging,colorlog,os,stat,time
colorlog.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
import configparser , os
conf = configparser.ConfigParser()
def write_conf():
    conf.add_section('ETCD')
    conf.set('ETCD','nodes','127.0.0.1,127.0.0.2')
    conf.add_section('MASTER-NODES')
    conf.set('MASTER-NODES','nodes','127.0.0.3,127.0.0.4')
    conf.add_section('WORKER-NODES')
    conf.set('WORKER-NODES','nodes','127.0.0.5,127.0.0.6')
    conf.add_section('HAPROXY-NODES')
    conf.set('HAPROXY-NODES','nodes','127.0.0.7,127.0.0.8')
    conf.add_section('KEEPALIVED')
    conf.set('KEEPALIVED','ip','127.0.0.10')
    conf.add_section('PODSUBNET')
    conf.set('PODSUBNET','podsubnet','30.30.1.0/16')
    with open('kube.cfg','w') as configfile:
        conf.write(configfile)
def read_conf():
      conf.read('kube.cfg')
      global etcd
      global masternodes
      global workernodes
      global haproxynodes
      global keepalivedip
      etcd = str(conf.get('ETCD', 'nodes')).replace(' ', '').split(',')
      masternodes = str(conf.get('MASTER-NODES', 'nodes')).replace(' ', '').split(',')
      workernodes = str(conf.get('WORKER-NODES', 'nodes')).replace(' ', '').split(',')
      haproxynodes = str(conf.get('HAPROXY-NODES', 'nodes')).replace(' ', '').split(',')
      podsubnet = conf.get('PODSUBNET','podsubnet')
      keepalivedip = str(conf.get('KEEPALIVED','ip'))
if not os.path.exists('kube.cfg'):
    logging.info('  create kube.cfg \n')
    write_conf()
read_conf()
path=('kube.cfg')
a=os.stat(path)
b=time.ctime(a[stat.ST_MTIME])
print(b)
