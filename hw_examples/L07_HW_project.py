DEFAULT_b0 = 1
DEFAULT_b1 = 1
MU = 0
SIGMA = 1

def get_float(x):
    """
    Преобразовывает x к типу float и возвращает его.
    """
    return float(x)

class LinearRegression:
    """
    Линейная функция
    """
    def __init__(self, b0=DEFAULT_b0, b1=DEFAULT_b1):
        """
        Инициализация параметров линейной регрессии
        """
        self.b0 = b0
        self.b1 = b1
    
    def predict(self, x):
        """
        Возвращает значение линейной функции на объекте x.
        """
        y = self.b0 + self.b1*x
        return y

def error(y_true, y_model):
    """
    Вычисляет отклонение y_model от y_true.
    """
    err = y_true - y_model
    return err

def squared_error(y0, y1):
    """
    Вычисляет квадратичную разницу между двумя значениями и возвращает ее.
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

def pipeline(x, y_true):
    """
    С помощью input получает x,y;
    Вычисляет прогноз модели по x;
    Выводит квадратичную ошибку в stdout;
    Анализирует отклонение ошибки модели от установленного распределения ошибок.
    """
    x = get_float(x)
    y_true = get_float(y_true)
    
    linreg = LinearRegression()
    
    y_model = linreg.predict(x)
    serr = squared_error(y_true, y_model)
    print('SE:', serr)
    err = error(y_true, y_model)
    zone_color = calculate_zone(err)
    print('Error zone:', zone_color)
        