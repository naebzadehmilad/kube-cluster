#!/usr/bin/python3.6
from config import *
import logging , os , time,colorlog
colorlog.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
def hosts():
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    if os.path.exists("tmp/hosts"):
        os.remove("tmp/hosts")
    hfile = open('tmp/hosts', 'a+')
    hfile_check = open('/etc/hosts', 'r')
    for line in hfile_check:
            if  '############Added by script#############' in line:
                logging.warn('\n/etc/hosts  \nplease delete this line   \n'+ line +' \nand afterwards\n')

                exit(1)
    hfile.write('\n############Added by script#############\n')
    for lenetcd in range(len(etcd)):
        hfile.write('\n{0}   etcd-{1} '.format(etcd[lenetcd], lenetcd))
    for lenmasternodes in range(len(masternodes)):
        hfile.write('\n{0}   k8sm-{1} '.format(masternodes[lenmasternodes], lenmasternodes))
    for lenworkernodes in range(len(workernodes)):
        hfile.write('\n{0}   k8sw-{1} '.format(workernodes[lenworkernodes], lenworkernodes))
    for lenhaproxynodes in range(len(haproxynodes)):
            hfile.write('\n{0}   haproxy-{1} '.format(haproxynodes[lenhaproxynodes], lenhaproxynodes))
    hfile.write('\n{0}   k8s-haproxy '.format(keepalivedip))

    hfile.close()

    ###send tmp/hosts
    for lenetcd in range(len(etcd)):
            time.sleep(1)
            if  (
                    os.system(('scp tmp/hosts root@{0}:/tmp/'.format(etcd[lenetcd]))) == 0
                    and 
                    os.system("ssh root@{0} 'cat /tmp/hosts >> /etc/hosts'".format(etcd[lenetcd])) == 0

            ):
                    logging.info('send tmp/hosts to {0} :/tmp/hosts \n'.format(etcd[lenetcd]))
            else:
                    logging.error('NOT send tmp/hosts to {0} :/tmp/hosts \n'.format(etcd[lenetcd]))
                
    for lenmasternodes in range(len(masternodes)):
            time.sleep(1)
            if (
                  os.system("ssh root@{0} 'cat /tmp/hosts >> /etc/hosts'".format(masternodes[lenmasternodes])) == 0
                  and 
                  os.system('scp tmp/hosts root@{0}:/tmp/'.format(masternodes[lenmasternodes])) == 0
             ):
                  logging.info('send tmp/hosts to {0} :/tmp/hosts \n'.format(masternodes[lenmasternodes]))
            else:
                  logging.error('NOT send tmp/hosts to {0} :/tmp/hosts \n'.format(masternodes[lenmasternodes]))
                  
    for lenworkernodes in range(len(workernodes)):
            if (
                 os.system("ssh root@{0} 'cat /tmp/hosts >> /etc/hosts'".format(workernodes[lenworkernodes])) == 0
                 and 
                 os.system('scp tmp/hosts root@{0}:/tmp/'.format(workernodes[lenworkernodes])) == 0
            ):
                logging.info('send tmp/hosts to {0} :/tmp/hosts \n'.format(workernodes[lenworkernodes]))
            else:
                logging.error('NOT send tmp/hosts to {0} :/tmp/hosts \n'.format(workernodes[lenworkernodes]))
                   
    for lenhaproxynodes in range(len(haproxynodes)):
          if (
                  os.system("ssh root@{0} 'cat /tmp/hosts >> /etc/hosts'".format(haproxynodes[lenhaproxynodes])) == 0
                  and 
                  os.system('scp tmp/hosts root@{0}:/tmp/'.format(haproxynodes[lenhaproxynodes])) == 0
             ):
              logging.info('send tmp/hosts to {0} :/tmp/hosts \n'.format(haproxynodes[lenhaproxynodes]))
          else:
              logging.error('NOT send tmp/hosts to {0} :/tmp/hosts \n'.format(haproxynodes[lenhaproxynodes]))
              
hosts()
