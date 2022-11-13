import time
from process import Process
from element import Element
from model import Model
import matplotlib.pyplot as plt

k = 2
modeling_time = 1000
test_count = 3
# actions_count = [15]
# actions_count = [100, 200]
# actions_count = [100, 200, 300, 400, 500]
actions_count = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

def analyze_theoretical(model: Model, modeling_time: int = modeling_time):
    intencity = 0
    model.list: list[Element]

    # Интенсивность = сумма всех интенсивностей каждой СМО.
    # Интенсивность СМО = интенсивность при полной загруженности СМО * загруженность СМО в действительности
    for e in model.list:
            if isinstance(e, Process):
                intencity += 1 / model.tcurr * model.get_meanload(e)

    return intencity * k * modeling_time

def analyze(create_model):
    analytic_time_values = []
    theoretical_values = []
    for i in actions_count:
        analytic_time_sum = 0
        theoretical_sum = 0

        for j in range(test_count):
            model = create_model(i)

            print(f'Working on {i}, time = {j}')
            start_time = time.perf_counter()
            model.simulate(modeling_time)
            end_time = time.perf_counter()
            theoretical_sum += analyze_theoretical(model, modeling_time)
            analytic_time_sum += end_time - start_time
            
        analytic_time_values.append(analytic_time_sum / test_count)
        theoretical_values.append(theoretical_sum / test_count)

    plt.title("Analytic estimation")
    plt.xlabel("Model complexity")
    plt.ylabel("Time")
    plt.plot(actions_count, analytic_time_values, color="blue")
    plt.show()

    plt.title("Theoretical estimation")
    plt.xlabel("Model complexity")
    plt.ylabel("Operations")
    plt.plot(actions_count, theoretical_values, color="blue")
    plt.show()