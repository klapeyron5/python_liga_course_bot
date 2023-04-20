from .mlmodel import MLModel
from .errors import error, squared_error
from .utils import ZeroDataException, get_float, init_weight, sum, sum_squares, sum_multiplication


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
    
    def get_params(self):
        return self.b0, self.b1
    
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
