class Snapshot(dict):

    def __init__(self, cluster, waiting, new, running, loaded, finished,
                 expired_while_waiting, expired_while_running):
        dict.__init__(self,
                      cluster=cluster,
                      waiting=waiting,
                      new=new,
                      running=running,
                      loaded=loaded,
                      finished=finished,
                      expired_while_running=expired_while_running,
                      expired_while_waiting=expired_while_waiting)
