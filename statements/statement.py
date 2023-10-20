from abc import ABC, abstractmethod

from securityLevel import SecurityLevel


class Statement(ABC):
    writeLevel: SecurityLevel = None
    terminationLevel: SecurityLevel = None
    
    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def toString(self):
        pass