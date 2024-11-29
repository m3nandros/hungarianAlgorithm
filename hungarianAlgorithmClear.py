import numpy as np

def hungarian_algorithm(cost_matrix):
    n = cost_matrix.shape[0]
    cost_matrix = np.copy(cost_matrix)
    
    # Шаг 1: Вычитаем минимальное значение из каждой строки
    for i in range(n):
        cost_matrix[i, :] -= np.min(cost_matrix[i, :])
    
    # Шаг 2: Вычитаем минимальное значение из каждого столбца
    for j in range(n):
        cost_matrix[:, j] -= np.min(cost_matrix[:, j])
    
    # Шаг 3: Покрытие всех нулей минимальным количеством линий
    def cover_zeros(matrix):
        n = matrix.shape[0]
        row_cover = np.zeros(n, dtype=bool)
        col_cover = np.zeros(n, dtype=bool)
        
        # Инициализация маркировок
        marked = np.zeros((n, n), dtype=bool)
        
        while True:
            # Находим незакрытые нули
            for i in range(n):
                for j in range(n):
                    if matrix[i, j] == 0 and not row_cover[i] and not col_cover[j]:
                        marked[i, j] = True
                        row_cover[i] = True
                        col_cover[j] = True
            
            # Если все строки покрыты, выходим из цикла
            if np.all(row_cover):
                break
            
            # Сбрасываем покрытия
            row_cover[:] = False
            col_cover[:] = False
        
        return marked, row_cover, col_cover
    
    # Шаг 4: Адаптация матрицы
    def adjust_matrix(matrix, row_cover, col_cover):
        min_val = np.inf
        for i in range(n):
            for j in range(n):
                if not row_cover[i] and not col_cover[j]:
                    min_val = min(min_val, matrix[i, j])
        
        for i in range(n):
            for j in range(n):
                if not row_cover[i] and not col_cover[j]:
                    matrix[i, j] -= min_val
                if row_cover[i] and col_cover[j]:
                    matrix[i, j] += min_val
    
    # Основной цикл
    while True:
        marked, row_cover, col_cover = cover_zeros(cost_matrix)
        
        # Если число незакрытых нулей равно размеру матрицы, задача решена
        if np.sum(marked) == n:
            break
        
        # Иначе адаптируем матрицу
        adjust_matrix(cost_matrix, row_cover, col_cover)
    
    # Извлекаем результат
    result = []
    for i in range(n):
        for j in range(n):
            if marked[i, j]:
                result.append((i, j))
    
    return result

# Пример матрицы стоимости
cost_matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

# Запуск алгоритма
assignments = hungarian_algorithm(cost_matrix)
print("Назначения:", assignments)
print("Общая стоимость:", sum(cost_matrix[i, j] for i, j in assignments))