from random import normalvariate

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

def calculate_zone(err, sigma, mu):
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

class MLModel:
    """
    Базовый класс ML-моделей.
    """
    def fit(self):
        """
        Обучает модель.
        """
    def predict(self, x):
        """
        Возвращает прогноз модели на x.
        """

class LinearRegression(MLModel):
    """
    Линейная функция
    """
    def __init__(self, b0=None, b1=None):
        """
        Инициализация параметров линейной регрессии
        """
        if b0 is None:
            b0 = init_weight()
        if b1 is None:
            b1 = init_weight()
        self.b0 = get_float(b0)
        self.b1 = get_float(b1)
    
    def fit(self):
        self.b0 = get_float(1)
        self.b1 = get_float(1)
        self.trn_err_mu = get_float(0)
        self.trn_err_sigma = get_float(1)
    
    def predict(self, x):
        """
        Возвращает значение линейной функции на объекте x.
        """
        y = self.b0 + self.b1*x
        return y
    
    @staticmethod
    def evaluate(y_true, y_predict):
        """
        Вычисляет метрики качества между верным ответом и предсказанием.
        """
        return squared_error(y_true, y_predict)

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
    linreg.fit()
    y_model = linreg.predict(x)
    
    serr = linreg.evaluate(y_true, y_model)
    print('SE:', serr)
    err = error(y_true, y_model)
    zone_color = calculate_zone(err=err, sigma=linreg.trn_err_sigma, mu=linreg.trn_err_mu)
    print('Error zone:', zone_color)
