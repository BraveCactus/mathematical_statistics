import numpy as np
from scipy import stats
from collections import Counter
import matplotlib.pyplot as plt

def exponential_distribution(sample_size, parametr = 1):
    #Генерирует выборку объема sample_size из экспоненциального распределения с параметром parametr
    exp_selection = np.round(np.random.exponential(parametr, sample_size), decimals=3)
    return exp_selection

def mode(data):
    #Возвращает наиболее часто встречающееся значение в выборке или -1, если такового нет
    counter = Counter(data) #коллекция значений с частотами появления (<)
    most_common = counter.most_common() #Отсортированный по частотам список кортежей (<значение>, <частота>)
    if(most_common[0][1] != most_common[1][1]):
        return most_common[0][0]
    else:
        return -1

def get_statistics(data):

    #Мода
    data_mode = mode(data)

    #Медиана
    data_median = np.median(data)

    #Размах
    data_range = round(max(data) - min(data), 3)

    #Коэффициент асимметрии
    data_coef_asymmetry = round(stats.skew(data), 3)

    return {'mode': data_mode,
            'median': data_median,
            'range': data_range,
            'coef_asymmetry': data_coef_asymmetry}

def get_dist_function(data):
    #Рисует график эмпирической функции распределения
    data_sorted = np.sort(data)

    y_values = np.arange(1, len(data_sorted) + 1) / len(data_sorted)
    
    fig, ax = plt.subplots(figsize = (12, 8))
    ax.step(data_sorted, y_values, where='post')   
    plt.show()

def get_histogram(data):
    data_sorted = np.sort(data)

    frequences = list()

    for i in range(len(data_sorted)):
        frequences.append(data_sorted/len(data_sorted))

    print(frequences)




exp_selection = exponential_distribution(25, 1)

# get_dist_function(exp_selection)

get_histogram(exp_selection)

# statistics = get_statistics(exp_selection)

# for key, value in statistics.items():
#     print(f'{key}: {value}')