import sys
import time


if __name__ == "__main__":
    reader = sys.stdin.read()
    info_cluster = reader
    
    print "OK"
    sys.stdout.flush()

    reader = sys.stdin.read()
    info_jobs = reader

    print "OK"
    sys.stdout.flush()

    """ while reader:
        x = reader
        for i in range(0, 5):
            print "{'%i'=>'%s'}" % (i, x)
            sys.stdout.flush()
            reader = sys.stdin.read() """
