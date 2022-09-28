def main(x1: str, y1: str, x2: str, y2: str):
    d_x = int(x2) - int(x1)
    d_y = int(y2) - int(y1)
    if d_x != 0:
        return d_y / d_x
    return 'undefined'
