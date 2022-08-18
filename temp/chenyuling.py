import random

xx = []
for i in range(1, 10):
    for j in range(1, 10):
        if j >= i:
            xx.append([i, j, i * j])

for i in range(0, 100):
    num1 = random.randint(1, len(xx) - 1)
    num2 = random.randint(1, len(xx) - 1)
    num3 = random.randint(1, len(xx) - 1)
    num4 = random.randint(1, len(xx) - 1)
    num5 = random.randint(1, len(xx) - 1)
    # print(
    #     "{:>1d} X {:>1d} =\t\t{:>1d} X {:>1d} =\t\t{:>1d} X {:>1d} =\t\t{:>1d} X {:>1d} =\t\t{:>1d} X {:>1d} =".format(
    #         xx[num1][0], xx[num1][1],
    #         xx[num2][0], xx[num2][1],
    #         xx[num3][0], xx[num3][1],
    #         xx[num4][0], xx[num4][1],
    #         xx[num5][0], xx[num5][1]))

    # print(
    #     "{:>2d} ➗ {:>2d} =\t\t{:>2d} ➗ {:>2d} =\t\t{:>2d} ➗ {:>2d} =\t\t{:>2d} ➗ {:>2d} =\t\t{:>2d} ➗ {:>2d} =".format(
    #         xx[num1][2], xx[num1][0],
    #         xx[num2][2], xx[num2][1],
    #         xx[num3][2], xx[num3][0],
    #         xx[num4][2], xx[num4][1],
    #         xx[num5][2], xx[num5][0]))

for i in range(0, 100):
    jia = []
    for j in range(0, 5):
        jia.append([random.randint(1, 99), random.randint(1, 99)])
    # print(
    #     "{:>2d} + {:>2d} =\t\t{:>2d} + {:>2d} =\t\t{:>2d} + {:>2d} =\t\t{:>2d} + {:>2d} =\t\t{:>2d} + {:>2d} =".format(
    #         jia[0][0], jia[0][1],
    #         jia[1][0], jia[1][1],
    #         jia[2][0], jia[2][1],
    #         jia[3][0], jia[3][1],
    #         jia[4][0], jia[4][1],
    #     ))

for i in range(0, 100):
    jian = []
    for j in range(0, 5):
        num = random.randint(1, 99)
        jian.append([num, random.randint(num, 99)])
    print("{:>2d} - {:>2d} =\t\t{:>2d} - {:>2d} =\t\t{:>2d} - {:>2d} =\t\t{:>2d} - {:>2d} =\t\t{:>2d} - {:>2d} =".format(
            jian[0][1], jian[0][0],
            jian[1][1], jian[1][0],
            jian[2][1], jian[2][0],
            jian[3][1], jian[3][0],
            jian[4][1], jian[4][0],
        ))
