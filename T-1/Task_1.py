import numpy as np
from scipy import stats
from collections import Counter
import matplotlib.pyplot as plt
import math

def mode(data):
    #Возвращает наиболее часто встречающееся значение в выборке или -1, если такового нет
    counter = Counter(data) #коллекция значений с частотами появления
    most_common = counter.most_common() #Отсортированный по частотам список кортежей (<значение>, <частота>)
    if(most_common[0][1] != most_common[1][1]):
        return most_common[0][0]
    else:
        return "нет моды"

def exponential_distribution(sample_size, parametr = 1):
    #Генерирует выборку объема sample_size из экспоненциального распределения с параметром parametr
    exp_selection = np.round(np.random.exponential(parametr, sample_size), decimals=3)
    return exp_selection

def show_statistics(data):
    #Строит эмпирическую функцию распределения, гистограмму и ящик с усами (boxplot)
    data_sorted = np.sort(data)

    fig, axs = plt.subplots(3, 1, figsize = (6, 10))
    ax1, ax2, ax3 = axs

    ax1.hist(data_sorted, histtype='step', cumulative=True, bins=len(data_sorted))
    ax1.set_title('Эмпирическая функция распределения')   
    
    ax2.hist(data_sorted, color = 'blue', edgecolor = 'black', bins = round(1 + math.log2(len(data_sorted))))
    ax2.set_title('Гистограмма')    
    
    ax3.boxplot(data_sorted, vert = False)
    ax3.set_title('Ящик с усами (boxplot)')
        
    plt.show()

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
  
    plt.hist(data_sorted, histtype='step', cumulative=True, bins=len(data_sorted))
    plt.show()

def get_histogram(data):
    #Рисует гистаграмму, считаем кол-во отрезков разбиения по ф-ле: 1 + log2(n)
    data_sorted = np.sort(data)

    plt.hist(data_sorted, color = 'blue', edgecolor = 'black', bins = round(1 + math.log2(len(data_sorted))))
    plt.show() 

def box_plot(data):
    #Рисует ящик с усами (boxplot)
    data_sorted = np.sort(data)
    plt.boxplot(data_sorted, vert = False)
    plt.show()

def bootstrap_means(data, samples_number):
    #Возвращает массив из средних значений каждой выборки от исходной выборки
    n = len(data)
    bootstrap_means = np.empty(samples_number)

    for i in range(samples_number):
        sample = np.random.choice(data, size = n, replace = True)
        bootstrap_means[i] = np.mean(sample)

    return bootstrap_means

def show_bootstrap_distribution(data, samples_number):
    #Рисует гистограмму плотности распределения среднего арифметического элементов выборки
    bootstrap_means_array = bootstrap_means(data, samples_number)

    fig, ax = plt.subplots(figsize = (12, 8))
    ax.hist(bootstrap_means_array, color = 'blue', edgecolor = 'black', bins = round(1 + math.log2(len(bootstrap_means_array))))
    plt.show()

#Генерируем выборку из экспоненциального закона распределения, с параметром лямбда = 1
exp_selection = exponential_distribution(25, 1)


#Рисуем графики
show_statistics(exp_selection)

#Получаем характеристики, описывающие выборку (моду, медиану, размах и коэффициент асимметрии выборки)
statistics = get_statistics(exp_selection)

#Печаем данные
for key, value in statistics.items():
    print(f'{key}: {value}')

#Рисуем гистограмму плотности распределения среднего арифметического элементов выборки
show_bootstrap_distribution(exp_selection, 100)
