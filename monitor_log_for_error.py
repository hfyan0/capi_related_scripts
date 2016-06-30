#!/usr/bin/python
import time, os, sys
from random import randint

problem_line=""

#Set the filename and open the file
filename=str(sys.argv[1])
file = open(filename,'r')

#Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

dirty=False

while 1:
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(0.5)
        file.seek(where)
    else:
        if line.find('ALERT') >= 0    : problem_line = line; dirty = True
        if line.find('WARNING') >= 0  : problem_line = line; dirty = True
        if line.find('ERROR') >= 0    : problem_line = line; dirty = True
        if line.find('CRITICAL') >= 0 : problem_line = line; dirty = True
        if line.find('EMERGENCY') >= 0: problem_line = line; dirty = True
        if line.find('Alert') >= 0    : problem_line = line; dirty = True
        if line.find('Warning') >= 0  : problem_line = line; dirty = True
        if line.find('Error') >= 0    : problem_line = line; dirty = True
        if line.find('Critical') >= 0 : problem_line = line; dirty = True
        if line.find('Emergency') >= 0: problem_line = line; dirty = True
    if dirty:
        os.system('clear')
        for j in range(0,5):
            irand=randint(5,10)
            for i in range(0,irand):
                sys.stdout.write(' ')
            sys.stdout.write('>>')
            irand=randint(5,10)
            for i in range(0,irand):
                sys.stdout.write(' ')
            sys.stdout.write('Dead')
            irand=randint(5,10)
            for i in range(0,irand):
                sys.stdout.write(' ')
            sys.stdout.write('!!!')
            irand=randint(5,10)
            for i in range(0,irand):
                sys.stdout.write(' ')
            sys.stdout.write('<<')
            irand=randint(5,10)
            for i in range(0,irand):
                sys.stdout.write(' ')
            sys.stdout.write('\n')

        print problem_line
        sys.stdout.write('\a')
        sys.stdout.flush()
        time.sleep(0.5)
