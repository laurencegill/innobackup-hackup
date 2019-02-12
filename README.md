# innobackup-hackup
Script to backup and rotate using innobackupex 

Run out of cron with a MAILTO and you'll get an email on sucess, and a dump of the log on a failure

You'll need a .xtrabackup.my.cnf in your $HOME such as:

```
[client]
user=backupuser
password=mybackuppassword
```

To Do:
1. cli arguments
2. drop priviledges if run as root
3. incremental backups
