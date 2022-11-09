#! /usr/bin/env python3
#
# This program analyzes a collection of files
# Create a list of files using glob.
# Create a dictionary, d, which is key'd by filename
# The value of each key is a dictionary with 3 keys,
# "written in" (a string), "mentions" ( list of file names), and
# "mentioned by" (a list of filenames).
#
#
import glob

# There were some files with "improper" names.
# jeffs@jeffs-desktop:~/work/expeditors/enhance_DBA_monitoring_script$ ls | egrep -v "\.sh|\.sql|\.java|\.class|\.py|\.pl|\.txt" | xargs file
# 65:                 empty
# check_instance_db:  Korn shell script, ASCII text executable
# check_instance_dbd: Korn shell script, ASCII text executable
# crypt:              Perl script text executable
# db2_terminate:      Korn shell script, ASCII text executable
# dba_monitor:        Korn shell script, ASCII text executable
# dba_monitord:       Korn shell script, ASCII text executable
# dba_schedule:       Korn shell script, ASCII text executable
# dba_scheduled:      Korn shell script, ASCII text executable
# dba_watchdog:       Korn shell script, ASCII text executable
# dba_watchdogd:      Korn shell script, ASCII text executable
# elektrik:           data
# gfile:              data
# gfile2:             data
# global_profile:     ASCII text
# goto_dba_user:      Korn shell script, ASCII text executable
# krap:               data
# nohup.out:          ASCII text
# trap:               data
# wrap:               data
# jeffs@jeffs-desktop:~/work/expeditors/enhance_DBA_monitoring_script$

WRITTEN_IN = "written_in"
MENTIONED_BY = "mentioned_by"
MENTIONS = "mentions"

filename_list = glob.glob("*.pl") + glob.glob("*.sh") + \
["check_instance_db", "check_instance_dbd", "crypt", "db2_terminate",
 "dba_monitor", "dba_monitord", "dba_schedule", "dba_scheduled",
 "dba_watchdog", "dba_watchdogd", "goto_dba_user"]

filename_list.sort()        # For convenience finding stuff

print(filename_list)

d = {}
for mentioner in filename_list:
    d[mentioner] = {WRITTEN_IN: "", MENTIONED_BY: [], MENTIONS: []}

for mentioner in filename_list:
    with open(mentioner, "r") as f:
        contents = f.readlines()
# The first line of the file should say what executes this file
    d[mentioner][WRITTEN_IN] = contents[0][:-1]

    for mentioned in filename_list:
        for line in contents:
            if mentioned in line:
                if mentioned not in d[mentioner][MENTIONS]:
                    d[mentioner][MENTIONS].append(mentioned)
                else:
                    pass
                if mentioner not in d[mentioned][MENTIONED_BY]:
                    d[mentioned][MENTIONED_BY].append(mentioner)
                else:
                    pass

for f in filename_list:
    print ( f"\nfile: {f}\nWritten in: {d[f][WRITTEN_IN]}\nMentions:\
    {d[f][MENTIONS]}\nIs Mentioned by: {d[f][MENTIONED_BY]}\n", "-"*40,"\n")

print(f"There are {len(filename_list)} files")