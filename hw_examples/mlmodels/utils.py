from random import normalvariate

class ZeroDataException(Exception):
    pass

def get_float(x):
    """
    Преобразовывает x к типу float и возвращает его.
    """
    return float(x)

def init_weight():
    """
    Возвращает инициализирующее значение для числа.
    """
    return normalvariate(mu=0, sigma=0.3)

def sum(X):
    """сумма"""
    S = 0
    for x in X:
        S += x
    return S

def sum_squares(X):
    """Сумма квадратов"""
    S = 0
    for x in X:
        S += x**2
    return S

def sum_multiplication(X, Y):
    """Сумма попарных произведений"""
    S = 0
    for i in range(len(X)):
        S += X[i]*Y[i]
    return S
