#!/usr/bin/python
import datetime
import time
import socket
import thread
from threading import Thread
from inspect import currentframe, getframeinfo
import sys
import time, os, sys

STRING_TO_MONITOR = "Max loss per day limit reached"
STRING_IS_FOUND = False
STRING_TO_SEND = ['20140122_113136_123213,signalfeed,DUMMY_MKT,DUMMY_SYM,OID_110522_3,999,9,open,1,insert,cancel_all_order,today\n', '20140122_113136_123213,signalfeed,DUMMY_MKT,DUMMY_SYM,OID_110531_6,999,9,open,1,insert,close_all_order,today\n']
STRING_IS_SENT = False

global otiSocket

def ThreadFunc1(i):
    global STRING_IS_FOUND
    global STRING_IS_SENT
    global otiSocket

    while 1:
        print time.strftime("%Y%m%d %H%M%S") + ": Checking for string: [" + STRING_TO_MONITOR + "]. String found == " + str(STRING_IS_FOUND)
        TRDG_HOUR = False
        if ((int(time.strftime("%H%M")) > 915 and int(time.strftime("%H%M")) < 1130) or (int(time.strftime("%H%M")) > 1300 and int(time.strftime("%H%M")) < 1510)):
            TRDG_HOUR = True

        if ((TRDG_HOUR == True) and (STRING_IS_FOUND == True) and (STRING_IS_SENT == False)):
            #os.system('clear')

            print time.strftime("%Y%m%d %H%M%S") + ': String is found at [' + str(sys.argv[1]) + ':' + str(sys.argv[2]) + ']'
            for i in STRING_TO_SEND:
                print 'Now send to [' + str(sys.argv[1]) + ':' + str(sys.argv[2]) + ']: ' + i
                otiSocket.send(i)
                time.sleep(1)

            STRING_IS_SENT = True

        time.sleep(1)


def ThreadFunc2(i):
    global STRING_IS_FOUND
    global otiSocket

    while 1:
        try:
            #############################################################
            # Open OTI socket
            #############################################################
            otiSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            otiSocket.connect((str(sys.argv[1]), int(sys.argv[2])))
            print "Socket connected."

            while 1:
                msg = otiSocket.recv(4096)
                if len(msg) > 0:
                    if (msg.find(STRING_TO_MONITOR) >= 0):
                        STRING_IS_FOUND = True
                else:
                    ## Just try to send sth so that any TCP disconnection is known
                    otiSocket.send("ping\n")
        except socket.error:
            print "Socket disconnected."
            otiSocket.close()
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
