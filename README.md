### For Python 3.7 or above

* you need to install pyyaml: pip3 install pyyaml
* first backup will be full snapshot and afterwards it will be incremental snapshot only
* config file is hardcoded at /etc/zfs_backup_config.yml

``` YAML
config:
    pools:
        - "data/home"
        - "data/storage/application"
        - "data/storage/downloads"
        - "data/storage/kids"
        - "data/storage/music"
        - "data/storage/photo"
        - "data/storage/video"
        - "data/template"
    remote_address: "user@192.168.249.161 -i identity_file"
    keep: 10
    shutdown: 1
```
**remote_address** remote backup host or fqdn must include identification file key using **-i**

**keep** means number of snapshot will be retended.

**shutdown** is to shutdown backup destination server or not

make sure to give execute permission to /usr/local/bin/zfs_backup.py  chmod +x /usr/local/bin/zfs_backup.py

Remote Destination Pool must have the same structure like the Source Pool

Create a cron job to run zfs_backup.py on daily basis and you are all set, e.g. runs on everyday 2am
``` BASH
0 2 * * *       /usr/local/bin/zfs_backup.py
```
For PVE after backup hook script you can edit **/etc/pve/vzdump.cron** and use the **--script**  to execute
``` BASH
0 0 * * 1,3,5       root vzdump 100 101 102 103 104 105 106 108 109 111 114 115 118 253 --quiet 1 --storage pbs --mailnotification failure --mode snapshot --script /usr/local/bin/zfs_backup.py
```
Please Note,if you edit the backup job in PVE Web GUI, --script will be removed and you must add to the cron again
