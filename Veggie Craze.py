
from tkinter import *
from math import *
from time import *
from random import *

root = Tk()
screen = Canvas(root, width=600, height=800, background="#66D5CC")

#IMPORT IMAGES
def importImages():
    global introimg, shovelimg, dirtimg, basketimg
    global carrotimg, beetimg, turnipimg, flowerimg, grassimg
    introimg = PhotoImage(file = "intro.gif")
    shovelimg = PhotoImage(file = "shovel.gif")
    dirtimg = PhotoImage(file = "dirt.gif")
    basketimg = PhotoImage(file = "basket.gif")
    carrotimg = PhotoImage(file = "carrot.gif")
    beetimg = PhotoImage(file = "beet.gif")
    turnipimg = PhotoImage(file = "turnip.gif")
    flowerimg = PhotoImage(file = "flower.gif")
    grassimg = PhotoImage(file = "grass.gif")

#SETTING INITIAL VALUES
def setInitialValues():
    global xMouse, yMouse, gameRunning, score, currentLevel, screenMode
    global vegs, xVeg, yVeg, typeVeg, numVeg, timePlanted, clickedVeg
    global shovel, xShovel, yShovel, messageText, messageTime

    score = 0
    screenMode = 0
    gameRunning = False

    messageText = []
    messageTime = []
    
    vegs = []
    xVeg = []
    yVeg = []
    typeVeg = []
    numVeg = 0
    timePlanted = []
    clickedVeg = False

    shovel = 0
    xShovel = 0
    yShovel = 0
    
    xMouse = 0
    yMouse = 0
    
#DRAWS THE SHOVEL
def drawShovel ():
    global shovel
    screen.delete(shovel)
    shovel = screen.create_image(xShovel,yShovel, image = shovelimg)
    screen.update()
    
#INTRO SCREEN
def drawIntroScreen():
    global screenMode, introscreen, text1, text2, text3, text4
    screenMode = 0
    introscreen = screen.create_image(300,400, image = introimg)
    text1 = screen.create_text (300,625, text = "Right click on the vegetables to dig them up!", font = "Helvetica 15 bold", fill = "white")
    text2 = screen.create_text (300,650, text = "Carrots give 5 points, beets give 25!", font = "Helvetica 15 bold", fill = "white")
    text3 = screen.create_text (300,675, text = "Turnips add a 3 second time bonus!", font = "Helvetica 15 bold", fill = "white")
    text4 = screen.create_text (300,700, text = "Watch out for flowers as they remove 5 seconds!", font = "Helvetica 15 bold", fill = "white")
    
    
#CHOOSE THE DIFFICULTY 
def chooseDifficulty():
    global easyButton, medButton, hardButton
    easyButton = Button(root, text = "EASY", font = "Helvetica 20", command = easyButtonPressed, anchor = CENTER)
    medButton = Button(root, text = "MEDIUM", font = "Helvetica 20", command = medButtonPressed, anchor = CENTER) 
    hardButton = Button(root, text = "HARD", font = "Helvetica 20", command = hardButtonPressed, anchor = CENTER)
    easyButton.pack()
    medButton.pack()
    hardButton.pack()
    easyButton.place(x = 225, y = 200, width = 175, height = 50)
    medButton.place(x = 225, y = 400, width = 175, height = 50)
    hardButton.place(x = 225, y = 600, width = 175, height = 50)
    screen.update()
    
#CALLED WHEN THE EASY BUTTON IS PRESSED
def easyButtonPressed():
    global easyButton, medButton, hardButton, gameTime, totalVeg, screenMode, timeUp
    easyButton.destroy()
    medButton.destroy()
    hardButton.destroy()
    screenMode = 2
    gameTime = 30
    totalVeg = 25
    timeUp = 3
    runGame()

#CALLED WHEN THE MEDIUM BUTTON IS PRESSED
def medButtonPressed():
    global easyButton, medButton, hardButton, gameTime, totalVeg, screenMode, timeUp
    easyButton.destroy()
    medButton.destroy()
    hardButton.destroy()
    screenMode = 3
    gameTime = 20
    totalVeg = 20
    timeUp = 2
    runGame()

#CALLED WHEN THE HARD BUTTON IS PRESSED
def hardButtonPressed():
    global easyButton, medButton, hardButton, gameTime, totalVeg, screenMode, timeUp
    easyButton.destroy()
    medButton.destroy()
    hardButton.destroy()
    screenMode = 4
    
    gameTime = 10
    totalVeg = 15
    timeUp = 1
    runGame()
  
#CALLED WHEN THE MOUSE IS CLICKED
def mouseClickHandler (event):
    global introscreen, text1, text2, text3, text4, xMouse, yMouse
    global typeVeg, xVeg, yVeg, clickedVeg
    xMouse = event.x
    yMouse = event.y
    #IF ITS THE INTRO SCREEN, CHECK IF THE USER CLICKED PLAY
    if screenMode == 0:
        if xMouse >=150 and xMouse <=450 and yMouse >= 450 and yMouse <=550:
            screen.delete(introscreen, text1, text2, text3, text4)
            chooseDifficulty()
    #CHECK IF THE USER CLICKED A VEGETABLE
    else:
        for i in range(numVeg):
            if xMouse >= xVeg[i]-25 and xMouse <= xVeg[i]+25 and yMouse >= yVeg[i]-25 and yMouse <= yVeg[i]+25:
                updateScore(i)
                deleteVeg(i)
                clickedVeg = True
                break
            
#CALLED WHEN MOUSE IS MOVING
def mouseMotionHandler (event):
    global xShovel,yShovel
    xShovel = event.x
    yShovel = event.y
    if screenMode != 0:
        drawShovel()

#BACKGROUND
def createBackground():
    global score, currentScore, gameTime, timeText
    #GRASS
    screen.create_image(300,225, image = grassimg)
    #BASKET
    screen.create_image(300,100, image = basketimg)
    #DIRT BACKGROUND
    screen.create_image(300,525, image = dirtimg)
    #TIME LEFT BOX
    screen.create_rectangle (10,10,210,80, fill = "chartreuse3", outline = "chartreuse3")
    screen.create_text (65,25, text = "TIME LEFT", font = "Helvetica 15", fill = "white")
    timeText = screen.create_text (150,55, text = gameTime, font = "Helvetica 24 bold", fill = "white")
    #SCORE BOX
    screen.create_rectangle(390,10,590,80, fill = "orange", outline = "orange")
    screen.create_text (430,25, text = "SCORE", font = "Helvetica 15", fill = "white")
    currentScore = screen.create_text (550,55, text = score, font = "Helvetica 24 bold", fill = "white")

#PUTS THE VEGETABLE IN BASKET IF YOU CLICKED ON IT
def vegInBasket(i):
    global xVeg, yVeg, typeVeg
    xVeg[i] = randint(250,350)
    yVeg[i] = randint(90,110)
    if typeVeg[i] == "CARROT":
        screen.create_image(xVeg[i],yVeg[i], image = carrotimg)
    elif typeVeg[i] == "BEET":
        screen.create_image(xVeg[i],yVeg[i], image = beetimg)
    elif typeVeg[i] == "TURNIP":
        screen.create_image(xVeg[i],yVeg[i], image = turnipimg)
    elif typeVeg[i] == "FLOWER":
        screen.create_image(xVeg[i],yVeg[i], image = flowerimg)
    
#RANDOMLY PLANTS THE VEGETABLE
def placeVeg():
    global vegs, numVeg, xVeg, yVeg, typeVeg
    if numVeg < totalVeg:
        xVeg.append(choice([100,200,300,400,500]))
        yVeg.append(choice([250,350,450,550,650]))
        numVeg = numVeg + 1
        vegs.append(0)
        timePlanted.append(time())
        #RANDOMLY CHOOSES A VEGETABLE TO PLANT
        typesofveg = randint(0,65)
        if 0 <= typesofveg <=25:
            typeVeg.append("CARROT")
        elif 26 <= typesofveg <= 40:
            typeVeg.append("BEET")
        elif 41 <= typesofveg <= 50:
            typeVeg.append("TURNIP")
        elif 51 <= typesofveg <= 65:
            typeVeg.append("FLOWER")
                
#CREATING THE VEGETABLE
def drawVeg():
    global vegs, xVeg, yVeg, typeVeg, numVeg, timePlanted
    for i in range(numVeg):
        if typeVeg[i] == "CARROT":
            vegs[i] = screen.create_image(xVeg[i],yVeg[i], image = carrotimg)
        elif typeVeg[i] == "BEET":
            vegs[i] = screen.create_image(xVeg[i],yVeg[i], image = beetimg)
        elif typeVeg[i] == "TURNIP":
            vegs[i] = screen.create_image(xVeg[i],yVeg[i], image = turnipimg)
        elif typeVeg[i] == "FLOWER":
            vegs[i] = screen.create_image(xVeg[i],yVeg[i], image = flowerimg)
        
#DELETE THE VEGETABLE IF HIT
def deleteVeg(i):
    global vegs, numVeg, timePlanted, clickedVeg
    if clickedVeg == True:
        vegInBasket(i)
    clickedVeg = False
    screen.delete(vegs[i])
    vegs.pop(i)
    xVeg.pop(i)
    yVeg.pop(i)
    typeVeg.pop(i)
    timePlanted.pop(i)
    numVeg = numVeg - 1

#DELETES VEGETABLES AFTER A WHILE
def checkVegs():
    currentTime = time()
    i = 0
    while i < numVeg:
        timePassed = currentTime - timePlanted[i]
        if timePassed >= timeUp:
            deleteVeg(i)
        i = i + 1        
        
#DELETES ALL THE VEGETABLES
def deleteAllVeg():
    global vegs, numVeg, typeVeg
    for i in range(numVeg):
        screen.delete(vegs[i])
        
#UPDATES TIME
def updateTime():
    global gameTime, timeText, beginningTime
    currentTime = time()
    timePassed = currentTime - beginningTime
    if timePassed >= 1:
        gameTime = gameTime - 1
        screen.delete (timeText)
        timeText = screen.create_text (150,55, text = gameTime, font = "Helvetica 24 bold", fill = "white")
        beginningTime = time()
        placeVeg()       
        
#UPDATE THE SCORE
def updateScore(i):
    global score, currentScore
    if typeVeg[i] == "CARROT":
        score = score + 5
        createMessage("+5 points", xVeg[i], yVeg[i])
    elif typeVeg[i] == "BEET":
        score = score + 25
        createMessage("+25 points", xVeg[i], yVeg[i])
    elif typeVeg[i] == "TURNIP":
        extraTime(i)
    elif typeVeg[i] == "FLOWER":
        lessTime(i)
    screen.delete(currentScore)
    currentScore = screen.create_text (550,55, text = score, font = "Helvetica 24 bold", fill = "white")

#GIVES EXTRA TIME IF THE USER CLICKS ON A TURNIP
def extraTime(i):
    global gameTime, timeText
    gameTime = gameTime + 3
    createMessage("+3 seconds", xVeg[i], yVeg[i])
    screen.delete(timeText)
    timeText = screen.create_text (150,55, text = gameTime, font = "Helvetica 24 bold", fill = "white")
    
#TAKES AWAY TIME IF THE USER CLICKS ON A FLOWER
def lessTime(i):
    global gameTime, timeText
    gameTime = gameTime - 5
    createMessage("-5 seconds", xVeg[i], yVeg[i])
    screen.delete(timeText)
    timeText = screen.create_text (150,55, text = gameTime, font = "Helvetica 24 bold", fill = "white")
    
#CREATES MESSAGE IF YOU DUG UP A VEGETABLE    
def createMessage(msg,xmsg,ymsg):
    global messageText, messageTime
    message = screen.create_text(xmsg,ymsg, text = msg, font = "Helvetica 12 bold", fill = "white")
    messageText.append(message)
    messageTime.append(time())

#DELETES THE MESSAGE AFTER A WHILE
def deleteMessage():
    global messageText, messageTime
    for i in range(len(messageText)):
        currentTime = time()
        timeElapsed = currentTime - messageTime[i]
        if timeElapsed >= 0.5:
            screen.delete(messageText[i])
            messageText.remove(messageText[i])
            messageTime.remove(messageTime[i])
            break
            
#COUNTDOWN THE NUMBERS
def countdownClock():
    for i in range(3,-1,-1):
        if i == 0:
            countdown = screen.create_text (300,400, text = "Start!", font = "Helvetica 64 bold", fill = "white")
        else:
            countdown = screen.create_text (300,400, text = i, font = "Helvetica 64 bold", fill = "white")
        screen.update()
        sleep(1)
        screen.delete(countdown)

#STARTS THE GAME
def startGame():
    global gameRunning
    gameRunning = True
    importImages()
    setInitialValues()
    drawIntroScreen()
    
#RUNS THE MAIN GAME    
def runGame():
    global gameTime, beginningTime, screen, screenMode
    importImages()
    createBackground()
    countdownClock()
    screenMode = 1
    beginningTime = time()
    while gameTime > 0:
        gameRunning = True
        updateTime()
        deleteMessage()
        drawVeg()
        screen.update()
        sleep(0.1)
        checkVegs()
        deleteAllVeg()
    endGame()

#ENDS THE GAME
def endGame():
    global score, gameRunning, over
    gameRunning = False
    end = screen.create_text (300,400, text = "Game Over", font = "Helvetica 64 bold", fill = "white")
    screen.update()
    sleep(2)
    screen.delete(end)
    finalscore = screen.create_text(300,325, text = "Final Score:", font = "Helvetica 32 bold", fill = "white")
    scorenum = screen.create_text(300,400, text = score, font = "Helvetica 55 bold", fill = "white")
    screen.update()
    sleep(2)
    screen.delete(finalscore,scorenum)
    over = screen.create_text(300,400, text = "Click 'R' to restart or 'Q' to quit", font = "Helvetica 30 bold", fill = "white")
    root.bind("<Key>", endMenu)
    
def endMenu(event):
    global over
    if event.keysym == "r" or "R":
        screen.delete(over)
        startGame()
    elif event.keysym == "q" or "Q":
        root.destroy()

#RUNS THE GAME AFTER 0 SECONDS
root.after(0, startGame)

#BINDS THE PROCEDURE mouseClickHandler TO ALL MOUSE-DOWN EVENTS
screen.bind("<Button-1>", mouseClickHandler)

#BINDS THE PROCEDURE mouseReleaseHandler TO ALL MOUSE-MOTION EVENTS
screen.bind("<Motion>", mouseMotionHandler)

screen.pack()
screen.focus_set()
root.mainloop()
