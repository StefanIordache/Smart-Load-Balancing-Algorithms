import sys
import time

cmd = sys.stdin.read()
while cmd:
    x = cmd
    for i in range(0, 5):
        print "{'%i'=>'%s'}" % (i, x)
        sys.stdout.flush()
        cmd = sys.stdin.read()
