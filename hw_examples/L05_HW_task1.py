def divisible_by_x(a: int, b: int):
    def divisible_by_y(c: int):
        return n % c

    return n % a + divisible_by_y(b)


n = int(input())
x = int(input())
y = int(input())
print('total remainder of divisions equals', divisible_by_x(x, y), end=';')
