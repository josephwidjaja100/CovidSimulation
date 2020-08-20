# Updated Animation Starter Code

from tkinter import *
from googletrans import Translator
import random

####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.simulationX = data.width / 5
    data.simulationY = data.height * 3 / 5
    data.contaminated = [(10, 10)]
    data.cured = []
    data.graph = [1] * 500
    data.day = 1
    data.i = 0
    data.paused = True
    data.probibility = 20
    data.cureProbibility = 100
    data.count = 0
    data.infect = 30

def mousePressed(event, data):
    # use event.x and event.y
    data.paused = not data.paused

def keyPressed(event, data):
    # use event.char and event.keysym

    if(event.char == "r"):
        data.contaminated = [(10, 10)]
        data.cured = []
        data.graph = [1] * 500
        data.day = 1
        data.i = 0
        data.probibility = 15
        data.cureProbibility = 20

def timerFired(data):
    if(data.paused == False):
        for c in data.contaminated:
            if(random.randint(0,data.infect) == 4 and (c[0]+1, c[1]) not in data.contaminated and (c[0]+1, c[1]) not in data.cured):
                data.contaminated.append((c[0]+1, c[1]))
            elif(random.randint(0,data.infect) == 4 and (c[0], c[1]+1) not in data.contaminated and (c[0], c[1]+1) not in data.cured):
                data.contaminated.append((c[0], c[1]+1))
            elif(random.randint(0,data.infect) == 4 and (c[0]-1, c[1]) not in data.contaminated and (c[0]-1, c[1]) not in data.cured):
                data.contaminated.append((c[0]-1, c[1]))
            elif(random.randint(0,data.infect) == 4 and (c[0], c[1]-1) not in data.contaminated and (c[0], c[1]-1) not in data.cured):
                data.contaminated.append((c[0], c[1]-1))
            data.graph[data.i] = len(data.contaminated)
        data.i += 1
        data.day += 1

    if(data.paused == False and data.day > 100):

        for c in data.contaminated:
            if(random.randint(0, data.probibility) == 4):
                data.contaminated.remove(c)
                data.cured.append(c)

            if(data.day > 110):
                data.graph[data.i] = len(data.contaminated)
            else:
                data.graph[data.i] = data.graph[data.i-1]

        data.i += 1


        if(data.probibility >= 10):
            data.probibility -= 1

        data.count += 1

    if(len(data.contaminated) == 0 and data.cured != []):
        for i in range(20):
            for j in range(20):
                if((i, j) not in data.cured and random.randint(0, data.cureProbibility) == 4):
                    data.cured.append((i, j))
                    if(data.cureProbibility > 5):
                        data.cureProbibility -= 1

def redrawAll(canvas, data):
    # draw in canvas
    canvas.create_rectangle(data.simulationX - data.width / 8, data.simulationY - data.width / 8, data.simulationX + data.width / 8, data.simulationY + data.width / 8)
    for i in range(20):
        for j in range(20):
            canvas.create_rectangle(data.simulationX - data.width / 8 + data.width / 80 * i, data.simulationY - data.width / 8 + data.width / 80 * j, data.simulationX - data.width / 8 + data.width / 80 * (i+1), data.simulationY - data.width / 8 + data.width / 80 * (j+1))

            if((i, j) in data.contaminated):
                canvas.create_rectangle(data.simulationX - data.width / 8 + data.width / 80 * i, data.simulationY - data.width / 8 + data.width / 80 * j, data.simulationX - data.width / 8 + data.width / 80 * (i+1), data.simulationY - data.width / 8 + data.width / 80 * (j+1), fill = "red")
            elif((i, j) in data.cured):
                canvas.create_rectangle(data.simulationX - data.width / 8 + data.width / 80 * i, data.simulationY - data.width / 8 + data.width / 80 * j, data.simulationX - data.width / 8 + data.width / 80 * (i+1), data.simulationY - data.width / 8 + data.width / 80 * (j+1), fill = "#00c000")

    canvas.create_text(data.simulationX, data.simulationY - data.width / 5, text = "Day: " + str(data.day), font = "Ariel " + str(int(data.width*3/80)))

    canvas.create_line(data.width / 2 - data.width / 15, data.height / 2 - data.height / 4, data.width / 2 - data.width / 15, data.height / 2 + data.height / 4)
    canvas.create_line(data.width / 2 - data.width / 15, data.height / 2 + data.height / 4, data.width - data.width / 15, data.height / 2 + data.height / 4)

    for i in range(0, 200, int(data.width / 200)):
        if(data.graph[i] != 1):
            canvas.create_rectangle(data.width / 2 - data.width / 15 + i, data.height / 2 - data.height / 4 + data.height / 2 - data.graph[i]/4, data.width / 2 + i + data.width / 200 - data.width / 15, data.height / 2 + data.height / 4, fill = "dark blue", width = 0)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10 # milliseconds
    root = Tk()
    translator = Translator()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 200)
