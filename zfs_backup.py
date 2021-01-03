#!/usr/bin/env python3
import subprocess, yaml
from datetime import datetime

config = yaml.safe_load(open('/etc/zfs_backup_config.yml'))
pools=config['config']['pools']
remote_address=config['config']['remote_address']
retention=config['config']['keep']+1
shutdown=config['config']['shutdown']

today = datetime.now().strftime("%Y-%m-%d-%H%M%S")

for i in pools:
    getsnapshots = subprocess.Popen("zfs list -t snapshot {}|grep {}".format(i,i),shell=True, stdout=subprocess.PIPE )
    snapshots = getsnapshots.communicate()[0].decode("utf-8").strip().splitlines()
    count = len(snapshots)

    if(count > 0):
        previous_snapshot = snapshots[count-1].split(" ")[0]

    #create today snapshot
    subprocess.run("zfs snapshot {}@{}".format(i,today), shell=True)
    count = count + 1

    #check if there is previous snapshot
    if(count > 1):
        checkremote = subprocess.Popen("ssh {} 'zfs list -t snapshot | grep {}'".format(remote_address,previous_snapshot),shell=True, stdout=subprocess.PIPE )

        if(i == checkremote.communicate()[0].decode("utf-8").strip().split('@')[0]):
            #send incremental snapshot
            subprocess.run("zfs send -i {} {}@{} | ssh {} zfs recv {}".format(previous_snapshot,i,today,remote_address,i),shell=True)
            #remove old snapshot
            if(count - retention > 0):
                for n in range(count - retention):
                    subprocess.run("zfs destroy {}".format(snapshots[n].split(" ")[0]),shell=True)
                    subprocess.run("ssh {} zfs destroy {}".format(remote_address,snapshots[n].split(" ")[0]),shell=True)
         else:
             #send complete snapshot since there is no increments
             subprocess.run("zfs send {}@{} | ssh {} zfs recv {} -F".format(i,today,remote_address,i),shell=True)
    else:
        #send complete snapshot since there is no increments
        subprocess.run("zfs send {}@{} | ssh {} zfs recv {} -F".format(i,today,remote_address,i),shell=True)

if(shutdown == 1):
    subprocess.run("ssh {} init 0".format(remote_address),shell=True)
