import turtle


# size：直线长度，n：阶数
def kochFlake(size, n):
    if n == 0:
        turtle.fd(size)
    else:
        for angle in [0, 60, -120, 60]:
            turtle.left(angle)
            kochFlake(size / 3, n - 1)


def main():
    turtle.setup(600, 600)  # 窗体大小
    turtle.penup()
    turtle.goto(-200, 100)
    turtle.pendown()
    turtle.pensize(2)  # 画笔宽度
    kochFlake(400, 3)
    turtle.right(120)
    kochFlake(400, 3)
    turtle.right(120)
    kochFlake(400, 3)
    turtle.hideturtle()


main()
