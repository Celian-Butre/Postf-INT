"""
À faire :  
    mettre du delay sur slide et resize
    à mettre de l'idle animation
"""


import time, pygame
pygame.init()
WIDTH, HEIGHT = 2200, 1100
BGCOLOR = 255, 255, 255
black = 0, 0, 0
pygame.display.set_caption("ToolBox")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

spriteList = []
buttonList = []

exampleAnimation = [["testDogFrames/dog_astropad-0.png", 5],["testDogFrames/dog_astropad-1.png", 5],["testDogFrames/dog_astropad-2.png", 5],["testDogFrames/dog_astropad-3.png", 5],["testDogFrames/dog_astropad-4.png", 5],["testDogFrames/dog_astropad-5.png", 5],["testDogFrames/dog_astropad-6.png", 5],["testDogFrames/dog_astropad-7.png", 5],["testDogFrames/dog_astropad-8.png", 5],["testDogFrames/dog_astropad-9.png", 5],["testDogFrames/dog_astropad-10.png", 5],["testDogFrames/dog_astropad-11.png", 5],["testDogFrames/dog_astropad-12.png", 5],["testDogFrames/dog_astropad-13.png", 5],["testDogFrames/dog_astropad-14.png", 5],["testDogFrames/dog_astropad-15.png", 5],["testDogFrames/dog_astropad-16.png", 5],["testDogFrames/dog_astropad-17.png", 5],["testDogFrames/dog_astropad-18.png", 5],["testDogFrames/dog_astropad-19.png", 5],["testDogFrames/dog_astropad-20.png", 5]]

def fillBG():
    """
    fill background with background color
    """
    screen.fill(BGCOLOR)



class Sprite:
    global spriteList
    def __init__(self, coords = (0,0), visible = False, texture = "BlackCircle.png", size = (-1,-1), isButton = False, shape = "circle", onPress = lambda : print("pressed !"), onClick = lambda : print("clicked !")):
        spriteList.append(self)
        self.coords = coords
        self.visible = visible
        if size == (-1,-1): #if default values
            self.size = (pygame.image.load(texture)).get_rect().size
        else :
            self.size = size
        self.textureName = texture
        self.texture = pygame.transform.scale(pygame.image.load(self.textureName), self.size)
        self.rect = (self.texture).get_rect()

        self.coordPredictions = {} #a dictionnary where the path for animations will be stored
        self.sizePredictions = {} #a dictionnary where the size for animations will be stored
        self.skinPredictions = {} #a dictionnary where the image for animations of the sprite will be stored

        self.isButton = isButton
        self.shape = shape

        self.onPress = onPress
        self.onClick = onClick

        self.notPressedDown = True #To make sur a buttons action doesn't happen every frame it is being pressed down
        self.released = True #To be able to do an action upon a click's release

    def center(self):
        """
        gives the coordinates of the center of the sprite
        """
        return((self.coords[0] + self.size[0]/2, self.coords[1] + self.size[1]/2))

    def topLeft(self):
        """
        gives the coordinates of the top left of the sprite
        """
        return((self.coords[0], self.coords[1]))

    def topRight(self):
        """
        gives the coordinates of the top right of the sprite
        """
        return((self.coords[0] + self.size[0], self.coords[1]))

    def bottomRight(self):
        """
        gives the coordinates of the bottom right of the sprite
        """
        return((self.coords[0] + self.size[0], self.coords[1] + self.size[1]))
    
    def bottomLeft(self):
        """
        gives the coordinates of the bottom left of the sprite
        """
        return((self.coords[0], self.coords[0] + self.size[1]))

    def middleLeft(self):
        """
        gives the coordinates of the middle left of the sprite
        """
        return((self.coords[0], self.coords[1] + self.size[1]/2))

    def middleRight(self):
        """
        gives the coordinates of the middle right of the sprite
        """
        return((self.coords[0] + self.size[0], self.coords[1] + self.size[1]/2))

    def middleTop(self):
        """
        gives the coordinates of the middle top of the sprite
        """
        return((self.coords[0] + self.size[0]/2, self.coords[1]))
    
    def middleBottom(self):
        """
        gives the coordinates of the middle bottom of the sprite
        """
        return((self.coords[0] + self.size[0]/2, self.coords[0] + self.size[1]))


    def visibleize(self):
        """
        makes the sprite visible
        """
        self.visible = True

    def invisibleize(self):
        """
        makes the sprite invisible
        """
        self.visible = False

    def teleport(self, coords):
        """
        teleports the sprite to the designated location
        no animation or anything, just *POOF* 
        """
        self.coords = coords

    def resize(self, endsize):
        """
        resizes a sprites size
        """
        resizeDifference = (endsize[0] - self.size[0], endsize[1] - self.size[1])
        self.coords = (self.coords[0] - resizeDifference[0]/2, self.coords[1] - resizeDifference[1]/2)

        self.size = endsize
        self.texture = pygame.transform.scale(pygame.image.load(self.textureName), endsize)
        self.rect = (self.texture).get_rect()

    def resizeSlide(self, endsize, slideFrameAmount = 60):
        """
        resizes a sprites size progressively
        """
        global frameCount
        for i in range(slideFrameAmount+1):
            self.sizePredictions[str(i+frameCount)] = (self.size[0]+i*(endsize[0] - self.size[0])/slideFrameAmount, self.size[1]+i*(endsize[1] - self.size[1])/slideFrameAmount)
    

    def slide(self, endcoords, slideFrameAmount = 60):
        """
        prepares the path to slide the sprite from current coordinates to the endcoordinates
        """
        #print("hey")
        global frameCount
        for i in range(slideFrameAmount+1):
            self.coordPredictions[str(i+frameCount)] = (self.coords[0]+i*(endcoords[0] - self.coords[0])/slideFrameAmount, self.coords[1]+i*(endcoords[1] - self.coords[1])/slideFrameAmount)
    
    def smoothSlideFifth(self, endcoords, slideFrameAmount = 60):
        """
        same as slide except the animation is smoother with an acceleration phase and a deceleration phase
        acceleration and deceleration make up a fifth of the time
        """
        global frameCount
        t1 = int(slideFrameAmount/5)
        x1 = ((endcoords[0] - self.coords[0])/8, (endcoords[1] - self.coords[1])/8)
        v1 = ((endcoords[0] - self.coords[0])/(4*t1),(endcoords[1] - self.coords[1])/(4*t1))
        for i in range(t1+1):
            self.coordPredictions[str(i+frameCount)] = (self.coords[0] + x1[0]*(i/t1)**2, self.coords[1] + x1[1]*(i/t1)**2)
            self.coordPredictions[str(slideFrameAmount+frameCount - i)] = (endcoords[0] - x1[0]*(i/t1)**2, endcoords[1] - x1[1]*(i/t1)**2)
        for i in range(t1, 4*t1+1):
            self.coordPredictions[str(i+frameCount)] = ((i-t1)*v1[0]+self.coords[0] + x1[0],(i-t1)*v1[1]+self.coords[1] + x1[1])

    def smoothSlideThird(self, endcoords, slideFrameAmount = 60):
        """
        same as slide except the animation is smoother with an acceleration phase and a deceleration phase
        acceleration and deceleration make up a third of the time
        """
        global frameCount
        t1 = int(slideFrameAmount/3)
        x1 = ((endcoords[0] - self.coords[0])/4, (endcoords[1] - self.coords[1])/4)
        v1 = ((endcoords[0] - self.coords[0])/(2*t1),(endcoords[1] - self.coords[1])/(2*t1))
        for i in range(t1+1):
            self.coordPredictions[str(i+frameCount)] = (self.coords[0] + x1[0]*(i/t1)**2, self.coords[1] + x1[1]*(i/t1)**2)
            self.coordPredictions[str(slideFrameAmount+frameCount - i)] = (endcoords[0] - x1[0]*(i/t1)**2, endcoords[1] - x1[1]*(i/t1)**2)
        for i in range(t1, 2*t1+1):
            self.coordPredictions[str(i+frameCount)] = ((i-t1)*v1[0]+self.coords[0] + x1[0],(i-t1)*v1[1]+self.coords[1] + x1[1])

    def actualise(self):
        """
        keeps the sprite along the programmed path
        """
        global frameCount
        newcoords = self.coordPredictions.get(str(frameCount))
        if newcoords is not None:
            self.teleport(newcoords)
        newSize = self.sizePredictions.get(str(frameCount))
        if newSize is not None:
            self.resize(newSize)
        newTexture = self.skinPredictions.get(str(frameCount))
        if newTexture is not None:
            self.setSkin(newTexture)

    def pressChecker(self, mouseCoords):
        """
        (Prefer using clickChecker, but might come in use)
        Checks if the mouse pressed on the sprite and activates the onClick function in that case
        Activates as soon as the mouse is pressed, not released
        """
        pressed = False
        if self.isButton and self.notPressedDown:
            if self.shape == "circle":
                if ((self.center()[0]-mouseCoords[0])**2 + (self.center()[1]-mouseCoords[1])**2)**0.5 < self.size[0]/2:
                    pressed = True
            if self.shape == "rectangle":
                if mouseCoords[0] >= self.middleLeft[0] and mouseCoords[0] <= self.middleRight[0] and mouseCoords[1] >= self.middleTop[1] and mouseCoords[1] <= self.middleBottom[1]:
                    pressed = True
            if pressed:
                self.notPressedDown = False
                self.onPress()

    def clickChecker(self, mouseCoords, mousePressed):
        """
        Checks if the mouse clicked on the sprite and activates the onClick function in that case
        Activates when the mouse is released (and still above the hitbox)
        """
        if self.released and mousePressed: #If mouse has JUST been pressed
            correctPosition = False
            if self.isButton:
                if self.shape == "circle":
                    if ((self.center()[0]-mouseCoords[0])**2 + (self.center()[1]-mouseCoords[1])**2)**0.5 < self.size[0]/2:
                        correctPosition = True
                if self.shape == "rectangle":
                    if mouseCoords[0] >= self.middleLeft[0] and mouseCoords[0] <= self.middleRight[0] and mouseCoords[1] >= self.middleTop[1] and mouseCoords[1] <= self.middleBottom[1]:
                        correctPosition = True
                if correctPosition:
                    self.released = False
                    #self.onClick() #Click happens only upon correct release
        elif not self.released and not mousePressed: #if mouse has JUST been released
            correctPosition = False
            if self.isButton :
                if self.shape == "circle":
                    if ((self.center()[0]-mouseCoords[0])**2 + (self.center()[1]-mouseCoords[1])**2)**0.5 < self.size[0]/2:
                        correctPosition = True
                if self.shape == "rectangle":
                    if mouseCoords[0] >= self.middleLeft[0] and mouseCoords[0] <= self.middleRight[0] and mouseCoords[1] >= self.middleTop[1] and mouseCoords[1] <= self.middleBottom[1]:
                        correctPosition = True
                if correctPosition:
                    self.onClick()
                    
    def setSkin(self, newTexture):
        """
        sets new skin for sprite
        """
        self.textureName = newTexture
        self.texture = pygame.transform.scale(pygame.image.load(self.textureName), self.size)
        #self.rect = ((self.texture).get_rect()).move(self.coords[0], self.coords[1])


    def startAnimation(self, animationList, delay = 0):
        """
        prepares the skins needed for an animation (animationList is a list of lists with the format [["image1.png",timeImage1IsDisplayed],[["image2.png",timeImage2IsDisplayed]]])
        """
        global frameCount
        accumulator = delay + frameCount
        for texture in animationList:
            self.skinPredictions[str(accumulator)] = texture[0]
            accumulator += texture[1]


def refreshSprites():
    """
    Puts all the sprites where they are supposed to be
    """
    global spriteList
    fillBG()
    for sprite in spriteList:
        if sprite.visible :
            sprite.actualise() #play the animation if needed
            sprite.rect = sprite.rect.move(-1 * sprite.rect.x, -1 * sprite.rect.y)
            sprite.rect = sprite.rect.move(sprite.coords)
            screen.blit(sprite.texture, sprite.rect)

def pressingBuisiness():
    """
    Does all the checks and updates related to pressing a sprite (no release needed)
    """
    global mouseIsClicked, mousePosition
    if mouseIsClicked:
        for sprite in spriteList:
            sprite.pressChecker(mousePosition)
    else:
        for sprite in spriteList:
            sprite.notPressedDown = True

def clickingBuisiness():
    """
    Does all the checks and updates related to clicking a sprite (correct release needed)
    """
    global mouseIsClicked, mousePosition
    for sprite in spriteList:
        sprite.clickChecker(mousePosition, mouseIsClicked) #set to pressed or released depening on mouseIsClicked
    if not mouseIsClicked:
        for sprite in spriteList:
            sprite.released = True #release all once mouse is released

def clickNpress():
    pressingBuisiness()
    clickingBuisiness()

mouseIsClicked = False
mousePosition = (0,0)
frameCount = 0
while True: 
    mousePosition = pygame.mouse.get_pos()
    #print(mouseIsClicked)
    #print(mousePosition)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouseIsClicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                mouseIsClicked = False
    if frameCount == 0:
        testDog = Sprite((300,300), True, size = (116,100), texture = "testDogFrames/dog_astropad-0.png")
        testDog.startAnimation(exampleAnimation, delay = 200)
        #testBall = Sprite((300,300), True, size = (100,100), isButton = True)
        #print("did a thing")
        #testBall.smoothSlideThird((600,600), slideFrameAmount = 40)
        #testBall.resizeSlide((200,200), slideFrameAmount = 60)
        #testBall.resize((200,200))
        #print("lol")


    if frameCount == 200:
        pass
        #testBall.resizeSlide((200,200), slideFrameAmount = 60)
        #testBall.teleport((600,600))
        #testBall.onClick()
        #print("other thing")
    print(frameCount)
    refreshSprites() 
    clickNpress()

    pygame.display.flip()
    time.sleep(1/60)
    frameCount += 1
