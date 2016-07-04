"""
Draws a histogram for a set of data using turtle
"""

import turtle as tt

def histogram(dataSet):
    """
    Draw a histogram using turtle.

    Args:
        dataSet (list): A list of data points
    """
    data = sorted(dataSet)
    min = data[0]
    max = data[-1]
    interval = int((max-min)/10 + 0.5)
    binCounts= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    i = 0
    for point in data:
        if point >= min+(interval*(i+1)):
            i += 1
        binCounts[i] += 1
    highest = 0
    for count in binCounts:
        if count > highest:
            highest = count

    tt.setworldcoordinates(min-interval, -highest*0.1, max+interval, highest*1.1)
    tt.hideturtle()
    tt.tracer(99999999999, 10)
    tt.up()
    tt.speed(0)

    # Draw the x axis
    tt.setpos(min, 0)
    tt.down()
    tt.forward(interval*10)
    tt.setpos(min, 0)

    # Draw the y axis
    tt.left(90)
    step = int((highest//10)+1)
    for i in range(10):
        tt.forward(step)
        tt.up()
        tt.left(90)
        tt.forward(interval/10)
        tt.write(str(step*(i+1)), align="right")
        tt.back(interval/10)
        tt.right(90)
        tt.down()
    tt.back(step*10)
    tt.right(90)

    # Draw each bar
    for i in range(len(binCounts)):
        tt.left(90)
        tt.forward(binCounts[i])
        tt.right(90)
        tt.forward(interval)
        tt.right(90)
        tt.forward(binCounts[i])
        tt.up()
        tt.forward(highest/40)
        tt.write(str(int(min+(interval*(i+1)))), align="center")
        tt.back(highest/40)
        tt.down()
        tt.left(90)

    tt.update()
    tt.done()
