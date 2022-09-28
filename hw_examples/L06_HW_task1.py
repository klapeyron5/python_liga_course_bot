def main(x: str, y: str, z: str):
    x = int(x)
    y = int(y)
    z = int(z)
    if x and y:
        print('life detected', end='!')
    elif x or y:
        if z:
            print('life detected', end='!')
        else:
            print('nothing', end='...')
    else:
        print('nothing', end='...')
