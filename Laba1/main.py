from task1 import Task1
from task2 import Task2
from task3 import Task3

count = 10000
interval_count_for_analyze = 20
lambda_values = [0.1, 0.4, 7]

# Task 1
# for i in range(len(lambda_values)):
#     print(f'\tLambda = {lambda_values[i]}')
#     task1 = Task1(lambda_values[i], count)
#     task1.analyze(interval_count_for_analyze, i)
#     print()

# Task 2
alpha_values = [0.1, 4, 12]
sigma_values = [0.3, 6, 8]

for i in range(len(alpha_values)):
    print(f'\tAlpha = {alpha_values[i]}; Sigma = {sigma_values[i]}')
    task2 = Task2(alpha_values[i], sigma_values[i], count)
    task2.analyze(interval_count_for_analyze, i)
    print()

# Task 3
# a_values = [pow(5, 13), pow(5, 5), pow(5, 7)]
# c_values = [pow(2, 31), pow(5, 21), pow(5, 11)]

# for i in range(len(a_values)):
#     print(f'\tA = {a_values[i]}; C = {c_values[i]}')
#     task3 = Task3(a_values[i], c_values[i], count)
#     task3.analyze(interval_count_for_analyze, i)
#     print()
