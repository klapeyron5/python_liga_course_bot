def get_x():
    """
    Запрашивает у пользователя объект x и возвращает его.
    """
    x = int(input('Введите x:'))
    return x

def get_y():
    """
    Запрашивает у пользователя объект y и возвращает его.
    """
    y = int(input('Введите y:'))
    return y

def squared_error(y0, y1):
    """
    Вычисляет квадратичную разницу между двумя значениями и возвращает ее.
    """
    err = (y0 - y1)**2
    return err

def linear_regression(x, b0=1, b1=1):
    """
    Возвращает значение линейной функции на объекте x.
    """
    y = b0 + b1*x
    return y

x = get_x()
y_true = get_y()
y_model = linear_regression(x)
err = squared_error(y_true, y_model)
print('SE:', err)