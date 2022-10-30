import utility


class Element:
    staticNextId = 0

    def __init__(self, delay=None, distribution=None):
        self.tnext = 0
        self.delayMean = delay
        self.distribution = distribution
        self.tcurr = self.tnext
        self.state = 0
        self.nextElement = None
        
        self.id = Element.staticNextId
        Element.staticNextId += 1

        self.name = 'element' + str(self.id)
        self.delayDev = None
        
        self.quantity = 0
        self.probability = [1]


    def getDelay(self):
        if 'exp' == self.distribution:
            return utility.exponential(self.delayMean)
        elif 'norm' == self.distribution:
            return utility.normal(self.delayMean, self.delayDev)
        elif 'uniform' == self.distribution:
            return utility.uniform(self.delayMean, self.delayDev)
        else:
            return self.delayMean
    
    def get_state(self):
        return self.state

    def set_state(self, new_state):
        self.state = new_state
    

    def set_tnext(self, value):
        self.tnext = value

    def get_tnext(self):
        return self.tnext
    
    
    def set_tcurr(self, value):
        self.tcurr = value

    def get_tcurr(self):
        return self.tcurr

    
    def inAct(self):
        pass

    def outAct(self):
        self.quantity += 1

    def printResult(self):
        print(f'{self.name} quantity = {str(self.quantity)} state = {self.state}')

    def printInfo(self):
        print(f'{self.name} state = {self.state} quantity = {self.quantity} t_next = {self.tnext}')

    def doStatistics(self, delta):
        pass
