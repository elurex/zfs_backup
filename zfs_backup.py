#!/usr/bin/python3
import subprocess, yaml
from datetime import datetime

config = yaml.safe_load(open('/etc/zfs_backup_config.yml'))
pools=config['config']['pools']
remote_address=config['config']['remote_address']
retention=config['config']['keep']+1
shutdown=config['config']['shutdown']

today = datetime.now().strftime("%Y-%m-%d-%H%M%S")

for a in pools:
    i=a.split(",")[0]
    r=a.split(",")[1]
    getsnapshots = subprocess.Popen("/usr/sbin/zfs list -t snapshot {}".format(i),shell=True, stdout=subprocess.PIPE )
    snapshots = getsnapshots.communicate()[0].decode("utf-8").strip().splitlines()
    count = len(snapshots)

    if(count > 0):
        previous_snapshot = snapshots[count-1].split(" ")[0]
        snapshot_stamp = previous_snapshot.split("@")[1]

    #create today snapshot
    subprocess.run("/usr/sbin/zfs snapshot {}@{}".format(i,today), shell=True)
    count = count + 1

    #check if there is previous snapshot
    if(count > 1):
        checkremote = subprocess.Popen("/usr/bin/ssh {} 'zfs list -t snapshot | grep {}@{}'".format(remote_address,r,snapshot_stamp),shell=True, stdout=subprocess.PIPE )

        if(i == checkremote.communicate()[0].decode("utf-8").strip().split('@')[0]):
            #send incremental snapshot
            subprocess.run("/usr/sbin/zfs send -i {} {}@{} | /usr/bin/ssh {} zfs recv {}".format(previous_snapshot,i,today,remote_address,r),shell=True)
            #remove old snapshot
            if(count - retention > 0):
                for n in range(count - retention):
                    subprocess.run("/usr/sbin/zfs destroy {}".format(snapshots[n].split(" ")[0]),shell=True)
                    subprocess.run("/usr/bin/ssh {} zfs destroy {}".format(remote_address,snapshots[n].replace(i,r).split(" ")[0]),shell=True)
        else:
             #send complete snapshot since there is no increments
             subprocess.run("/usr/sbin/zfs send {}@{} | /usr/bin/ssh {} zfs recv {} -F".format(i,today,remote_address,r),shell=True)
    else:
        #send complete snapshot since there is no increments
        subprocess.run("/usr/sbin/zfs send {}@{} | /usr/bin/ssh {} zfs recv {} -F".format(i,today,remote_address,r),shell=True)

if(shutdown == 1):
    subprocess.run("/usr/bin/ssh {} init 0".format(remote_address),shell=True)
