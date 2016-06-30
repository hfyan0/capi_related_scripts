#!/usr/bin/python
import time, os, sys
import fnmatch
import subprocess

TESTING=False
problem_line=""
filename=''
date_initialized_filename=[]
LAST_RECV_TIME=time.time()
ORC_HEARTBEAT_WARN_INTERVAL=120
global file
DIRTY_CANNOT_CONNECT=False
DIRTY_NO_PING=False
CAPI_RESTARTED_BY_THIS_SCRIPT=False



log_path=''
if TESTING == True:
    log_path='/tmp/'
else:
    log_path='/home/smartwise/orcOTI_fileMDI/data/log/'


print "monitor_log_for_error_smartwise.py"

while 1:
    ##########################################
    SHOULD_ROTATE_FILE = False
    if ((int(time.strftime("%H%M")) > 919 and int(time.strftime("%H%M")) < 924) and not (any(time.strftime("%Y%m%d") in s for s in date_initialized_filename))): SHOULD_ROTATE_FILE = True
    if (TESTING == True                                                         and not (any(time.strftime("%Y%m%d") in s for s in date_initialized_filename))): SHOULD_ROTATE_FILE = True
    if (CAPI_RESTARTED_BY_THIS_SCRIPT == True                                                                                                                 ): SHOULD_ROTATE_FILE = True; CAPI_RESTARTED_BY_THIS_SCRIPT=False


    SHOULD_OPEN_ANOTH_FILE = False
    if (not filename or SHOULD_ROTATE_FILE):
        SHOULD_OPEN_ANOTH_FILE = True


    if (SHOULD_ROTATE_FILE == True):
        if not file.closed:
            file.close()
        filename=''
        date_initialized_filename.append(time.strftime("%Y%m%d"))
        print "File rotation performed on dates: " + str(date_initialized_filename)


    if (SHOULD_OPEN_ANOTH_FILE == True):
        for filelisted in sorted(os.listdir(log_path)):
            if fnmatch.fnmatch(filelisted, 'capi*.log'):
                filename=log_path+filelisted
    
        #Set the filename and open the file
        file = open(filename,'r')
        print "File to monitor: " + filename
    
        #Find the size of the file and move to the end
        st_results = os.stat(filename)
        st_size = st_results[6]
        file.seek(st_size)
    
        DIRTY_CANNOT_CONNECT=False
        DIRTY_NO_PING=False

    ##########################################
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(1)
        file.seek(where)
    else:
        HKSE_TRDG_HOUR = False
        if (((int(time.strftime("%H%M")) > 928 and int(time.strftime("%H%M")) < 1200) or (int(time.strftime("%H%M")) > 1300 and int(time.strftime("%H%M")) < 1600)) or (TESTING == True)):
            HKSE_TRDG_HOUR = True

        #############################
        #Error Detection
        #############################
        #Error on initial connection
        if (HKSE_TRDG_HOUR == True and (line.find('ERROR') >= 0) and (line.find('Cannot connect') >= 0)):
            DIRTY_CANNOT_CONNECT = True
            problem_line = line

        #Check missing heartbeat
        if ((line.find('ping') >= 0) and (line.find('message') >= 0)):
            LAST_RECV_TIME=time.time()
            DIRTY_NO_PING = False

        if (((HKSE_TRDG_HOUR == True) and (time.time() - LAST_RECV_TIME > ORC_HEARTBEAT_WARN_INTERVAL)) or (TESTING == True)):
            DIRTY_NO_PING = True
            problem_line="Not recv Orc heartbeat for more than " + str(ORC_HEARTBEAT_WARN_INTERVAL) + " sec!\n"

    if ((DIRTY_CANNOT_CONNECT == True) or (DIRTY_NO_PING == True)):
        sys.stdout.write(time.strftime("%Y%m%d %H%M%S") + ": " + problem_line)
        sys.stdout.write('\a')
        sys.stdout.flush()
        time.sleep(1)

    if (DIRTY_NO_PING == True):
        subprocess.call("/home/smartwise/usefulscripts/restart_smw_file_mdi_orc_oti.sh", shell=True)
        LAST_RECV_TIME=time.time()
        DIRTY_NO_PING = False
        CAPI_RESTARTED_BY_THIS_SCRIPT = True


    ##########################################
    #time.sleep(1)
