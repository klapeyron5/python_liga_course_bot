def task_1(n: str, x: str, y: str):
    def divisible_by_x(a: int, b: int):
        def divisible_by_y(c: int):
            return n % c

        return n % a + divisible_by_y(b)

    n = int(n)
    x = int(x)
    y = int(y)
    print('total remainder of divisions equals', divisible_by_x(x, y), end=';')

task_1(input(), input(), input())
