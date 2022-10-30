import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from hi_squared_table import find_table_hi_squared


def print_extra_info(average, dispersion, observed_x_2, expected_x_2, result):
    print('\Середнє: ' + str(average))
    print('Дисперсія: ' + str(dispersion))
    print('X квадрат - реальне: ' + str(observed_x_2))
    print('X квадрат - очікуване: ' + str(expected_x_2))
    if(result):
        print('Знайдений закон розподілу відповідає спостережуваним значенням випадкової величини')
    else:
        print('Знайдений закон розподілу НЕ відповідає спостережуваним значенням випадкової величини')


def get_average_and_dispersion(array):
    s = 0
    average = array.sum() / array.size

    for i in array:
        s += pow(i - average, 2)

    dispersion = s / (array.size - 1)
    return average, dispersion


def getIntervals(array, intervalCount):
    interval_size = (array.max() - array.min()) / intervalCount

    items = list()
    limit_1 = array.min()

    for i in range(0, intervalCount):
        limit_2 = limit_1 + interval_size

        counter = 0
        for n in array:
            if limit_1 <= n < limit_2:
                counter += 1

        items.append([[limit_1, limit_2], counter])
        limit_1 = limit_2

    return items


def pull_intervals_from_list(items, intervalCount):
    intervals = list()
    
    for i in range(intervalCount):
        intervals.append([items[i][0][0], items[i][0][1]])
    
    return intervals


def to_data_frame(arr, intervalCount):
    copy_arr = [x[:] for x in arr]
    for i in range(intervalCount):
        name_interval = '[' + str(round(copy_arr[i][0][0], 2)) + ',' + str(round(copy_arr[i][0][1], 2)) + ')'
        copy_arr[i][0] = name_interval

    df = pd.DataFrame(copy_arr, columns=['Interval', 'Value count'])
    return df


def plot_histogram(items, intervalCount):
    df_e = to_data_frame(items, intervalCount)

    print(df_e.head(intervalCount))

    sns.barplot(data=df_e, x='Interval', y='Value count', color='b', edgecolor='black')
    plt.tight_layout()
    plt.xticks(rotation=30)
    plt.show()


def get_x_squared(functions_result, observed_list, intervalCount):
    x_2 = 0
    for i in range(intervalCount):
        expected = 10000 * functions_result[i]
        x_2 += pow(observed_list[i] - expected, 2) / expected
    return x_2


def x_2_tool(functions_result, observed_list, intervalCount):
    observed_x_squared = get_x_squared(functions_result, observed_list, intervalCount)
    expected_x_squared = find_table_hi_squared(intervalCount - 1)

    return observed_x_squared, expected_x_squared
