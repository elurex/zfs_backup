### Using Python 3.7 or above

* you need to install pyyaml: pip3 install pyyaml

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
    remote_address: "192.168.249.161"
    keep: 10
```
remote_address can supply with username/password or with key
keep means number of snapshot will be retended.

Remote destination Pool must have the same structure like the Source Pool

Create a cron job to run zfs_backup.py on daily basis and you are all set, e.g. runs on everyday 2am

0 2 * * * /usr/local/bin/zfs_backup.py

For PVE after backup hook you can edit /etc/pve/vzdump.cron and use the --script  to execute

0 0 * * 1,3,5       root vzdump 100 101 102 103 104 105 106 108 109 111 114 115 118 253 --quiet 1 --storage pbs --mailnotification failure --mode snapshot --script /usr/local/bin/zfs_backup.py
