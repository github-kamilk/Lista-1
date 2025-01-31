import random
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import csv


class BinHeap:
    def __init__(self):
        self.heap_list = [0]
        self.current_size = 0

    def percUp(self, index):
        while index // 2 > 0:
            if self.heap_list[index] < self.heap_list[index // 2]:
                tmp = self.heap_list[index // 2]
                self.heap_list[index // 2] = self.heap_list[index]
                self.heap_list[index] = tmp
            index = index // 2

    def insert(self, k):
        self.heap_list.append(k)
        self.current_size = self.current_size + 1
        self.percUp(self.current_size)

    def findMin(self):
        return self.heap_list[1]

    def percDown(self, index):
        while (index * 2) <= self.current_size:
            mc = self.minChild(index)
            if self.heap_list[index] > self.heap_list[mc]:
                tmp = self.heap_list[index]
                self.heap_list[index] = self.heap_list[mc]
                self.heap_list[mc] = tmp
            index = mc

    def minChild(self, index):
        if index * 2 + 1 > self.current_size:
            return index * 2
        else:
            if self.heap_list[index * 2] < self.heap_list[index * 2 + 1]:
                return index * 2
            else:
                return index * 2 + 1

    def delMin(self):
        retval = self.heap_list[1]
        self.heap_list[1] = self.heap_list[self.current_size]
        self.current_size = self.current_size - 1
        self.heap_list.pop()
        self.percDown(1)
        return retval

    def buildHeap(self, alist):
        index = len(alist) // 2
        self.current_size = len(alist)
        self.heap_list = [0] + alist[:]
        while (index > 0):
            self.percDown(index)
            index = index - 1

    def size(self):
        return self.current_size

    def isEmpty(self):
        return self.current_size == 0

    def __str__(self):
        txt = "{}".format(self.heap_list[1:])
        return txt


def sortHeap(data_list):
    sorted_heap = []
    heap = BinHeap()
    heap.buildHeap(data_list)
    n = len(data_list)
    for i in range(n):
        temp = heap.delMin()
        sorted_heap.append(temp)
    return sorted_heap


def fit_fun(n, a):
    return a * n * np.log(n)


def time_checker(n):
    a = [random.randint(-100, 100) for _ in range(n)]
    start = time.time()
    sortHeap(a)
    stop = time.time()
    return stop - start


def plot(x, y):
    plt.plot(x, y, 'ro', label="Dane")
    plt.xlabel("Liczba elementów")
    plt.ylabel("Czas wykonania [s]")
    plt.legend(loc='upper left')
    plt.title("Wykres czasu w zależności od liczby elementów")
    plt.show()


def hypothesis_plot(x, y, func, popt):
    x2 = np.arange(1, x[-1])

    plt.plot(x, y, 'ro', label="Dane")
    plt.plot(x2, func(x2, *popt), label="Hipoteza", linewidth=3.5)
    plt.xlabel("Liczba elementów")
    plt.ylabel("Czas wykonania [s]")
    plt.legend(loc='upper left')
    plt.title("Wykres czasu w zależności od liczby elementów")
    plt.show()


if __name__ == "__main__":
    n = [1000 * i for i in range(2, 100)]

    execution_times = []

    # for i in n:
    #     execution_times.append(time_checker(i))
    # with open('execution_times.csv', 'w', newline='') as myfile:
    #     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    #     wr.writerow(execution_times)

    with open('execution_times.csv', newline='') as f:
        reader = csv.reader(f)
        execution_times = [float(i) for i in list(reader)[0]]

    plot(n, execution_times)
    popt, pcov = curve_fit(fit_fun, n, execution_times)
    hypothesis_plot(n, execution_times, fit_fun, popt)
