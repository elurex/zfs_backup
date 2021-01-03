#!/usr/bin/env python3
import subprocess, yaml
from datetime import date, timedelta

config = yaml.safe_load(open('/etc/zfs_backup_config.yml'))
pools=config['config']['pools']
remote_address=config['config']['remote_address']
retention=config['config']['keep']+1

today = date.today()
yesterday = date.today() - timedelta(1)
daytoremove = date.today() - timedelta(retention)

for i in pools:
    #create today snapshot
    subprocess.run("zfs snapshot {}@{}".format(i,today), shell=True)

    #check if there is yesterday snapshot
    checksnap = subprocess.Popen("zfs list -t snapshot | grep {}@{}".format(i,yesterday),shell=True, stdout=subprocess.PIPE )
    checkremote = subprocess.Popen("ssh {} 'zfs list -t snapshot | grep {}@{}'".format(remote_address,i,yesterday),shell=True, stdout=subp$

    if(i ==  checksnap.communicate()[0].decode("utf-8").strip().split('@')[0] and i == checkremote.communicate()[0].decode("utf-8").strip($
        #send incremental snapshot
        subprocess.run("zfs send -i {}@{} {}@{} | ssh {} zfs recv {}".format(i,yesterday,i,today,remote_address,i),shell=True)
        #remove old snapshot
        subprocess.run("ssh {} zfs destroy {}@{}".format(remote_address,i,daytoremove),shell=True)
    else:
        #send complete snapshot since there is no increments
        print("send complete snapshot")
        subprocess.run("zfs send {}@{} | ssh {} zfs recv {} -F".format(i,today,remote_address,i),shell=True)
