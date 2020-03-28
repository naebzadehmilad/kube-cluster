from config import *
import os  , logging
from  jinja2 import Template
import colorlog
colorlog.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
def ha():
    if os.path.exists('tmp/haproxy'):
       os.system('rm -rf tmp/haproxy')
    if not os.path.exists('tmp/haproxy'):
        os.mkdir('tmp/haproxy')
    lenhaproxynodes=len(haproxynodes)
    f = open('tmp/haproxy/haproxy.cfg', "w")
    template=Template("""global
        log /dev/log    local0
        log /dev/log    local1 notice
        chroot /var/lib/haproxy
        stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
        stats timeout 30s
        user haproxy
        group haproxy
        daemon

        # Default SSL material locations
        ca-base /etc/ssl/certs
        crt-base /etc/ssl/private

        # Default ciphers to use on SSL-enabled listening sockets.
        # For more information, see ciphers(1SSL). This list is from:
        #  https://hynek.me/articles/hardening-your-web-servers-ssl-ciphers/
        # An alternative list with additional directives can be obtained from
        #  https://mozilla.github.io/server-side-tls/ssl-config-generator/?server=haproxy
        ssl-default-bind-ciphers ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:RSA+AESGCM:RSA+AES:!aNULL:!MD5:!DSS
        ssl-default-bind-options no-sslv3
        frontend kubernetes
        bind {{keepalivedip}}:6443
        option tcplog
        mode tcp
        default_backend kubernetes-master-nodes

        backend kubernetes-master-nodes
                mode tcp
                balance roundrobin
                option tcp-check
                {% for j in range(lenhaproxynodes) %}
                server {{ haproxynodes[j] }}:6443 check fall 3 rise 2
                {% endfor %} """ )
    f.write(template.render(keepalivedip=keepalivedip,haproxynodes=haproxynodes,lenhaproxynodes=lenhaproxynodes))
    f.close()
    f = open('tmp/haproxy/keepalived.conf', "w")
    template=Template("""global_defs {
    notification_email {
        naebzadeh.milad@gmail.com     # Email address for notifications 
    }
    notification_email_from loadb01@domain.ext  # The from address for the notifications
    smtp_server 127.0.0.1     # You can specifiy your own smtp server here
    smtp_connect_timeout 15
}
  
# Define the script used to check if haproxy is still working
vrrp_script chk_haproxy { 
    script "killall -0 haproxy"
    interval 2 
    weight 2 
}
  
# Configuation for the virtual interface
vrrp_instance VI_1 {
    interface ens160
    state Master        # set this to BACKUP on the other machine
    priority 101       # set this to 100 on the other machine
    virtual_router_id 51
  
    smtp_alert          # Activate email notifications
  
    authentication {
        auth_type AH
        auth_pass mypassword1      # Set this to some secret phrase
    }
  
    # The virtual ip address shared between the two loadbalancers
    virtual_ipaddress {
        {{keepalivedip}}
    }
     
    # Use the script above to check if we should fail over
    track_script {
        chk_haproxy
    }
}

 """ )
    f.write(template.render(keepalivedip=keepalivedip,haproxynodes=haproxynodes,lenhaproxynodes=lenhaproxynodes))
    f.close()
    for i in range(lenhaproxynodes):
                os.system('scp -r tmp/haproxy/haproxy.cfg root@{0}:/etc/haproxy'.format(haproxynodes[i]))
                os.system('scp -r tmp/haproxy/keepalived.conf root@{0}:/etc/keepalived/'.format(haproxynodes[i]))
                logging.info('scp from tmp/haproxy/haproxy.cfg&keepalived.conf to root@{0}:/etc/haproxy && root@{0}:/etc/keepalived/'.format(haproxynodes[i]))

ha()
