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
SIGMA = 1
MU = 0

def linear_regression(x, b0=DEFAULT_b0, b1=DEFAULT_b1):
    """
    Возвращает значение линейной функции на объекте x.
    """
    y = b0 + b1*x
    return y

def error(y0, y1):
    """
    Вычисляет разницу между двумя значениями.
    """
    return y0 - y1

def squared_error(y0, y1):
    """
    Вычисляет квадрат разницы между двумя значениями.
    """
    err = error(y0, y1)**2
    return err

def calculate_zone(err, sigma=SIGMA, mu=MU):
    """
    Вычисляет зону, в которой находится отклонение.
    Если отклонение находится в критической зоне, возвращает "red".
    Также может вернуть "orange" или "green".
    """
    abs_err = abs(err)
    if mu-2*sigma <= abs_err <= mu+2*sigma:
        return 'green'
    elif (mu-3*sigma <= abs_err < mu-2*sigma) or (mu+2*sigma < abs_err <= mu+3*sigma):
        return 'orange'
    else:
        return 'red'

def pipeline():
    """
    С помощью input получает x,y;
    Вычисляет прогноз модели по x;
    Выводит квадратичную ошибку в stdout;
    Анализирует отклонение ошибки модели от установленного распределения ошибок.
    """
    x = get_x()
    y_true = get_y()
    y_model = linear_regression(x)
    se = squared_error(y_true, y_model)
    print('SE:', se)
    err = error(y_true, y_model)
    zone_color = calculate_zone(err)
    print('Error zone:', zone_color)
