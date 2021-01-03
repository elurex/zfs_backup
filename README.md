### Using Python 3.7 or above

* you need to install pyyaml: pip3 install pyyaml

* config file is hardcoded at /etc/zfs_backup_config.yml


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
