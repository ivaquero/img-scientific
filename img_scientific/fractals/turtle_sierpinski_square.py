import turtle


def sierpinski_square(points, length, level, obj):
    obj.up()
    obj.goto(points[0], points[1])
    obj.down()
    obj.seth(0)

    if level > 0:
        obj.color("light gray")
    else:
        obj.color("blue")

    for _ in range(4):
        obj.fd(length)
        obj.left(90)
    if level == 0:
        return

    sierpinski_square([points[0] + length, points[1]], length / 2, level - 1, obj)
    sierpinski_square(
        [points[0] + length, points[1] + length], length / 2, level - 1, obj
    )
    sierpinski_square([points[0], points[1] + length], length / 2, level - 1, obj)


def main():
    obj = turtle.Turtle()
    screen = turtle.Screen()
    screen.title("Sierpinski Squares")

    points = [-100, -100]
    length = 100
    level = 3
    sierpinski_square(points, length, level, obj)

    turtle.speed(0)
    turtle.hideturtle()
    screen.tracer(0, 0)
    screen.exitonclick()


main()
