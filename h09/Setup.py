class Setup:
    def __init__(self):
        self._ProblemType = None
        self._FileName = None
        self._SelectAlgorithm = None
        self._delta = 0.01
        self._alpha = 0.01
        self._dx = 10**(-4)
        
    def setAll(self, ProblemType, FileName, SelectAlgorithm):
        self._ProblemType = ProblemType
        self._FileName = FileName
        self._SelectAlgorithm = SelectAlgorithm
