from global_e.element import Element


class Create(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def outAct(self):
        # збільшуємо лічильник кількості
        super().outAct()
        # коли пристрій буде вільним
        self.tnext[0] = self.tcurr + super().getDelay()

        # пріоритетність чи ймовірність
        nextElement = self.get_nextElement()
        nextElement.inAct()
