def get_int(tip=''):
    """
    Считывает целое число с помощью input и возвращает его.
    """
    a = int(input(tip))
    return a

def get_x():
    """
    Запрашивает у пользователя объект x и возвращает его.
    """
    x = get_int('Введите x:')
    return x

def get_y():
    """
    Запрашивает у пользователя объект y и возвращает его.
    """
    y = get_int('Введите y:')
    return y

DEFAULT_b0 = 1
DEFAULT_b1 = 1

def linear_regression(x, b0=DEFAULT_b0, b1=DEFAULT_b1):
    """
    Возвращает значение линейной функции на объекте x.
    """
    y = b0 + b1*x
    return y

def squared_error(y0, y1):
    """
    Вычисляет квадратичную разницу между двумя значениями и возвращает ее.
    """
    err = (y0 - y1)**2
    return err

def pipeline():
    """
    С помощью input получает x,y;
    Вычисляет прогноз модели по x;
    Выводит квадратичную ошибку в stdout.
    """
    x = get_x()
    y_true = get_y()
    y_model = linear_regression(x)
    err = squared_error(y_true, y_model)
    print('SE:', 'asdf')
