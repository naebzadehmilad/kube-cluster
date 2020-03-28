from config import *
import os , fileinput
from  jinja2 import Template
import colorlog
colorlog.basicConfig(level=logging.DEBUG)
def masternodes_init():
    if os.path.exists('tmp/masterinit/'):
        os.remove('tmp/masterinit/m0.yml')
    if not os.path.exists('tmp/masterinit/'):
        os.mkdir('tmp/masterinit')
    f = open('tmp/masterinit/m0.yml', "w")
    etcdlen=len(etcd)
    template=Template("""
    apiVersion: kubeadm.k8s.io/v1beta2
    kind: ClusterConfiguration
    kubernetesVersion: stable
    controlPlaneEndpoint: "k8s-haproxy:6444" #default 6443
    networking:
            podSubnet: "{{podsubnet}}"
    etcd:
        external:
            endpoints:
            {% for z in range(etcdlen) %}
            - https://{{ etcd[z] }}:2379
            {% endfor %}
            caFile: /etc/kubernetes/pki/etcd/ca.crt
            certFile: /etc/kubernetes/pki/apiserver-etcd-client.crt
            keyFile: /etc/kubernetes/pki/apiserver-etcd-client.key """ )
    f.write(template.render(etcd=etcd,etcdlen=etcdlen,podsubnet=podsubnet))
    f.close()
    print('\ncopy  tmp/masterinit/master0.yml to master0\n')
    os.system('scp -r  tmp/masterinit/m0.yml root@{0}:/tmp/master0.yml'.format(masternodes[0]))
    os.system("ssh root@{0} 'mkdir -p /etc/kubernetes/pki/etcd/' ".format(masternodes[0]))
    print('\ncopy ca.crt to master0 \n')
    os.system('scp -r  /etc/kubernetes/pki/etcd/ca.crt root@{0}:/etc/kubernetes/pki/etcd/'.format(masternodes[0]))
    print('\ncopy apiserver-etcd-client.crt to master0\n')
    os.system('scp -r  /etc/kubernetes/pki/apiserver-etcd-client.crt root@{0}:/etc/kubernetes/pki/'.format(masternodes[0]))
    print('\ncopy apiserver-etcd-client.key to master0\n')
    os.system('scp -r  /etc/kubernetes/pki/apiserver-etcd-client.key root@{0}:/etc/kubernetes/pki/'.format(masternodes[0]))
    print('\n kubeadm init --config /tmp/master0.yml --upload-certs\n')
    os.system("ssh root@{0} 'kubeadm init --config /tmp/master0.yml --upload-certs ' ".format(masternodes[0]))
    if exit(0) :
        os.system("ssh root@{0} '   mkdir -p $HOME/.kube &&  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config &&   sudo chown $(id -u):$(id -g) $HOME/.kube/config ' ".format(masternodes[0]))
        print(" run this command for install weavenet from {0} \nkubectl apply -f https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d  '\n' ".format(masternodes[0]))
masternodes_init()
