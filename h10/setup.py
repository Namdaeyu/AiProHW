class setup:
    def __init__(self):
        self._delta=0.01
        self._alpha=0.01
        self._dx=10**(-4)
        self._aType=None
    def setDelta(self,delta):
        self._delta=delta
        
    def setAlpha(self,alpha):
        self._alpha=alpha

    def setDx(self,dx):
        self._dx=dx
        
    def setAType(self,aType):
        self._aType=aType
            
    def getAType(self):
        return self._aType        
