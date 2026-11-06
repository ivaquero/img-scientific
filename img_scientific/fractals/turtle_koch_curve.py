import turtle


# size：直线长度，n：阶数
def kochCurve(size, n):
    if n == 0:
        turtle.fd(size)
    else:
        for angle in [0, 60, -120, 60]:
            turtle.left(angle)
            kochCurve(size / 3, n - 1)


def main():
    turtle.setup(800, 400)  # 窗体大小
    turtle.penup()
    turtle.goto(-300, -50)
    turtle.pendown()
    turtle.pensize(2)  # 画笔宽度
    kochCurve(600, 3)
    turtle.hideturtle()


main()
