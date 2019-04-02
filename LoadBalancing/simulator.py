import sys
import time


if __name__ == "__main__":
    logger = open ("log.txt", "w+")


    reader = sys.stdin.read()
    info_cluster = reader

    logger.write("am citit info_cluster")

    f = open ("cluster.json", "w+")
    f.write(info_cluster)
    f.close()

    logger.writelines("am realizat cluster.json")
    
    print "OK1\n"
    print '\0'
    sys.stdout.flush()

    logger.writelines("am afisat OK1")

    reader = sys.stdin.read()
    info_jobs = reader

    logger.writelines("am citit info_jobs")

    g = open ("jobs.json", "w+")
    g.write(info_jobs)
    g.close()

    logger.writelines("am realizat jobs.json")

    print "OK2"
    sys.stdout.flush()

    logger.writelines("am afisat OK2")

    """ while reader:
        x = reader
        for i in range(0, 5):
            print "{'%i'=>'%s'}" % (i, x)
            sys.stdout.flush()
            reader = sys.stdin.read() """
