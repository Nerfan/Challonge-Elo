"""
Draws box-and-whisker plots
file: boxAndWhisker.py
author: Jeremy Lefurge
"""

import turtle as tt


def boxAndWhisker(small, q1, med, q3, large):
    """
    Draws a box-and-whisker plot given a five-number summary
    :param small: float, minimum
    :param q1: float, first quartile
    :param med: float, median
    :param q3: float, third quartile
    :param large: float, maximum
    :return:
    """
    length = large-small
    tt.setworldcoordinates(small-(length/2), 0, large+(length/2), 100)
    tt.hideturtle()
    tt.tracer(99999999999999999, 10)
    tt.up()
    tt.speed(0)

    tt.setpos(small, 50)
    tt.setheading(90)
    tt.down()
    tt.forward(5)
    tt.back(10)
    tt.forward(5)
    tt.right(90)

    tt.setpos(q1, 50)

    tt.left(90)
    tt.forward(10)
    tt.right(90)
    tt.forward(q3-q1)
    tt.right(90)
    tt.forward(20)
    tt.right(90)
    tt.forward(q3-q1)
    tt.right(90)
    tt.forward(10)
    tt.up()

    tt.setpos(med, 40)
    tt.down()
    tt.forward(20)
    tt.up()

    tt.setpos(q3, 50)
    tt.down()
    tt.setpos(large, 50)
    tt.forward(5)
    tt.back(10)
    tt.forward(5)
    tt.right(90)

    tt.update()
    tt.done()


if __name__ == "__main__":
    boxAndWhisker(1,200,300,400,500)