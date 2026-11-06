import turtle


def sierpinski_triangle(points, color, obj):
    obj.fillcolor(color)
    obj.up()
    obj.goto(points[0][0], points[0][1])
    obj.down()
    obj.begin_fill()
    obj.goto(points[1][0], points[1][1])
    obj.goto(points[2][0], points[2][1])
    obj.goto(points[0][0], points[0][1])
    obj.end_fill()


def getMid(p1, p2):
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)


def sierpinski(points, level, obj):
    colormap = ["blue", "red", "green", "white", "yellow", "violet", "orange"]
    sierpinski_triangle(points, colormap[level], obj)
    if level > 0:
        sierpinski(
            [points[0], getMid(points[0], points[1]), getMid(points[0], points[2])],
            level - 1,
            obj,
        )
        sierpinski(
            [points[1], getMid(points[0], points[1]), getMid(points[1], points[2])],
            level - 1,
            obj,
        )
        sierpinski(
            [points[2], getMid(points[2], points[1]), getMid(points[0], points[2])],
            level - 1,
            obj,
        )


def main():
    obj = turtle.Turtle()
    screen = turtle.Screen()
    screen.title("Sierpinski Triagles")

    points = [[-100, -50], [0, 100], [100, -50]]  # triangle
    sierpinski(points, 3, obj)

    turtle.speed(0)
    turtle.hideturtle()
    screen.tracer(0, 0)
    screen.exitonclick()


main()
