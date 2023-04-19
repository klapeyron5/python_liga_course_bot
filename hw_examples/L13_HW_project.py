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

class MLModel:
    """
    Базовый класс ML-моделей.
    """
    def fit(self, X, Y):
        """
        Обучает модель.
        """
        assert len(X)==len(Y), "Длина X должна быть равна длине Y"
        if len(X)==0:
            raise ZeroDataException
    def predict(self, X):
        """
        Возвращает прогноз модели на x.
        """
    def get_params(self):
        """
        Возвращает параметры модели списком, в порядке как в аргументах __init__.
        """
    
    def save(self, file):
        """
        Сохраняет параметры модели в файл.
        """
        to_save = ','.join([str(round(float(x),4)) for x in self.get_params()])
        return to_save
    
    @classmethod
    def load(cls, file):
        """
        Загружает параметры модели из файла, инициализирует ими инстанс модели и возвращает.
        """
        return cls(*[float(x) for x in file.split(',')])

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
    
    def fit(self, X, Y):
        super().fit(X,Y)
        N = len(X)
        if len(set(X))==1:
            self.b1 = 0
        else:
            self.b1 = (sum_multiplication(X,Y)/N-sum(X)*sum(Y)/N**2)/(sum_squares(X)/N-(sum(X)/N)**2)
        self.b0 = sum(Y)/N-self.b1*sum(X)/N
#         Y_predict = self.predict(X)
#         eval_dict = self.eval(Y, Y_predict)
#         return eval_dict
    
    def predict(self, X):
        """
        Возвращает список, где каждый элемент является значением линейной регрессии 
        на соответствующем элементе последовательности X.
        """
        super().predict(X)
        def predict_sample(x):
            return self.b0 + self.b1*x
        return [predict_sample(x) for x in X]
    
    @staticmethod
    def evaluate(Y_true, Y_predict):
        """
        Вычисляет метрики качества между верными ответами и предсказаниями.
        """
        N = len(Y_true)
        errs = [yt-yp for yt,yp in zip(Y_true, Y_predict)]
        mean_err = sum(errs)/N
        mean_serr = sum([e**2 for e in errs])/N
#         err_mu = mean_err
#         err_sigma = (sum([(e-err_mu)**2 for e in errs])/(N-1))**0.5
        return dict(mean_error=mean_err, mean_squared_error=mean_serr)
    
    def get_params(self):
        return self.b0, self.b1

def pipeline(X, Y_true):
    """
    С помощью input получает x,y;
    Вычисляет прогноз модели по x;
    Выводит квадратичную ошибку в stdout;
    Анализирует отклонение ошибки модели от установленного распределения ошибок.
    """
    linreg = LinearRegression()
    linreg.fit(X, Y_true)
    Y_model = linreg.predict(X)
    
    eval_stat = linreg.evaluate(Y_true, Y_model)
    err, serr = eval_stat['mean_error'], eval_stat['mean_squared_error']
    print('SE:', serr)
