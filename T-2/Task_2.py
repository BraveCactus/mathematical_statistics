import numpy as np
from scipy import stats
from collections import Counter
import matplotlib.pyplot as plt
import math
import statistics
from scipy.stats import norm


#Task a)
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

#Task b)
def show_statistics(data):
    #Строит эмпирическую функцию распределения, гистограмму и ящик с усами (boxplot)
    data_sorted = np.sort(data)

    fig, axs = plt.subplots(3, 1, figsize = (6, 10))
    ax1, ax2, ax3 = axs  

    #Эмпирическая функция распределения
    counts, bins, patches = ax1.hist(data_sorted, histtype='step', cumulative=True, bins=len(data_sorted))    

    new_counts = counts / len(data_sorted)

    ax1.clear()
    ax1.set_title('Эмпирическая функция распределения')
    ax1.bar(bins[:-1], new_counts, width=np.diff(bins))     

    #Гистограмма
    # counts, bins, patches = ax2.hist(data_sorted, color='blue', edgecolor='black', bins=round(1 + math.log2(len(data_sorted))))    
    
    # new_counts = counts / len(data_sorted)

    # ax2.clear()
    
    # ax2.bar(bins[:-1], new_counts, width=np.diff(bins), color='blue', edgecolor='black')

    ax2.hist(data_sorted, color='blue', edgecolor='black', bins=round(1 + math.log2(len(data_sorted)))) 
    ax2.set_title('Гистограмма')

    #Ящик с усами
    ax3.boxplot(data_sorted, vert = False)
    ax3.set_title('Ящик с усами (boxplot)')

    plt.tight_layout() #Для удовлетворения чувства прекрасного
        
    plt.show()

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

#Task c)
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
    #Накладывает плотность распределения полученное с помощью ЦПТ (нормальное распределение)
    bootstrap_means_array = bootstrap_means(data, samples_number)
    sorted_arr = np.sort(bootstrap_means_array)

    # mean = statistics.mean(sorted_arr)
    # standard_deviation = statistics.stdev(sorted_arr)

    # x_array = np.linspace(sorted_arr[0], sorted_arr[-1], 50)
    # y_array = norm.pdf(x_array, mean, standard_deviation)    

    fig, ax = plt.subplots(figsize = (12, 8))
    ax.hist(bootstrap_means_array, color = 'blue', edgecolor = 'black', bins = round(1 + math.log2(len(bootstrap_means_array))))

    #Перестраиваем гистограмму так, чтобы по оси y были вероятности
    y_value, bins, patches = plt.hist(bootstrap_means_array, bins=30, alpha=0.5, color='blue')
    y_new_value = y_value / samples_number #делим на количество подвыборок, чтобы посчитать вероятность
    plt.clf()
    plt.bar(bins[:-1], y_new_value, width=np.diff(bins), alpha=0.5, color='blue', align='edge', edgecolor = 'black')
    plt.title('Плотность распределения среднего арифметического элементов выборки')
    plt.xlabel('Значения')
    plt.ylabel('Вероятность')
    
    # ax.plot(x_array, y_array, color = 'red', linewidth=2) #НЕ ОТОБРАЖАЕТСЯ!!! ХЗ ПОЧЕМУ
    plt.show()

#Task d)
def bootstrap_coef_asymmetry(data, samples_number):
    #Возвращает массив из коэффициентов асимметрии каждой выборки от исходной выборки
    n = len(data)
    bootstrap_coef_asymmetry = np.empty(samples_number)

    for i in range(samples_number):
        sample = np.random.choice(data, size = n, replace = True)
        bootstrap_coef_asymmetry[i] = round(stats.skew(sample), 3)

    return bootstrap_coef_asymmetry

def show_coef_asymmetry_distribution(data, samples_number):
    #Рисует гистограмму плотности распределения коэффициентов асимметрии элементов выборки
    bootstrap_coef_asymmetry_array = bootstrap_coef_asymmetry(data, samples_number)
    fig, ax = plt.subplots(figsize = (12, 8))
    ax.hist(bootstrap_coef_asymmetry_array, color = 'blue', edgecolor = 'black', bins = round(1 + math.log2(len(bootstrap_coef_asymmetry_array))))

    #Перестраиваем гистограмму так, чтобы по оси y были вероятности
    y_value, bins, patches = plt.hist(bootstrap_coef_asymmetry_array, bins=30, alpha=0.5, color='blue')
    y_new_value = y_value / samples_number #делим на количество подвыборок, чтобы посчитать вероятность
    plt.clf()
    plt.bar(bins[:-1], y_new_value, width=np.diff(bins), alpha=0.5, color='blue', align='edge', edgecolor = 'black')
    plt.title('Плотность распределения коэффициента асимметрии элементов выборки')
    plt.xlabel('Значения')
    plt.ylabel('Вероятность')

    plt.show()

def probability_coef_assym_less_then_1(data, samples_number):
    bootstrap_coef_asymmetry_array = bootstrap_coef_asymmetry(data, samples_number)
    count_less_then_1 = 0

    for i in range(len(bootstrap_coef_asymmetry_array)):
        if(bootstrap_coef_asymmetry_array[i] < 1):
            count_less_then_1 += 1
    
    probability = round(count_less_then_1 / samples_number, 3)

    return probability

#Task e)
def bootstrap_median(data, samples_number):
    #Возвращает массив из медиан каждой выборки от исходной выборки
    n = len(data)
    bootstrap_means = np.empty(samples_number)

    for i in range(samples_number):
        sample = np.random.choice(data, size = n, replace = True)
        bootstrap_means[i] = np.median(sample)

    return bootstrap_means

def show_median_distribution(data, samples_number): 
    #Рисует гистограмму плотности распределения медиан элементов выборки
    bootstrap_median_array = bootstrap_median(data, samples_number)
    fig, ax = plt.subplots(figsize = (12, 8))
    ax.hist(bootstrap_median_array, color = 'blue', edgecolor = 'black', bins = round(1 + math.log2(len(bootstrap_median_array))))

    #Перестраиваем гистограмму так, чтобы по оси y были вероятности
    y_value, bins, patches = plt.hist(bootstrap_median_array, bins=round(1 + math.log2(len(bootstrap_median_array))), alpha=0.5, color='blue', edgecolor = 'black')
    y_new_value = y_value / samples_number #делим на количество подвыборок, чтобы посчитать вероятность
    plt.clf()
    plt.bar(bins[:-1], y_new_value, width=np.diff(bins), alpha=0.5, color='blue', align='edge', edgecolor = 'black')
    plt.title('Плотность распределения медиан элементов выборки')
    plt.xlabel('Значения')
    plt.ylabel('Вероятность')

    plt.show()

#Генерируем выборку объемом 25 из экспоненциального закона распределения, с параметром лямбда = 1
exp_selection = exponential_distribution(25, 1)

#Получаем характеристики, описывающие выборку (моду, медиану, размах и коэффициент асимметрии выборки)
statistics = get_statistics(exp_selection)

# #Печаем данные
for key, value in statistics.items():
    print(f'{key}: {value}')




#Рисуем графики
show_statistics(exp_selection)

#Рисуем гистограмму плотности распределения среднего арифметического элементов выборки
show_bootstrap_distribution(exp_selection, 1000)

print("Вероятность того, что коэф асимметрии меньше 1: ",probability_coef_assym_less_then_1(exp_selection, 1000))

#Рисуем гистограмму п\лотности распределения коэффициента асимметрии элементов выборки
show_coef_asymmetry_distribution(exp_selection, 1000)

#Рисуем гистограмму плотности распределения медиан элементов выборки
show_median_distribution(exp_selection, 1000)

