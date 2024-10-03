import time
import random
import math
from tkinter import *
import keyboard
from functools import partial
import winsound

root = Tk()
root.geometry('1920x1080')
root.resizable(0, 0)
root.title('Project Diva: Parkour')

#SUBMITTED APRIL 1ST 11:30

#function for reading data from the text files and turning them into variables. 
def openReadFile(direct):
    with open(direct) as f:
        directtxt = f.readlines()
    
    directData = ['' for i in range (len(directtxt))]
    for i in range (len(directtxt)):
        for j in range (len(directtxt[i])):
            if directtxt[i][j] != '\n':
                directData[i] += directtxt[i][j]
            
    
    return directData

#function for writing data in variables into text files
def openWriteFile(direct, content):
    f = open(direct, 'w')
    writeContent = ''
    
    
    for i in range (len(content)):
        content[i] += '\n'
        writeContent += content[i]
    
    f.write(writeContent)

    f.close()



#FIRST FRAME FUNCTION DEFINITION STARTS HERE ---------------------------------------------------------------


#start user Creation process
def userCreate():
    #canvasLOGINRBcreateU
    global canvasLOGINRBselect
    global canvasLOGINRBcreateU
    userName = StringVar()
    userPassword = StringVar()
    canvasLOGINRBselect.destroy()
    canvasLOGINRBcreateU = Canvas(frameLOGIN, bg = '#6fbada', height = 810, width = 930)
    
    #widgets and objects for recording password and username entry
    userNameEntry = Entry(canvasLOGINRBcreateU, textvariable = userName)
    userPasswordEntry = Entry(canvasLOGINRBcreateU, textvariable = userPassword, show = '*')
    userNameText = canvasLOGINRBcreateU.create_text(96, 200, text = 'Username', anchor = W)
    passwordText = canvasLOGINRBcreateU.create_text(96, 400, text = 'Password', anchor = W)
    
    #upon pressing the button, conditions for user creation will be checked
    nextButton = Button(canvasLOGINRBcreateU, command = lambda: userCreationCheck(userName.get(), userPassword.get()), text = 'ENTER')
    
    
    userNameEntry.place(x = 296, y = 200, anchor = W)
    userPasswordEntry.place(x = 296, y = 400, anchor = W)
    nextButton.place(x = 864, y = 600, anchor = W)
    canvasLOGINRBcreateU.grid(row = 1, column = 1, columnspan = 2, sticky = NW)


#check user creation conditions
def userCreationCheck(user, password):
    global users
    
    #get rid of the extra blank characters at the front or back
    userNameLen = len(user)
    charEnd = False
    blankStart = True
    validChar = userNameLen
    invalidCharStart = 0

    for i in range (userNameLen):
        if (user[userNameLen - 1 - i] == ' ' or user[userNameLen - 1 - i] == '\n') and charEnd == False:
            validChar -= 1
        else:
            charEnd = True
        
        if (user[i] == ' ' or user[i] == '\n') and blankStart == True:
            invalidCharStart += 1
        else:
            blankStart = False
    
    userName = ''
    for i in range (invalidCharStart, validChar):
        userName += user[i]
        
    
    #check if the current username overlapses with other user, if it doesn't overlapse, the account is created in the userCreateGet function. Otherwise, error message will be displayed
    i = 1
    overlapCheck = False
    while i < len(users) and overlapCheck == False:
        if userName == users[i]:
            overlapCheck = True
        i += 2
    
    if validChar < 1 or overlapCheck == True:
        canvasLOGINRBcreateU.create_text(96, 600, anchor = W, text = 'Your user name overlapses, or is invalid. Enter again')
        canvasLOGINRBcreateU.update()
    else:
        userCreateGet(userName, password)


#recording user account into the "data bases" and the user directed back to login page
def userCreateGet(user, password):
    global userAmount
    global config
    global users
    global canvasLOGINRBcreateU
    
    userAmount += 1
    config[1] = str(userAmount)
    users.append(user)
    users.append(password)
    
    for i in range (len(users)):
        users[i] += '\n'
    for i in range (len(config)):
        config[i] += '\n'
    #user is recorded in the general profile
    f = open('config/config.txt', 'w')
    f.writelines(config)
    #user is recorded in the accounts
    f.close()
    f = open('users/users.txt', 'w')
    f.writelines(users)
    f.close()
    
    
    #data base for the new user is created
    initialUserStatus = "Storage\n0\nSongs\nCANDYYYLAND - tofubeats, LIZ, Pa's Lam System\n"
    newUserProfileDirect = 'users/' + user + '.txt'
    f = open(newUserProfileDirect, 'w')
    f.writelines(initialUserStatus)
    f.close()
    canvasLOGINRBcreateU.destroy()
    
    #the user is directed back to the user selection page
    userSelect()


#The user can select from the list of users and lead to login page
def userSelect():
    global canvasLOGINRBselect
    global config
    global users
    global userAmount
    
    canvasLOGINRBselect = Canvas(frameLOGIN, bg = '#6fbada', height = 810, width = 930)
    
    
    users = openReadFile('users/users.txt')
    config = openReadFile('config/config.txt')
    
    
    #creating a fluid container of the usernames
    userFrame = Frame(canvasLOGINRBselect, height = 90 + 180 * userAmount, width = 930, bg = '#6fbada')
    
    
    userButton = [0 for i in range (userAmount)]
    userButtonCommand = [0 for i in range (userAmount)]
    
    
    #create number of username buttons based on how many users there are
    for i in range (userAmount):
        userButtonCommand[i] = partial(accountVerCanvas, users[1 + i * 2]) 
        userButton[i] = Button(userFrame, text = users[1 + i * 2], command = userButtonCommand[i])
        userButton[i].place(anchor = NW, x = 96, y = 90 + 180 * i)
    
    
    #check if a scrollable region to view is necessary. If it is, a scroll region is created with scrollbar. Uppon clicking any button, the user enters the main game
    if userAmount > 4:
        canvasLOGINRBScrollBar = Scrollbar(frameLOGIN, orient = VERTICAL, width = 30, command = canvasLOGINRBselect.yview)
        canvasLOGINRBselect.create_window(0, 0, anchor = NW, window = userFrame)
        canvasLOGINRBselect.grid(row = 1, column = 1, sticky = NW)
        canvasLOGINRBScrollBar.grid(row = 1, column = 2, sticky = NS)
        canvasLOGINRBselect.config(scrollregion = canvasLOGINRBselect.bbox('all'))
        canvasLOGINRBScrollBar.config(command = canvasLOGINRBselect.yview)
        canvasLOGINRBselect.config(yscrollcommand = canvasLOGINRBScrollBar.set)
    else:
        canvasLOGINRBselect.create_window(0, 0, anchor = NW, window = userFrame)
        canvasLOGINRBselect.grid(row = 1, column = 1, columnspan = 2, sticky = NW)
        
    
    

#Here the user verifies their account information by entering their password into the entry box
def accountVerCanvas(user):
    global canvasLOGINRBselect
    global canvasLOGINRBver
    
    canvasLOGINRBselect.destroy()
    
    userPassword = StringVar()
    
    #entry box is created
    canvasLOGINRBver = Canvas(frameLOGIN, bg = 'white', height = 810, width = 930)
    passwordText = canvasLOGINRBver.create_text(96, 400, text = 'password', anchor = W)
    userPasswordEntry = Entry(canvasLOGINRBver, textvariable = userPassword, show = '*')
    
    #upon pressing the button, the user and the password entered is sent to be verified
    nextButton = Button(canvasLOGINRBver, text = 'Enter', command = lambda: passwordVer(user, userPassword.get()))
    
    userNameText = Label(canvasLOGINRBver, bg = 'White', text = 'Welcome, '+ user, font = 'Verdana 20')
    canvasLOGINRBver.create_window(96, 200, width = 738, height = 200, anchor = W, window = userNameText)
    
    userPasswordEntry.place(x = 296, y = 400, anchor = W)
    nextButton.place(x = 864, y = 600)
    canvasLOGINRBver.grid(row = 1, column = 1, columnspan = 2, sticky = NW)


#entered password is verified against the account data
def passwordVer(user, password):
    global users
    global canvasLOGINRBver
    
    
    i = 1
    check = False
    while i < len(users) and check == False:
        if user == users[i]:
            check = True
            if users[i + 1] == password:
                
                #if the password check passes, the program goes to main UI
                createMainUI(user, 'users/' + user + '.txt', frameLOGIN)
                
            else:
                #if the password check fails, the program prompts the user to enter again
                canvasLOGINRBver.create_text(96, 600, anchor = W, text = 'Password invalid. Try again')
                
        i += 2
    
#FIRST FRAME FUNCTION DEFINITIONS END HERE -----------------------------------------------------



#SECOND FRAME FUNCTION DEFINITIONS START HERE --------------------------------------------------

#The main UI
def createMainUI(user, userDirect, toDestroy):
    global frameMainUI
    global canvasMainUI
    global frameLOGIN
    global playButtonImage
    global MainUIBackground
    global karmaImage
    
    
    playButtonImage = PhotoImage(file = 'images/playButton.png')
    MainUIBackground = PhotoImage(file = 'images/MainUIbackground.png')
    karmaImage = PhotoImage(file = 'images/karma.png')
    
    userStatus = openReadFile(userDirect)
    
    userStorage = float(userStatus[1])
    toDestroy.destroy()
    
    
    frameMainUI = Frame(root, height = 1080, width = 1920)
    canvasMainUI = Canvas(frameMainUI, height = 1080, width = 1920, bg = 'blue')
    canvasMainUIBackground = canvasMainUI.create_image(0, 0, anchor = NW, image = MainUIBackground)
    canvasMainUI.create_oval(96, 78, 156, 138, fill = 'White')
    karmaImageimg = canvasMainUI.create_image(96, 108, image = karmaImage, anchor = W)
    
    
    #upon pressing, it leads to song selection screen
    buttonMainUI = Button(frameMainUI, image = playButtonImage, command = lambda: createPreGame(user, userDirect, userStatus, userStorage))
    
    
    #amount of karma displayed
    storageMainUI = canvasMainUI.create_text(156, 108, anchor = W, text = str(int(userStorage)), font = 'Times 20', fill = 'White')
    #user name displayed
    userNameMainUI = canvasMainUI.create_text(1824, 108, text = user, font = 'Times 20', fill = 'White', anchor = E)
    
    
    canvasMainUI.pack()
    buttonMainUI.place(anchor = SE, x = 1824, y = 972)
    frameMainUI.pack()


#SECOND CANVAS FUNCTION DEFINITIONS END HERE -----------------------------------------------------


#THIRD CANVAS FUNCTION DEFINITIONS START HERE ----------------------------------------------------

#song to play is selected here under conditions
def createPreGame(user, userDirect, userStatus, userStorage):
    global frameMainUI
    global framePreGame
    global config
    global songs
    global canvasSongImage
    global songButtonImages
    global songCoverImage
    global diffUnitImage
    global canvasPreGame
    
    
    frameMainUI.destroy()
    
    
    songs = openReadFile('musics/musics.txt')
    diffUnitImage = PhotoImage(file = 'images/difficulty unit.png')
    
    
    songAmount = int(config[3])
    
    framePreGame = Frame(root, height = 1080, width = 1920)
    canvasPreGame = Canvas(framePreGame, height = 1080, width = 1122, bg = 'Red')
    canvasSongImage = Canvas(framePreGame, height = 1080, width = 768, bg = 'White')
    frameCanvasPreGame = Frame(canvasPreGame, height = 216 * songAmount, width = 1122, bg = 'Blue')
    
    
    
    
    #this stores the commands for each of the buttons
    nextCommand = [0 for i in range (songAmount)]
    #initializing buttons
    songSelectButton = [0 for i in range (songAmount)]
    #this stores the name of the song and the length
    songData = [[0 for i in range (2)] for j in range (songAmount)]
    #this stores the corresponding images created for the difficulty of the song
    songDifficultyImage = [[0 for i in range (5)] for j in range (songAmount)]
    
    userStatus = openReadFile(userDirect)
    
    #this stores the songs that are unlocked by the user
    userAvailableSongs = [0 for i in range (len(userStatus) - 3)]
    for i in range (3, len(userStatus)):
        userAvailableSongs[i - 3] = userStatus[i]
    
    
    #this stores whether the corresponding song of the button is unlocked by the user or not
    buttonMode = [False for i in range (songAmount)]
    
    songButtonImages = [PhotoImage(file = 'images/' + songs[i * 6] + ' - C' + '.png') for i in range (songAmount)]
    songCoverImages = [PhotoImage(file = songs[i * 6 + 4]) for i in range (songAmount)]
    
    for i in range (songAmount):
        for j in userAvailableSongs:
            if songs[i * 6] == j:
                buttonMode[i] = True
            
        #if the song is unlocked, clicking the button of the song will make the rightside fo the buttons the confirmation screen
        if buttonMode[i] == True:
            nextCommand[i] = partial(songImagePlay, songCoverImages[i], float(songs[i * 6 + 2]), songs[i * 6 + 3], user, userDirect, userStorage, songs[i * 6 + 4], userStatus, float(songs[i * 6 + 5]), canvasSongImage)


        #the song isn't unlocked, clicking the button of the song will make the rightside of the buttons the purchase song screen
        else:
            nextCommand[i] = partial(songLock, songCoverImages[i], float(songs[i * 6 + 2]), songs[i * 6 + 3], user, userDirect, userStorage, songs[i * 6 + 4], songs[i * 6], userStatus, float(songs[i * 6 + 5]))
        
        labelTemp = Label(image = songButtonImages[i])
        
        songSelectButton[i] = Button(frameCanvasPreGame, width = 1122, height = 216, image = songButtonImages[i], command = nextCommand[i]) # mainGameCommand[i]
        songData[i][0] = Label(frameCanvasPreGame, text = songs[i * 6])
        songData[i][1] = Label(frameCanvasPreGame, text = str(math.floor(float(songs[i * 6 + 2]) // 60)) + ':' + str(math.floor(float(songs[i * 6 + 2]) % 60)))
        
        songSelectButton[i].place(anchor = NW, x = 0, y = i* 216)
        
        #this displays image
        for j in range (int(songs[i * 6 + 1])):
            
            
            songDifficultyImage[i][j] = Label(frameCanvasPreGame, image = diffUnitImage)
            songDifficultyImage[i][j].place(y = 206 + i * 216, x = 10 + j * 80, anchor = SW)
            
        songData[i][0].place(x = 10, y = 10 + i* 216, anchor = NW)
        songData[i][1].place(x = 1112, y = 206 + i* 216, anchor = SE)
    
    #prepare the scrollable region for buttons for song if the screen cannot fit all of the buttons
    canvasPreGame.create_window(0, 0, anchor = NW, window = frameCanvasPreGame)
    
    #if creating scrollbar is necessary, then scrollbar is created and the region is made scrollable
    if songAmount > 5:
        songSelectScrollBar = Scrollbar(framePreGame, width = 30, orient = VERTICAL)
        canvasPreGame.grid(row = 0, column = 0, sticky = NW)
        songSelectScrollBar.grid(row = 0, column = 1, sticky = NS)
        canvasSongImage.grid(row = 0, column = 2, sticky = NW)
        canvasPreGame.config(scrollregion = canvasPreGame.bbox('all'))
        songSelectScrollBar.config(command = canvasPreGame.yview)
        canvasPreGame.config(yscrollcommand = songSelectScrollBar.set)
        
    else:
        canvasPreGame.grid(row = 0, column = 0, sticky = NW)
        canvasSongImage.grid(row = 0, column = 1, sticky = NE)
    
    
    
    framePreGame.pack()


#THIRD CANVAS FUNCTION DEFINITIONS END HERE -----------------------------------------------------

#this is the confirmation canvas to start the game
def songImagePlay(songImage, endTime, songDirect, user, userDirect, userStorage, songImageDirect, userStatus, screenRate, toDestroy):
    global karmaImage
    
    toDestroy.destroy()
    
    canvasSongImage = Canvas(framePreGame, height = 1080, width = 768, bg = 'Green')
    
    canvasSongImageDisplay = canvasSongImage.create_image(0, 0, image = songImage, anchor = NW)
    
    #upon pressing this button, the game begins based on the parameters of the song
    confirmButton = Button(canvasSongImage, text = 'PLAY', font = 'Verdana 20', command = lambda: MainGame(endTime, songDirect, user, userDirect, userStorage, songImageDirect, userStatus, screenRate))
    
    
    confirmButton.place(x = 384, y = 810, anchor = CENTER)
    canvasSongImage.grid(row = 0, column = 2, sticky = NW)


#this creates the canvas to the right that processes song purchasing
def songLock(songImage, endTime, songDirect, user, userDirect, userStorage, songImageDirect, songName, userStatus, screenRate):
    global canvasSongLock
    
    canvasSongLock = Canvas(framePreGame, height = 1080, width = 768, bg = 'Black')
    
    canvasSongLockDisplay = canvasSongLock.create_image(0, 0, image = songImage, anchor = NW)
    
    
    
    
    canvasSongLock.create_image(77, 138, image = karmaImage, anchor = W)
    storageAmountDisplay = Label(canvasSongLock, text = str(int(userStorage)), fg = 'White', bg = '#4f5161', font = 'Times 15')
    
    #upon pressing, the conditions for purchasing is checked
    confirmButton = Button(canvasSongLock, text = 'PURCHASE', command = lambda: purchaseSong(songImage, endTime, songDirect, user, userDirect, userStorage, songImageDirect, songName, userStatus, screenRate))
    storageAmountDisplay.place(x = 137, y = 138, anchor = W)
    confirmButton.place(x = 384, y = 810, anchor = CENTER)
    canvasSongLock.grid(row = 0, column = 2, sticky = NW)
    
    
#purchasing condition is checked. 
def purchaseSong(songImage, endTime, songDirect, user, userDirect, userStorage, songImageDirect, songName, userStatus, screenRate):
    global canvasSongLock
    global canvasPreGame
    
    #the purchase will be passed if the user has more than 50000 karma. If it is the case, 50000 karma will be removed from the user's inventory. Otherwise, the purchase will be rejected
    if userStorage >= 100000:
        userStorage -= 100000
        userStatus[1] = str(userStorage)
        userStatus.append(songName)

        openWriteFile(userDirect, userStatus)
        
        userStorage = float(userStatus[1])
        framePreGame.destroy()
        createPreGame(user, userDirect, userStatus, userStorage)
        
    else:
        rejectText = canvasSongLock.create_text(384, 900, text = "You don't have enough karma to purchase the song. The song requires 50000 karma.")
        
    
#MAIN GAME FUNCTION DEFINITIONS START HERE ---------------------------------------------------------------

def MainGame(endTime, songDirect, user, userDirect, userStorage, songImageDirect, userStatus, screenRate):
    global framePreGame
    global canvasMGI
    global bonusImage

    
    framePreGame.destroy()
    
    #initialization canvas
    canvasMGI = Canvas(root, height = 1080, width = 1920)
    terrainImage = PhotoImage(file = "images/terrain.gif")
    bgImage = PhotoImage(file = "images/background.gif")
    platformImage = PhotoImage(file = "images/plat.png")
    charImage = PhotoImage(file = "images/character.png")
    bonusImage = [0, 0, 0]
    bonusImage[0] = PhotoImage(file = "images/bonus1.png")
    bonusImage[1] = PhotoImage(file = "images/bonus2.png")
    bonusImage[2] = PhotoImage(file = "images/bonus3.png")
    

    #frame and duration settings
    #this should be equal to the average run time of 
    frameGap = 0.02
    frameRate = 1 / frameGap


    #initialization velocities
    terrainHeight = 204
    horEnvDisplace =  - 1920 / (screenRate * frameRate)
    horEnvDisplaceAbs = 1920 / (screenRate * frameRate)



    #background creation
    createbgImage = canvasMGI.create_image(0, 0, image = bgImage, anchor = NW)


    #one time calculation for platform moving
    platInScreen = math.ceil((1920 + 150) / 125)
    platHorCount = -1
    platVerChar = [0, 1]
    levelVerPos = [870, 666, 462, 258]
    horVelo = 1920 / screenRate
    platformPassFreq = 125 / horVelo
    platformHorMax = math.floor(endTime / platformPassFreq)
    platMoveCheckMax = platformHorMax - platInScreen
    forwardMostPlatInScreen = 0
    stopGenBeforeEnd = 2 * platformPassFreq
    blankTime = endTime - platformPassFreq
    platStopGen = platformHorMax - platInScreen

    
    
    #platform initialization and randomization. [x][y][z] x = platform horizontal locater, y = platform level, z:0 = ID, 1 = probability allows or no, 2 = whether there is a platform or no, 3 = probability, 4 = probability reset timer
    #platforms are generated outside of the screen. They will start moving at the appropriate time and end moving once they are out of the screen again
    createPlatformImage = [[[0 for i in range (3)] for j in range (3)] for n in range (platformHorMax)]
        
    platformRoll = [0, 0, 0]
    platformProb = [80, 80, 80]
    platformCD = [0, 0, 0]


    for i in range (1, platStopGen):

        for j in range (3):
            platformCD[j] -= 1
            if platformCD[j] == 0:
                platformProb[j] = 80
            if createPlatformImage[i - 1][j][2] == 1:
                platformProb[j] -= 50 / (1 / 3 * (120 / 6))
                
            
        for j in range (3):
            platformRoll[j] = random.randint(1, 100)
            if platformRoll[j] <= platformProb[j]:
                createPlatformImage[i][j][1] = 1
                createPlatformImage[i][j][2] = 1
             
            
        if createPlatformImage[i - 1][1][2] == 1 and createPlatformImage[i][2][1] == 1:
            createPlatformImage[i][2][2] = 1
            if createPlatformImage[i - 1][1][2] == 0:
                platformCD[1] = 0
                platformProb[1] = 80
                
        if createPlatformImage[i - 1][0][2] == 1 and createPlatformImage[i][0][2] == 0:
            createPlatformImage[i - 1][1][2] == 0
            
        if createPlatformImage[i - 1][0][2] == 0 and createPlatformImage[i][0][2] == 1:
            createPlatformImage[i - 1][1][2] == 0
        for j in range (3):
            if createPlatformImage[i - 1][j][2] == 1 and createPlatformImage[i][j][2] == 0:
                if j == 1:
                    platformCD[j] = math.floor(1 / 6 * (120 / 6))
                else:
                    platformCD[j] = math.floor(1 / 3 * (120 / 6))
                platformProb[j] = 0
                

    bonusProb = [90, 90, 90]
    bonusGenCD = [0, 0, 0]
    bonusRoll = [0, 0, 0]
    bonusForceGen = True

    createBonusImage = [[[0 for i in range (3)] for j in range (3)] for n in range (platformHorMax)]
    
    
    #platform generation and bonus randomization and generation || createBonusImage[][][0] is ID, 1 is if there is or not.
    #bonus follow the same moving rule as platform


    for i in range (platformHorMax):
        for j in range (3):
            if createPlatformImage[i][j][2] == 1:
                if i > 0 and createPlatformImage[i - 1][j][2] == 0:
                    bonusProb[j] = 90
                    bonusGenCD[j] = 0
                    
                createPlatformImage[i][j][0] = canvasMGI.create_image(1920, 666 - j * 204, image = platformImage, anchor = NW)
                bonusRoll[j] = random.randint(0, 99)
                if (bonusRoll[j] < bonusProb[j] or bonusForceGen == True) and bonusGenCD[j] == 0:
                    createBonusImage[i][j][1] = 1
                    createBonusImage[i][j][2] = 1
                    createBonusImage[i][j][0] = canvasMGI.create_image(1952.5, 666 - j * 204, image = bonusImage[j], anchor = SW)
                    bonusProb[j] -= 10
                    bonusForceGen = False
                elif bonusGenCD[j] == 0:
                    bonusGenCD[j] = 3
                    bonusProb[j] = 90
                elif bonusGenCD[j] > 0:
                    bonusGenCD[j] -= 1
                    bonusForceGen = True
                    

    #terrain creation: 1 = ID 2 = difference of x coordinate of terrain image object to x coordinate 3840
    createTerrainImage = [[0 for i in range(2)] for j in range(2)]
    createTerrainImage[0][0] = canvasMGI.create_image(0, 870, image = terrainImage, anchor = N)
    createTerrainImage[1][0] = canvasMGI.create_image(3820, 870, image = terrainImage, anchor = N)
    createTerrainImage[0][1] = 3840
    createTerrainImage[1][1] = 0

    #initializing variables for checking character imapct on object
    platformTravelTimeFront = (1920 - 252 - 86) / horVelo
    startPlatImpactCheck = False
    platFrontTimer = platformTravelTimeFront
    platRearTimer = platFrontTimer + platformPassFreq
    platCheck = [0 , 0]

    #initializing variables for checking character acquisition of bonus
    bonusTravelTimeFront = (1920 - 252 - 86 - 32.5) / horVelo
    startBonusImpactCheck = False
    bonusFrontTimer = bonusTravelTimeFront
    bonusRearTimer = bonusFrontTimer + (86 + 60) / horVelo
    bonusCheck = [0 , 0]
    bonusAcquired = [0, 0, 0]



    #create character
    spaceCounter = 0
    spaceIniTime = time.time()
    spaceTime = time.time()

    #the movement parameters for the character. They vary based on the difficulty level
    charIniVelo = - 2533
    acceleration = 6000 + 9000 / screenRate
    charVelo = 0
    charDisplace = 0

    charHorPos = 252
    createChar = canvasMGI.create_image(charHorPos, 870, image = charImage, anchor = SW)

    #character control initialization
    spacePressed = False
    lastSpacePressed = True
    charInAir = False
    charLevel = 0
    onLevel = True
    onFloor = True
    verDisplace = 0



    #initializie vertical movement
    checkVerContactStartTime = 0
    startCheck = (1920 - 252) / (1920 / screenRate)
    adjustVerPos = 0
    v0 = 0
    inAirType = 0


    #Objects categorization
    gameObjects = [0 for i in range (2 + 3 * platStopGen)]
    for i in range (platStopGen * 3):
        gameObjects[i] = createPlatformImage[i // 3][i % 3][0]
        
    for i in range (2):
        gameObjects[platStopGen * 3 + i] = createTerrainImage[i][0]


    gameImpactObjects = [0 for i in range (2 + 3 * platStopGen)]
    for i in range (platStopGen * 3):
        gameImpactObjects[i] = createPlatformImage[i // 3][i % 3][0]
        
    for i in range (2):
        gameImpactObjects[platStopGen * 3 + i] = createTerrainImage[i][0]


    #play the song
    winsound.PlaySound(songDirect, winsound.SND_ASYNC)
    
    #the movement velocity of background
    bgVelo = (4198 - 1920) / endTime
    
    #initializing variables of parameters for frame update 
    lastCurTime = time.time()

    firstCheck = True
    
    
    curTime = time.time() - frameGap
    iniTime = curTime
    timeDiff = time.time()
    accuTerrain = 0
    endTime = curTime + endTime
    nextPlatTime = curTime + platformPassFreq
    timeLapse = endTime - iniTime

    checkVerContactStartTime = iniTime + startCheck
    canvasMGI.pack()
    canvasMGI.update()
    platCounter = 0
    platEndCheck = curTime + blankTime

    #main game process-------------------------------------------------------
    
    while curTime <= endTime:
        #frame update -- recorde time

        #background move
        bgDisplace =  - bgVelo * frameGap
        canvasMGI.move(createbgImage, bgDisplace, 0)
        
        #horizontal movement velocities
        horEnvDisplace = - frameGap * horVelo
        horEnvDisplaceAbs = frameGap * horVelo
        
        
        if createTerrainImage[0][1] >= 5760:
            canvasMGI.move(createTerrainImage[0][0], createTerrainImage[0][1], 0)
            createTerrainImage[0][1] = 0
        if createTerrainImage[1][1] >= 5760:
            canvasMGI.move(createTerrainImage[1][0], createTerrainImage[1][1], 0)
            createTerrainImage[1][1] = 0
        canvasMGI.move(createTerrainImage[0][0], horEnvDisplace, 0)
        canvasMGI.move(createTerrainImage[1][0], horEnvDisplace, 0)
        
        createTerrainImage[0][1] += horEnvDisplaceAbs
        createTerrainImage[1][1] += horEnvDisplaceAbs
        
        refreshTime = curTime + frameGap
        
        #platform and bonus horizontal movement. The movement of platforms that enter the screen off the designated platform entry times is compensated
        if curTime < platEndCheck:
            if curTime >= nextPlatTime:
                platCounter += 1
                newPlatHorDisplace = -(curTime - nextPlatTime) * horVelo
                nextPlatTime = nextPlatTime + platformPassFreq
                if platCounter < platInScreen - 1:
                    for j in range (3):
                        for i in range (0, platCounter):
                            if createPlatformImage[i][j][2] == 1:
                                canvasMGI.move(createPlatformImage[i][j][0], horEnvDisplace, 0)
                            if createBonusImage[i][j][1] == 1:
                                canvasMGI.move(createBonusImage[i][j][0], horEnvDisplace, 0)
                        if createPlatformImage[platCounter][j][2] == 1:
                            canvasMGI.move(createPlatformImage[platCounter][j][0], newPlatHorDisplace, levelVerPos[j + 1] - (666 - j * 204))
                        if createBonusImage[platCounter][j][1] == 1:
                            canvasMGI.move(createBonusImage[platCounter][j][0], newPlatHorDisplace, levelVerPos[j + 1] - (666 - j * 204))
                else:
                    for j in range (3):
                        for i in range (platCounter + 1 - platInScreen, platCounter):
                            if createPlatformImage[i][j][2] == 1:
                                canvasMGI.move(createPlatformImage[i][j][0], horEnvDisplace, 0)
                            if createBonusImage[i][j][1] == 1:
                                canvasMGI.move(createBonusImage[i][j][0], horEnvDisplace, 0)
                        if createPlatformImage[platCounter][j][2] == 1:
                            canvasMGI.move(createPlatformImage[platCounter][j][0], newPlatHorDisplace, levelVerPos[j + 1] - (666 - j * 204))
                        if createBonusImage[platCounter][j][1] == 1:
                            canvasMGI.move(createBonusImage[platCounter][j][0], newPlatHorDisplace, levelVerPos[j + 1] - (666 - j * 204))
            else:
                if platCounter < platInScreen - 1:
                    for i in range (0, platCounter + 1):
                        for j in range (3):
                            if createPlatformImage[i][j][2] == 1:
                                canvasMGI.move(createPlatformImage[i][j][0], horEnvDisplace, 0)
                            if createBonusImage[i][j][1] == 1:
                                canvasMGI.move(createBonusImage[i][j][0], horEnvDisplace, 0)
                else:
                    for i in range (platCounter + 1 - platInScreen, platCounter + 1):
                        for j in range (3):
                            if createPlatformImage[i][j][2] == 1:
                                canvasMGI.move(createPlatformImage[i][j][0], horEnvDisplace, 0)
                            if createBonusImage[i][j][1] == 1:
                                canvasMGI.move(createBonusImage[i][j][0], horEnvDisplace, 0)
        
        
        #tracking platform horizontally in concern for the impact checking
        if startPlatImpactCheck == False and curTime - iniTime >= platformTravelTimeFront:
            startPlatImpactCheck = True
            platFrontTimer = platformTravelTimeFront + iniTime + (86 / horVelo)
            platRearTimer = platFrontTimer + (86 / horVelo)

        
        if startPlatImpactCheck == True:
            if curTime >= platFrontTimer:
                platFrontTimer = (curTime + platformPassFreq - (curTime - platFrontTimer))
                platCheck[0] += 1
            if curTime >= platRearTimer:
                platRearTimer = (curTime + platformPassFreq - (curTime - platRearTimer))
                platCheck[1] += 1
            
        #tracking bonus horizontally in concern for the impact checking
        if startBonusImpactCheck == False and curTime - iniTime >= bonusTravelTimeFront:
            startBonusImpactCheck = True
            bonusFrontTimer = bonusTravelTimeFront + iniTime + (125 / horVelo) + (86 / horVelo) #to allow the list to start with 0
            bonusRearTimer = bonusRearTimer + iniTime

        
        if startBonusImpactCheck == True:
            if curTime >= bonusFrontTimer:
                bonusFrontTimer = (curTime + platformPassFreq - (curTime - bonusFrontTimer))
                bonusCheck[0] += 1
            if curTime >= bonusRearTimer:
                bonusRearTimer = (curTime + platformPassFreq - (curTime - bonusRearTimer))
                bonusCheck[1] += 1
        
        
        
        
        
        #non artificial in air check (falling off from platform)
        onLevel = False
        charInAir = True
        i = 0
        while i < 4 and onLevel == False and charInAir == True:
            if levelVerPos[i] == 870:
                onLevel = True
                
                #platform in air check
                if i > 0:
                    x = 0
                    charInAir = True
                    while x < 2 and charInAir == True:
                        if createPlatformImage[platCheck[x]][i - 1][2] == 1:
                            charInAir = False
                        x += 1
                else:
                    charInAir = False
            i += 1
        
        
        #functions controlling the movement of user input and character. The character will jump higher when the space key is pressed down longer. The accumulated jump energy will be released if the character reaches the edge of a platform even if the space key isn't released
        lastSpacePressed = spacePressed
        charHorPos = (canvasMGI.coords(createChar)[0])  
        if keyboard.is_pressed('space') and charInAir == False:
            
            spacePressed = True
            if lastSpacePressed == False:
                charVelo = charIniVelo
            else:
                charVelo -= frameGap * (2 / screenRate) * 600
        else:
            spacePressed = False
            


        #the first condition to determine if the character is in air or not is to determine whether the space is released
        if spacePressed == False and lastSpacePressed == True:
            charInAir = True
        
        
        #objects vertical movement. If the character will land on to platforms, corrections of the movements will be made and the character will reenter the state of not in air              
        if charInAir == True:
            
            charVelo += acceleration * frameGap
            verDisplace =  - frameGap * charVelo
            
            #impactobject contact check (terrain and object)
            if startPlatImpactCheck == True:
                for i in range (6):
                    if createPlatformImage[platCheck[i // 3]][i // 2][2] == 1:
                        if levelVerPos[(i // 2) + 1] > 870 and levelVerPos[(i // 2) + 1] + verDisplace < 870:
                            charInAir = False
                            charVelo = 0
                            verDisplace = 870 - levelVerPos[(i // 2) + 1]
                    
                    
            if charInAir == True and levelVerPos[0] > 870 and levelVerPos[0] + verDisplace < 870:
                charInAir = False
                charVelo = 0
                verDisplace = 870 - levelVerPos[0]
            
            
            #moving terrain
            for i in range (2):
                canvasMGI.move(createTerrainImage[i][0], 0, verDisplace)
            
            #moving platforms
            if platCounter < platInScreen - 1:
                for i in range (0, platCounter + 1):
                    for j in range (3):
                        if createPlatformImage[i][j][2] == 1:
                            canvasMGI.move(createPlatformImage[i][j][0], 0, verDisplace)
            else:
                for i in range (platCounter + 1 - platInScreen, platCounter + 1):
                    for j in range (3):
                        if createPlatformImage[i][j][2] == 1:
                            canvasMGI.move(createPlatformImage[i][j][0], 0, verDisplace)
                            

            
            #moving bonus
            if platCounter < platInScreen - 1:
                for i in range (0, platCounter + 1):
                    for j in range (3):
                        if createBonusImage[i][j][1] == 1:
                            canvasMGI.move(createBonusImage[i][j][0], 0, verDisplace)
            else:
                for i in range (platCounter + 1 - platInScreen, platCounter + 1):
                    for j in range (3):
                        if createBonusImage[i][j][1] == 1:
                            canvasMGI.move(createBonusImage[i][j][0], 0, verDisplace)
            
            

            #update position
            for i in range (4):
                levelVerPos[i] += verDisplace
        
        
        #check if the character is in contact with the bonus
        if startBonusImpactCheck == True:
            for i in range (6):
                if createBonusImage[bonusCheck[i // 3]][i // 2][2] == 1:
                    if levelVerPos[(i // 2) + 1] + verDisplace >= 726 and levelVerPos[(i // 2) + 1] + verDisplace <= 930:
                        createBonusImage[bonusCheck[i // 3]][i // 2][2] = 0
                        bonusAcquired[i // 2] += 1
                        canvasMGI.itemconfig(createBonusImage[bonusCheck[i // 3]][i // 2][0], state = HIDDEN)
        

        canvasMGI.update()
        
        verDisplace = 0
        #first frame correction and update framerate
        lastCurTime = time.time()
        if firstCheck == True:
            firstCheck = False
            frameGap = lastCurTime - curTime - frameGap
        else:
            frameGap = lastCurTime - curTime
        curTime = lastCurTime
        
        #end of cycle
        
    #the program goes to the endGame canvas
    endGame(bonusAcquired, user, userDirect, userStorage, songImageDirect)
    
    #main game functions end here------------------------------------------------------
    
#MAIN GAME FUNCTION DEFINITIONS END HERE -----------------------------------------------------------------



#END GAME FUNCTION DEFINITIONS BEGIN HERE-----------------------------------------------------------

#the canvas displays the user earning and records them into the user profile; prompt the user to continue into mainUI
def endGame(bonuses, user, userDirect, userStorage, songImageDirect):
    global canvasMGI
    global endGameFrame
    global userData
    global endGameCanvasImage
    global songImage
    
    #Bonuses added to the user storage
    for i in range (bonuses[0]):
        userStorage += 20
    for i in range (bonuses[1]):
        userStorage += 15
    for i in range (bonuses[2]):
        userStorage += 25
    
    
    userDirect = 'users/' + user + '.txt'
    userData = openReadFile(userDirect)
    userData[1] = str(userStorage)
    
    #recording the new profile 
    openWriteFile(userDirect, userData)
    
    
    canvasMGI.destroy()
    
    endGameCanvasImage = PhotoImage(file = 'images/endGameCanvasimage.png')
    
    endGameFrame = Frame(root, height = 1080, width = 1920)
    endGameCanvas = Canvas(endGameFrame, height = 1080, width = 1920, bg = 'Red')
    endGameCanvas.create_image(0, 0, anchor = NW, image = endGameCanvasImage)
    
    #user earning displayed here
    endGameCanvas.create_text(1344, 270, text = 'YOU EARNED', fill = 'White', font = 'Verdana 20')
    statusBonusimg = [0 for i in range (3)]
    statusBonustxt = [0 for i in range (3)]
    for i in range (3):
        endGameCanvas.create_image(1267, 505 + i * 90, image = bonusImage[i], anchor = W)
        endGameCanvas.create_text(1357, 505 + i * 90, text = str(bonuses[i]), fill = 'White', font = 'Verdana 15', anchor = W)

    #upon pressing, the program goes back to the main UI
    continueButton = Button(endGameFrame, text = 'CONTINUE', command = lambda: createMainUI(user, userDirect, endGameFrame))
    
    songImage = PhotoImage(file = songImageDirect)
    songImageCreate = Label(endGameCanvas, image = songImage)
    songImageCreate.place(x = 0, y = 0, anchor = NW)
    
    endGameCanvas.pack()
    continueButton.place(y = 880, x = 1344, anchor = CENTER)
    
    endGameFrame.pack()
    
#END GAME FUNCTION DEFINITIONS END HERE ------------------------------------------------------------


#LOGIN SCREEN UNCHANGING PART-----------------------------------------------------------------------


#loading files
loginButtonImage = PhotoImage(file = 'images/loginButton.png')
LOGINLImage = PhotoImage(file = 'images/LOGINLimage.png')
LOGINRTImage = PhotoImage(file = 'images/LOGINRTimage.png')


#config data which records user amount and song amount
config = openReadFile('config/config.txt')

userAmount = int(config[1])

#user account data
users = openReadFile('users/users.txt')

frameLOGIN = Frame(root, height = 1080, width = 1920)

canvasLOGINL = Canvas(frameLOGIN, bg = 'Blue', height = 1080, width = 960)
canvasLOGINRT = Canvas(frameLOGIN, bg = 'Green', height = 270, width = 960)

#canvasLOGIN left
#loginText = canvasLOGINL.create_text(480, 270, anchor = S, text = "LOCAL\n\tLOGIN", font = "Verdana 30")
createLOGINLImage = canvasLOGINL.create_image(0, 0, anchor = NW, image = LOGINLImage)

#canvasLOGIN top right

createLOGINRTImage = canvasLOGINRT.create_image(0, 0, anchor = NW, image = LOGINRTImage)
userText = canvasLOGINRT.create_text(864, 220, anchor = E, text = "USER", font = "Verdana 30")
canvasLOGINRT.create_line(924, 20, 924, 250, fill = 'Yellow')
addLoginButton = Button(canvasLOGINRT, image = loginButtonImage, bg = 'White')
addLoginButton.place(anchor = E, x = 864, y = 135)


canvasLOGINL.grid(row = 0, column = 0, rowspan = 2, sticky = NW)
canvasLOGINRT.grid(row = 0, column = 1, columnspan = 2, sticky = NW)
userSelect()

#uppon clicking this button, the program will start user creation process
addLoginButton.config(command = userCreate)

frameLOGIN.pack()

#LOGIN SCREEN UNCHANGING PART------------------------------------------------------------------------


mainloop()