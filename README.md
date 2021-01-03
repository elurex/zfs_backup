### Using Python 3.7 or above

* you need to install pyyaml: pip3 install pyyaml

* config file is hardcoded at /etc/zfs_backup_config.yml

``` YAML
config:
    pools:
        - "data/home"
        - "data/storage/application"
        - "data/storage/av"
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

Create a cron job to run zfs_backup.py on daily basis and you are all set, e.go

0 2 * * * /usr/local/script/zfs_backup.py
