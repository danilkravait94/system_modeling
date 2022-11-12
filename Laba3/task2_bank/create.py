from global_e.element import Element


class BankCreate(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def outAct(self):
        # виконуємо збільшення лічильника кількості
        super().outAct()
        # встановлюємо коли пристрій буде вільним
        self.tnext[0] = self.tcurr + super().getDelay()

        first = self.nextElement[0]
        second = self.nextElement[1]

        isFirst = (first.queue == second.queue) or (first.queue == 0 and second.queue == 0) or (first.queue < second.queue)
        if isFirst:
            first.inAct()
        else:
            second.inAct()
