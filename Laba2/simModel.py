from create import Create
from model import Model
from process import Process

class Sim():
    def test1(self):
        creator = Create(5)

        p1 = Process(5)

        p1.maxqueue = 5

        creator.distribution = 'exp'
        p1.distribution = 'exp'

        creator.name = 'Creator'
        p1.name = 'Process 1'

        creator.nextElement = [p1]

        elements = [creator, p1]
        model = Model(elements)
        res = model.simulate(1000)

