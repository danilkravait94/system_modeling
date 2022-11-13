from create import Create
from model import Model
from process import Process
import utility

def create_laba2_model(n):
    creator = Create(delayMean=utility.get_random_delaymean(), name='Creator 1', distribution='exp')

    elements = [creator]
    for i in range(n):
        process = Process(delayMean=utility.get_random_delaymean(), name=f'Process {i + 1}', distribution='exp')
        elements[i].nextElement = [process]
        elements.append(process)

    model = Model(elements)
    return model

def create_thread_model(n):
    creator = Create(delayMean=utility.get_random_delaymean(), name='Creator 2', distribution='exp')

    elements = [creator]
    i = 0
    while i < n:
        process1 = Process(delayMean=utility.get_random_delaymean(), name=f'Process {i + 1}', distribution='exp')
        elements[i].nextElement = [process1]

        process2 = Process(delayMean=utility.get_random_delaymean(), name=f'Process {i + 2}', distribution='exp')
        process3 = Process(delayMean=utility.get_random_delaymean(), name=f'Process {i + 3}', distribution='exp')
        process1.nextElement = [process2, process3]
        process1.probability = [0.2, 0.8]
        
        process4 = Process(delayMean=utility.get_random_delaymean(), name=f'Process {i + 4}', distribution='exp')
        process2.nextElement = [process4]
        process3.nextElement = [process4]

        elements.append(process1)
        elements.append(process2)
        elements.append(process3)
        elements.append(process4)
        
        i += 4

    model = Model(elements)
    return model

