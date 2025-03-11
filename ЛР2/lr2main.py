import matplotlib.pyplot as plt
import time
from bintreenerec import gen_bin_nec_tree
from bintreerec import gen_bin_rec_tree

def setup_data(n: int) -> list:
    """
    Создает список данных для тестирования.
    Params:
    n (int): Количество элементов в списке данных.
    Return:
    list: Список кортежей, содержащих значения корня и высоты дерева.
    """
    data = []
    for root, height in zip([0,1,2,3,4,5], [0,2,4,6,8,10]): # zip - объединяет несколько итерируемых объектов в один итерируемы объект, который содержит кортежи
        data.append((root, height))
    return data[:n]


def calculate_time(data, func) -> float:
    """
    Измеряет время выполнения функции на заданных данных.
    Params:
    data (list): Список данных, передаваемых в функцию.
    func(): Функция, время выполнения которой нужно измерить.
    Return:
    float: Время выполнения функции в секундах.
    """
    start_time = time.time()
    for root, height in data:
        func(root, height)
    end_time = time.time()
    return end_time - start_time

def main():
    """
    Основная функция программы. Выполняет измерение времени работы рекурсивной и нерекурсивной функций
    генерации бинарных деревьев и строит график результатов.
    """
    num_runs = 10
    step = 10
    max_list_length = step ** 2
    l = range(step, max_list_length + 1, step)

    results_recursive = []
    results_iterative = []

    for n in l:
        total_time_rec = 0
        total_time_iter = 0

        for i in range(num_runs):
            data = setup_data(n)
            total_time_rec += calculate_time(data, gen_bin_rec_tree)
            total_time_iter += calculate_time(data, gen_bin_nec_tree)

        average_rec = total_time_rec / num_runs
        average_iter = total_time_iter / num_runs
        results_recursive.append(average_rec)
        results_iterative.append(average_iter)
        print(f"Размер дерева {n}: Рекурсия - {average_rec:.6f} секунд, Итерация - {average_iter:.6f} секунд")

    plt.plot(l, results_recursive, label='Рекурсия')
    plt.plot(l, results_iterative, label='Нерекурсия')
    plt.xlabel('Размер дерева')
    plt.ylabel('Время выполнения (с)')
    plt.title('Сравнение времени выполнения')
    plt.legend()
    plt.savefig('lr2results.png') # Сохраняем график в файл
    plt.show()

if __name__ == "__main__":
    main()
