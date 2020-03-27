import logging , time , os , fileinput
from  jinja2 import Template
from config import *
import colorlog
colorlog.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
lenetcd=len(etcd)
lst = []
for m in range(lenetcd):
    lst.append(("etcd-{1}=https://{0}:2380".format(etcd[m], m)))
def etcd_init():
    os.system('rm -rf tmp/etcd*')
    for x in range(lenetcd) :
        os.mkdir('tmp/etcd-{0}'.format(x))
        path='tmp/etcd-{0}'.format(x)
        f = open( str(path)+'/kubeadmcfg.yml' , "w")
        template= Template(""" 
    apiVersion: kubeadm.k8s.io/v1beta2
    kind: ClusterConfiguration
    kubernetesVersion: 1.17.3
    etcd:
        local:
            serverCertSANs:
            - "{{etcd[x]}}"
            peerCertSANs:
            - "{{etcd[x]}}"
            extraArgs:
                initial-cluster:
                initial-cluster-state: new
                name: etcd-{{x}}
                listen-peer-urls: https://{{etcd[x]}}:2380
                listen-client-urls: https://{{etcd[x]}}:2379
                advertise-client-urls: https://{{etcd[x]}}:2379
                initial-advertise-peer-urls: https://{{etcd[x]}}:2380
    """)
        f.write( template.render(etcd=etcd , x=x ) )
    res_etcd=('initial-cluster: '+str(lst).replace("[","").replace(' ','').replace(']','').replace("'",""))
    f.close()
    for i in range(lenetcd):
        path1 = 'tmp/etcd-{0}/'.format(i)
        print(path1)
        for line in fileinput.input(str(path1)+'kubeadmcfg.yml',inplace=True):
             print (line.replace("initial-cluster:", res_etcd))
    logging.info("\nrun kubeadm init phase certs etcd-ca to etcd0-{0}\n ".format(etcd[0]))
    os.system("ssh root@{0} 'kubeadm init phase certs etcd-ca' ".format(etcd[0]))
    logging.info("\ncopy tmp/etcd-{0}/kubeadmcfg.yml to {0}\n ".format( etcd[0]))
    os.system('scp -r  tmp/etcd-*/ root@{0}:/tmp/'.format( etcd[0]))
    for n in range(lenetcd):
         os.system("ssh root@{1} 'kubeadm init phase certs etcd-server --config=/tmp/etcd-{0}/kubeadmcfg.yml'".format(n,etcd[0]))
         logging.info('\n kubeadm init phase certs etcd-server --config=/tmp/etcd-{0}/kubeadmcfg.yml --Done at  {0} \n '.format(etcd[0]))
         os.system("ssh root@{1} 'kubeadm init phase certs etcd-peer --config=/tmp/etcd-{0}/kubeadmcfg.yml'".format(n,etcd[0]))
         logging.info('\n kubeadm init phase certs etcd-peer --config=/tmp/etcd-{0}/kubeadmcfg.yml --Done at  {0} \n '.format(etcd[0]))
         os.system("ssh root@{1} 'kubeadm init phase certs etcd-healthcheck-client --config=/tmp/etcd-{0}/kubeadmcfg.yml'".format(n,etcd[0]))
         logging.info('\n kubeadm init phase certs etcd-healthcheck-client --config=/tmp/etcd-{0}/kubeadmcfg.yml --Done at  {0} \n '.format(etcd[0]))
         os.system("ssh root@{1} 'kubeadm init phase certs apiserver-etcd-client --config=/tmp/etcd-{0}/kubeadmcfg.yml'".format(n,etcd[0]))
         logging.info('\n\n kubeadm init phase certs apiserver-etcd-client --config=/tmp/etcd-{0}/kubeadmcfg.yml --Done at  {0} \n\n '.format(etcd[0]))
         os.system("ssh root@{1} 'cp -R /etc/kubernetes/pki/ /tmp/etcd-{0}/ '".format(n,etcd[0]))
         logging.info('\n cp -R /etc/kubernetes/pki/ /tmp/etcd-{0}/ --Done at  {0} \n '.format(etcd[0]))
         os.system("ssh root@{1} 'find /etc/kubernetes/pki -not -name ca.crt -not -name ca.key -type f -delete'".format(n,etcd[0]))
         logging.info('\n  find /etc/kubernetes/pki -not -name ca.crt -not -name ca.key -type f -delete --Done at  {0} \n '.format(etcd[0]))

    for j in range(lenetcd):
          logging.info('\n copy from /tmp/etcd-{1}/pki to {0}/etc/kubernetes/   \n '.format(etcd[j],j))
          time.sleep(3)
          os.system("ssh  root@{2} 'scp -r  /tmp/etcd-{1}/* root@{0}:/etc/kubernetes/' ".format(etcd[j],j,etcd[0]))
          logging.info("\n  ssh root@{0} 'kubeadm init phase etcd local --config=/etc/kubernetes/kubeadmcfg.yml ' \n\n\n\n ".format(etcd[j]))
          os.system("ssh root@{0}  'kubeadm init phase etcd local --config=/etc/kubernetes/kubeadmcfg.yml'".format(etcd[j]))
    #     os.system('find tmp/etcd-{0}/ -name ca.key -type f -delete ; find tmp/etcd-{0}/ -name ca.key -type f -delete'.format(n))
    #     os.system('scp -r  tmp/etcd-{0}/pki root@{1}:/etc/kubernetes'.format(n,etcd[n]))
    #     os.system("ssh root@{0} 'kubeadm init phase etcd local --config=/etc/kubernetes/kubeadmcfg.yml | 'echo swapoff -a >> /root/.bashrc' ".format(etcd[n]))
    # #ansible-playbook playbook/playbook-etcdkeys.yml -i localhost, -k
etcd_init()
