from multiprocessing import Process, Event


class BaseLiveManager():
    def __init__(self):
        """
        Initializes an empty base manager.
        """
        self.liveProcess = None
        self.multiprocessingProcess = None
        self.stopEvent = Event()


    def beginDetection(self):
        """
        Initializes a new multiprocessing process to run the main function of the manager
        :return:
        """
        if self.multiprocessingProcess is None or not self.multiprocessingProcess.is_alive():
            self.multiprocessingProcess = Process(target=self.liveProcess)
            self.multiprocessingProcess.daemon = True
            self.multiprocessingProcess.start()


    def stopDetection(self):
        """
        Completely unused function, but it stops the detection process
        Just ctrl+c the process
        :return:
        """
        self.stopEvent.set()
        if self.liveProcess is not None:
            self.liveProcess.join()
        pass