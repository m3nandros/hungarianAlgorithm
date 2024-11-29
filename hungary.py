import numpy as np
from scipy.optimize import linprog

def hungarian_alg(cost_matrix):
    n = cost_matrix.shape[0]

    # Преобразуем задачу в задачу линейного программирования
    # Целевая функция: минимизация суммы затрат
    c = cost_matrix.flatten()

    # Ограничения:
    # 1. Каждому исполнителю назначена одна задача
    A_eq = np.zeros((2*n, n*n))
    b_eq = np.ones(2*n)

    for i in range(n):
        for j in range(n):
            A_eq[i, i*n + j] = 1  # Строки: каждый исполнитель получает одну задачу
            A_eq[n + j, i*n + j] = 1  # Столбцы: каждая задача назначается одному исполнителю

    # Ограничения на бинарные переменные
    bounds = [(0, 1) for _ in range(n * n)]

    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

    if result.success:
        # Индексы назначений
        assignments = np.unravel_index(np.round(result.x).astype(int), (n, n))
        total_cost = result.fun
        assignments = list(zip(assignments[0], assignments[1]))
        return assignments, total_cost
    else:
        raise ValueError("Решение не найдено.")

# Пример использования
cost_matrix = np.array([
    [4, 2, 9],
    [4, 3, 5],
    [3, 1, 6]
])

assignments, total_cost = hungarian_alg(cost_matrix)
print("Назначения:", assignments)
print("Минимальная стоимость:", total_cost)
