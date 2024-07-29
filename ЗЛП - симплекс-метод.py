import math
import numpy as np
n =int(input("Введите количество строк, которые будут находится в матрице A  "))
m =int(input("Введите количество столбцов, которые будут находится в матрице А "))
A =list()
B=[0]* n
Z =[0]* m
for start in range(n):
    a_start =list()
    for sstart in range(m):
        g =float(input("Введите значения элементов, находящихся в матрице А "+str(start +1)+" "+str(sstart +1)+" "))
        a_start.append(g)
    A.append(a_start)
for start in range(n):
    g =int(input("Введите значения ограничений B "+str(start +1)+" "))
    B[start]= g
for start in range(m):
    g =int(input("Введите коэффициенты критериальной функции "+str(start+1)+" "))
    Z[start]= g

def TAB(Z, A, B): #Создаем симплекс-таблицу с нашими ограничениями и коэффициентами критериальной функции.
    xB = [stroka + [x] for stroka, x in zip(A, B)]
    a = Z + [0]
    return xB + [a]

def Proverka_on_optimal(tab): #Данная функция проверяет оптимальная ли наша задача, тоесть проверяется есть ли отрицательные элементы в последней строке.
    a = tab[-1]
    return any(x > 0 for x in a[:-1]) # при наличии элемента больше 0, будет возвращаться True

def finding_element(tab):  #Находим разрешающий элемент (в нашей нижней строке ищем наименьший элемент(соответствует разрешающему столбцу), далее по минимальной theta находим разрешающую строку).
    a = tab[-1]
    column = next(i for i, x in enumerate(a[:-1]) if x > 0)
    theta = []  #Поиск theta(в начале создадим ее как пустой список, затем найдем ее)
    for stroka in tab[:-1]:
        stolbets = stroka[column]
        theta.append(math.inf if stolbets <= 0 else stroka[-1] / stolbets)
    min_theta = theta.index(min(theta))
    return min_theta, column

def gauss_jordan(tab, element): # Используем метод Гаусса-Жордана (новый элемент=старый элемент - (элемент разрешающей строки * элемент разрешающего столбца)/ разрешающий элемент)
    new_tab = [[] for stroka in tab] # создадим пустой двумерный массив
    i, j = element
    res_element = tab[i][j]
    new_tab[i] = np.array(tab[i]) / res_element
    for stroka_i, stroka in enumerate(tab):
        if stroka_i != i:
            ij_element = np.array(new_tab[i]) * tab[stroka_i][j]
            new_tab[stroka_i] = np.array(tab[stroka_i]) - ij_element
    return new_tab

def proverka(column):
    return sum(column) == 1 and len([Z for Z in column if Z == 0]) == len(column) - 1 #Данная функция проверяет то что в данном столбце находится базисная переменная

def get_result(tab): #Находим вектор решения из  матрицы
    column = np.array(tab).T #транспонируем массив
    results = [] # создадим отдельный список для хранения полученного решения
    for vector in column :
        result = 0
        if proverka(vector):
            our_index = vector.tolist().index(1)
            result = column[-1][our_index]
        results.append(result)
    return results

def If_simplex_is_optimal(Z, A, B): #Если решение оптимальное и конечное то выводим его
    tab=TAB(Z, A, B)
    while Proverka_on_optimal(tab):
        element = finding_element(tab)
        tab = gauss_jordan(tab, element)
    return tab
tab=list(np.around(np.array(If_simplex_is_optimal(Z, A, B)), 2))
print("Матрица, получаемая в конце в ходе проведенных итераций: \n", "\n".join(" \t".join(str(stolbets) for stolbets in r)for r in tab))
print("Решение:",get_result(tab))




