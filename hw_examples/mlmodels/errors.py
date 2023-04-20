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
