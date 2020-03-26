from config import *
import os ,colorlog
colorlog.basicConfig(level=logging.DEBUG)
def edit_host():
    os.system('export ANSIBLE_HOST_KEY_CHECKING=False')
    if not os.path.exists('ansible'):
        os.makedirs('ansible')
    if os.path.exists('./ansible/hosts'):
        os.remove('./ansible/hosts')
    ansiblehosts=open("ansible/hosts", "a+")
    ansiblehosts.write('[etcd]')
    for lenetcd in range(len(etcd)):
        ansiblehosts.write('\n{0}    '.format(etcd[lenetcd],lenetcd))
    else:
        ansiblehosts.write('\n[master]')
    for lenmasternodes in range(len(masternodes)):
        ansiblehosts.write('\n{0}    '.format(masternodes[lenmasternodes],lenmasternodes))
    else:
        ansiblehosts.write('\n[worker]')
    for lenworkernodes in range(len(workernodes)):
        ansiblehosts.write('\n{0}    '.format(workernodes[lenworkernodes],lenworkernodes))
    else:
        ansiblehosts.write('\n[haproxy]')
    for lenhaproxynodes in range(len(haproxynodes)):
            ansiblehosts.write('\n{0}    '.format(haproxynodes[lenhaproxynodes], lenhaproxynodes))
    ansiblehosts.close()

edit_host()
