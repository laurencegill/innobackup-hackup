#!/usr/bin/python
import subprocess
import re
import datetime
import os
import time
import shutil
import ConfigParser
import sys

home = os.getenv("HOME")+"/"
config = ConfigParser.ConfigParser()
config.read(home+".xtrabackup.my.cnf")
user = config.get("client", "user")
pw = config.get("client", "password")
backup_location = home+"backups/"
epoch_secs = time.time()
c = "None"
day = datetime.datetime.today().isoweekday()
day_of_month = datetime.datetime.now().day
bname = os.path.basename(sys.argv[0][:-3])
outfile = (home + bname + ".log")


## Decide whether this is a daily/weekly/monthly backup ##
## Do full and monthly backups on a Friday, otherwise daily ##
if (day == 5):
  if (day_of_month <= 7):
    backup_dir = (backup_location+"monthly")
    keep_days = 365
  else:
    backup_dir = (backup_location+"weekly")
    keep_days = 31
else:
    backup_dir = (backup_location+"daily")
    keep_days = 14


## Do the backup ##
flog = open(outfile, "w")
xb = subprocess.call(["innobackupex", "--history", "--compress", "--user="+user, "--host=localhost", "--password="+pw, backup_dir], stderr=flog)
flog.close()


## Check the return code of the program ##
if (xb == 0):
  print ("Backup return status OK.")
elif (xb == 1):
  print ("Backup return status is Error.")
else:
  print ("Unknown returncode.")


## Check the log file confirms the backup return code ##
logfile = open(outfile, 'r')
for line in logfile:
  # match the date (greedy), a space, the time, space, the string and the EOL:
  if re.match("(^[0-9]*)(\s)([0-9]{2}:[0-9]{2}:[0-9]{2})\scompleted OK!$", line):
    c = line
logfile.closed


## Check the content and output a final status ##
if "completed OK" in c:
  print "OK status detected in backup log:"
  print " "+c
else:
  print ("ERROR FAIL detected in backup log:")
  flog = open(outfile, "r")
  log_content = flog.read()
  print (log_content)
  quit()


## Remove the oldest backups ##
print ("Purging backups in " + backup_dir + " older than " + repr(keep_days) + " days")
os.chdir(backup_dir)
cwd = os.getcwd()
dirs=os.listdir(backup_dir)
for d in dirs:
  if os.path.isdir(d):
    days_old = int(round((epoch_secs - os.stat(d).st_mtime) / 86400,0))
    print d + " is " + repr(days_old) + " days old"
    if os.stat(d).st_mtime < (epoch_secs - keep_days * 86400):
      print "Removing "+d,"from "+cwd
      shutil.rmtree(d)
