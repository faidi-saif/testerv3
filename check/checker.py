
from abc import ABC, abstractmethod
from parser import Parser
from check.videoStat import VideoStat
from check.photoStat import PhotoStat

# ----------------------------------------------base class checker ------------------------------------------
class Checker (ABC):

    def __init__(self):
        self._result = False
        self.parser = Parser()
        super().__init__()



    @ property
    def result(self):
        return self._result


    @abstractmethod
    def check(self,*args ):
        pass