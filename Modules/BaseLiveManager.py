from multiprocessing import Process, Event


class BaseLiveManager():
    def __init__(self):
        self.liveProcess = None
        self.multiprocessingProcess = None
        self.stopEvent = Event()
        pass


    def beginDetection(self):

        if self.multiprocessingProcess is None or not self.multiprocessingProcess.is_alive():
            self.multiprocessingProcess = Process(target=self.liveProcess)
            self.multiprocessingProcess.daemon = True
            self.multiprocessingProcess.start()


    def stopDetection(self):
        self.stopEvent.set()
        if self.liveProcess is not None:
            self.liveProcess.join()
        pass