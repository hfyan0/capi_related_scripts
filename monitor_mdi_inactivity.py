#!/usr/bin/python
import datetime
import time
import socket
import thread
from threading import Thread
from inspect import currentframe, getframeinfo
import sys
import time, os, sys

LAST_RECV_TIME = time.time()

def ThreadFunc1(i):
    global LAST_RECV_TIME

    while 1:
        print time.strftime("%Y%m%d %H%M%S") + ": Last market data recv " + str(int(time.time() - LAST_RECV_TIME)) + " sec ago."
        HKSE_TRDG_HOUR = False
        if ((int(time.strftime("%H%M")) > 930 and int(time.strftime("%H%M")) < 1200) or (int(time.strftime("%H%M")) > 1300 and int(time.strftime("%H%M")) < 1600)):
            HKSE_TRDG_HOUR = True

        if ((HKSE_TRDG_HOUR == True) and (time.time() - LAST_RECV_TIME > 10)):
            #os.system('clear')

            print time.strftime("%Y%m%d %H%M%S") + ': Stale market data in MDI: ' + str(sys.argv[1]) + ':' + str(sys.argv[2])
            sys.stdout.write('\a')
            sys.stdout.flush()

        time.sleep(1)




def ThreadFunc2(i):
    global LAST_RECV_TIME

    while 1:
        try:
            #############################################################
            # Open MDI socket
            #############################################################
            mdiSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mdiSocket.connect((str(sys.argv[1]), int(sys.argv[2])))
            print "Socket connected. (for getting data)"

            while 1:
                msg = mdiSocket.recv(4096)
                if len(msg) > 0:
                    if not (msg.find('ping') >= 0):
                        LAST_RECV_TIME = time.time()
                else:
                    ## Just try to send sth so that any TCP disconnection is known
                    mdiSocket.send("ping\n")
        except socket.error:
            print "Socket disconnected."
            mdiSocket.close()
        time.sleep(3)

def main():
  print "Start monitoring " + str(sys.argv[1]) + ":" + str(sys.argv[2])

  t1 = Thread(target=ThreadFunc1, args=(1,))
  t1.daemon = True
  time.sleep(0.5)
  t1.start()

  t2 = Thread(target=ThreadFunc2, args=(1,))
  t2.daemon = True
  time.sleep(0.5)
  t2.start()

  print "All threads started."
  #t1.join()
  while True:
      time.sleep(1)

if __name__ == '__main__':
  main()
