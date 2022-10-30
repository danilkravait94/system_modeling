import pandas as pd

from create import Create
from model import Model
from process import Process


class Sim():
    def task1(self):
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


    def task3(self):
        creator = Create(5)

        p1 = Process(5)
        p2 = Process(5)
        p3 = Process(5)

        creator.nextElement = [p1]
        p1.nextElement = [p2, p3]
        
        p1.probability = ([0.5, 0.5])

        p1.maxqueue = 5
        p2.maxqueue = 5
        p3.maxqueue = 5
        
        creator.distribution = 'exp'
        p1.distribution = 'exp'
        p2.distribution = 'exp'
        p3.distribution = 'exp'

        creator.name = 'Creator'
        p1.name = 'Process 1'
        p2.name = 'Process 2'
        p3.name = 'Process 3'
        
        elements = [creator, p1, p2, p3]
        model = Model(elements)
        res = model.simulate(1000)

    def task4(self):
        creator_delays = [12, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 6]
        
        process_delays = [
            [6, 12, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 6, 6],
            [6, 6, 12, 6, 6, 6, 6, 6, 6, 6, 6, 1, 6, 6, 6],
            [6, 6, 6, 12, 6, 6, 6, 6, 6, 6, 1, 6, 6, 6, 6],
        ]

        maxqueue_values = [
            [4, 4, 4, 4, 12, 4, 4, 4, 4, 1, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 12, 4, 4, 1, 4, 4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4, 4, 12, 1, 4, 4, 4, 4, 4, 4, 4],
        ]

        distribution = 'exp'

        result_array = []

        for i in range(len(creator_delays)):
            creator = Create(creator_delays[i])

            p1 = Process(process_delays[0][i])
            p2 = Process(process_delays[1][i])
            p3 = Process(process_delays[2][i])

            p1.maxqueue = maxqueue_values[0][i]
            p2.maxqueue = maxqueue_values[1][i]
            p3.maxqueue = maxqueue_values[2][i]

            creator.distribution = distribution
            p1.distribution = distribution
            p2.distribution = distribution
            p3.distribution = distribution

            creator.name = 'Creator'
            p1.name = 'Process 1'
            p2.name = 'Process 2'
            p3.name = 'Process 3'

            creator.nextElement = [p1]
            p1.nextElement = [p2]
            p2.nextElement = [p3]

            elements = [creator, p1, p2, p3]
            model = Model(elements)
            res = model.simulate(1000)

            i_result = [
                creator_delays[i],
                
                process_delays[0][i],
                process_delays[1][i],
                process_delays[2][i],

                maxqueue_values[0][i],
                maxqueue_values[1][i],
                maxqueue_values[2][i],

                p1.quantity,
                p1.failure,

                p2.quantity,
                p2.failure,
                
                p3.quantity,
                p3.failure,
            ]

            result_array.append(i_result)

        columns = [
            'Creator Delay',

            'Process Delay 1',
            'Process Delay 2',
            'Process Delay 3',

            'Max Queue 1',
            'Max Queue 2',
            'Max Queue 3',

            'Process 1 - success',
            'Process 1 - fail',

            'Process 2 - success',
            'Process 2 - fail',

            'Process 3 - success',
            'Process 3 - fail',
            
            ]

        df = pd.DataFrame(result_array, columns=columns)
        pd.set_option('display.max_columns', None)
        print(f"Distribution: {distribution}")

        print(df)
        

    def task5_6(self):
        creator = Create(5)

        p1 = Process(5, 2)

        p1.maxqueue = 5

        creator.distribution = 'exp'
        p1.distribution = 'exp'

        creator.name = 'Creator'
        p1.name = 'Process 1'

        creator.nextElement = [p1]

        elements = [creator, p1]
        model = Model(elements)
        res = model.simulate(1000)

