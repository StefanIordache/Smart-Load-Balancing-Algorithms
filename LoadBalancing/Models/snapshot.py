class Snapshot(dict):

    def __init__(self, timestamp=0, cluster=[], waiting=0, new=0, running=0, loaded=0, finished=0,
                 expired_while_running=0, expired_while_waiting=0, arrived=0):
        dict.__init__(self,
                      timestamp=timestamp,
                      cluster=cluster,
                      waiting=waiting,
                      new=new,
                      running=running,
                      loaded=loaded,
                      finished=finished,
                      expired_while_running=expired_while_running,
                      expired_while_waiting=expired_while_waiting,
                      arrived=arrived)
