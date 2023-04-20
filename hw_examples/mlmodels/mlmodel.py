from .utils import ZeroDataException


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
        with open(file, 'w') as f:
            f.write(to_save)
    
    @classmethod
    def load(cls, file):
        """
        Загружает параметры модели из файла, инициализирует ими инстанс модели и возвращает.
        """
        with open(file, 'r') as f:
            l = f.readline()
        return cls(*[float(x) for x in l.split(',')])
