from . import mlmodels

def pipeline(X, Y_true):
    """
    С помощью input получает x,y;
    Вычисляет прогноз модели по x;
    Выводит квадратичную ошибку в stdout;
    Анализирует отклонение ошибки модели от установленного распределения ошибок.
    """
    linreg = mlmodels.linreg.LinearRegression()
    linreg.fit(X, Y_true)
    Y_model = linreg.predict(X)
    
    eval_stat = linreg.evaluate(Y_true, Y_model)
    err, serr = eval_stat['mean_error'], eval_stat['mean_squared_error']
    print('SE:', serr)
