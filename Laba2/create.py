from element import Element


class Create(Element):
    def __init__(self, delay):
        super().__init__(delay)

    def outAct(self):
        # збільшуємо лічильник кількості
        super().outAct()
        # коли пристрій буде вільним
        self.tnext[0] = self.tcurr + self.getDelay()
        self.nextElement[0].inAct()
