from config import *
import os, logging
from jinja2 import Template
import colorlog

colorlog.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')


def create_playbook():
    if os.path.exists('playbook'):
        os.system('rm -rf playbook ')
    if not os.path.exists('playbook '):
        os.mkdir('playbook')
    if os.path.exists('install'):
        os.system('rm -rf install ')
    if not os.path.exists('install '):
        os.mkdir('install')
    f = open('playbook/externaletcd.yml', "w")
    template = Template("""
    - hosts: etcd
      remote_user: root
      become: true
      become_method: sudo
      tasks:
         - name: Transfer executable script script
           copy: src=../install/etcd-nodes dest=/tmp/etcd-nodes.sh mode=0777
         - name: install docker & k8s
           command: sh /tmp/etcd-nodes.sh   """)
    f.write(template.render())
    f.close()
    f = open('playbook/playbook-install-etcd.yml', "w")
    template = Template("""
   - hosts: master
     remote_user: root
     become: true
     become_method: sudo
     tasks:
        - name: Transfer executable script script
          copy: src=../install/repo-docker dest=/tmp/repo-docker.sh mode=0777
        - name: run script
          command: sh /tmp/repo-docker.sh && ssh /tmp/repo-kuber.sh && ssh /tmp/svc-docker.sh
        - name: Transfer executable script script2
          copy: src=../install/repo-kuber  dest=/tmp/repo-kuber.sh mode=0777
        - name: run script
          command: sh /tmp/repo-docker.sh && ssh /tmp/repo-kuber.sh && ssh /tmp/svc-docker.sh
        - name: Transfer executable script script3
          copy: src=../install/svc-docker  dest=/tmp/svc-docker.sh mode=0777
        - name: install docker and k8s
          command: sh /tmp/repo-docker.sh && ssh /tmp/repo-kuber.sh && ssh /tmp/svc-docker.sh""")
    f.write(template.render())
    f.close()
    f = open('playbook/playbook-install-master.yml', "w")
    template = Template("""
        - hosts: master
          remote_user: root
          become: true
          become_method: sudo
          tasks:
             - name: Transfer executable script script
               copy: src=../install/repo-docker dest=/tmp/repo-docker.sh mode=0777
             - name: run script
               command: sh /tmp/repo-docker.sh && ssh /tmp/repo-kuber.sh && ssh /tmp/svc-docker.sh
             - name: Transfer executable script script2
               copy: src=../install/repo-kuber  dest=/tmp/repo-kuber.sh mode=0777
             - name: run script
               command: sh /tmp/repo-docker.sh && ssh /tmp/repo-kuber.sh && ssh /tmp/svc-docker.sh
             - name: Transfer executable script script3
               copy: src=../install/svc-docker  dest=/tmp/svc-docker.sh mode=0777
             - name: install docker & k8s
               command: sh /tmp/repo-docker.sh && ssh /tmp/repo-kuber.sh && ssh /tmp/svc-docker.sh
        """)
    f.write(template.render())
    f.close()
    f = open('playbook/playbook-install-worker.yml', "w")
    template = Template("""
           - hosts: worker
             remote_user: root
             become: true
             become_method: sudo
             tasks:
                - name: Transfer executable script script
                  copy: src=../install/repo-docker dest=/tmp/repo-docker.sh mode=0777
                - name: run script
                  command: sh /tmp/repo-docker.sh && ssh /tmp/repo-kuber.sh && ssh /tmp/svc-docker.sh
                - name: Transfer executable script script2
                  copy: src=../install/repo-kuber  dest=/tmp/repo-kuber.sh mode=0777
                - name: add repo docker & k8s
                  command: sh /tmp/repo-docker.sh && ssh /tmp/repo-kuber.sh && ssh /tmp/svc-docker.sh
                - name: Transfer executable script script3
                  copy: src=../install/svc-docker  dest=/tmp/svc-docker.sh mode=0777
                - name: install docker and k8s
                  command: sh /tmp/repo-docker.sh && ssh /tmp/repo-kuber.sh && ssh /tmp/svc-docker.sh

            """)
    f.write(template.render())
    f.close()
    f = open('playbook/resolvconf.yml', "w")
    template = Template("""
          - hosts: all
            remote_user: root
            become: true
            become_method: sudo
            tasks:
               - name: shecan DNS
                 copy: src=../tmp/resolv.conf dest=/etc/resolv.conf
            """)
    f.write(template.render())
    f.close()
    f = open('playbook/playbook-disable-swap-fstab.yml', "w")
    template = Template("""
- hosts: etcd:master:worker
  remote_user: root
  become: true
  become_method: sudo
  tasks:
    - name: Disable SWAP in fstab since kubernetes can't work with swap enabled (2/2)
      replace:
      path: /etc/fstab
      regexp: '^([^#].*?\sswap\s+sw\s+.*)$'
      replace: '# \1'
            """)
    f.write(template.render())
    f.close()
    f = open('playbook/playbook-swapoff.yml', "w")
    template = Template("""
- hosts: etcd:master:worker
  remote_user: root
  become: true
  become_method: sudo
  tasks:
        - name: swapoff -a
          command: |
            swapoff -a
                """)
    f.write(template.render())
    f.close()
    f = open('playbook/playbook-install-haproxy.yml', "w")
    template = Template("""
           - hosts: haproxy
             remote_user: root
             become: true
             become_method: sudo
             tasks:
                - name: Transfer executable script script
                  copy: src=../install/haproxy-nodes dest=/tmp/haproxy-nodes.sh mode=0777
                - name: install haproxy & keepalived
                  command: sh /tmp/haproxy-nodes.sh
            """)
    f.write(template.render())
    f.close()
    f = open('install/etcd-nodes', "w")
    template = Template("""
            cat << EOF > /etc/systemd/system/kubelet.service.d/20-etcd-service-manager.conf
            [Service]
            ExecStart=
            #  Replace "systemd" with the cgroup driver of your container runtime. The default value in the kubelet is "cgroupfs".
            ExecStart=/usr/bin/kubelet --address=127.0.0.1 --pod-manifest-path=/etc/kubernetes/manifests --cgroup-driver=systemd
            Restart=always
            EOF
            
            # Reload and restart the kubelet
            systemctl daemon-reload && systemctl restart kubelet
                           """)
    f.write(template.render())
    f.close()
    f = open('install/repo-docker', "w")
    template = Template("""
                            # Add Docker’s official GPG key
            curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

            # Add Docker apt repository
            add-apt-repository \
              "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
              $(lsb_release -cs) \
              stable"

            # Install Docker CE
            apt-get update && apt-get install -y docker-ce
                           """)
    f.write(template.render())
    f.close()
    f = open('install/repo-kuber', "w")
    template = Template("""
            apt-get update -y && curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
            
            cat <<EOF | tee /etc/apt/sources.list.d/kubernetes.list
            deb https://apt.kubernetes.io/ kubernetes-xenial main
            EOF
            
            apt-get update -y && apt-get install -y kubelet kubeadm kubectl
            apt-mark hold kubelet kubeadm kubectl

                           """)
    f.write(template.render())
    f.close()
    f = open('install/svc-docker', "w")
    template = Template("""
                cat > /etc/docker/daemon.json <<EOF
                {
                  "exec-opts": ["native.cgroupdriver=systemd"],
                  "log-driver": "json-file",
                  "log-opts": {
                    "max-size": "100m"
                  },
                  "storage-driver": "overlay2"
                }
                EOF
                
                mkdir -p /etc/systemd/system/docker.service.d
                
                # Restart docker
                systemctl daemon-reload && systemctl restart docker
                           """)
    f.write(template.render())
    f.close()
    f = open('install/haproxy-nodes', "w")
    template = Template("""
                 apt-get install software-properties-common -y
                add-apt-repository ppa:vbernat/haproxy-2.1
                apt-get install haproxy=2.1.\* -y
                ap install keepalived -y

                            """)
    f.write(template.render())
    f.close()





create_playbook()
