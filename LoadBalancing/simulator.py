import sys
import time


if __name__ == "__main__":
    logger = open ("log.txt", "w+")
    log1 = open ("log1.txt", "w+")
    log2 = open ("log2.txt", "w+")

    info_cluster = sys.stdin.readline()
    logger.write(str(info_cluster))

    logger.write("am citit info_cluster\n")
    
    print "OK1"
    sys.stdout.flush()

    logger.write("am afisat OK1\n")

    info_jobs = sys.stdin.readline()
    logger.write(str(info_jobs))

    logger.write("am citit info_jobs\n")

    print "OK2"
    sys.stdout.flush()

    logger.write("am afisat OK2\n")
