import time, pygame
pygame.init()
WIDTH, HEIGHT = 2200, 1100
BGCOLOR = 255, 255, 255
black = 0, 0, 0
pygame.display.set_caption("ToolBox")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

spriteList = []
buttonList = []


def fillBG():
    """
    fill background with background color
    """
    screen.fill(BGCOLOR)



class Sprite:
    global spriteList
    def __init__(self, coords = (0,0), visible = False, texture = "BlackCircle.png", size = (-1,-1), isButton = False, shape = "circle", onClick = lambda : print("clicked !")):
        spriteList.append(self)
        self.coords = coords
        self.visible = visible
        if size == (-1,-1): #if default values
            self.size = (pygame.image.load(texture)).get_rect().size
        else :
            self.size = size
        self.textureName = texture
        self.texture = pygame.transform.scale(pygame.image.load(texture), size)
        self.rect = (self.texture).get_rect()

        self.coordPredictions = {} #a dictionnary where the path for animations will be stored
        self.sizePredictions = {} #a dictionnary where the size for animations will be stored

        self.isButton = isButton
        self.shape = shape

        self.onClick = onClick

        self.released = True #pour éviter qu'un bouton soit cliquer pleins de fois à la suite

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

    def clickChecker(self, mouseCoords):
        """
        Checks if the mouse is clicking on the sprite and activates the onClick function in that case
        """
        clicked = False
        if self.isButton and self.released:
            if self.shape == "circle":
                if ((self.center()[0]-mouseCoords[0])**2 + (self.center()[1]-mouseCoords[1])**2)**0.5 < self.size[0]/2:
                    clicked = True
            if self.shape == "rectangle":
                if mouseCoords[0] >= self.middleLeft[0] and mouseCoords[0] <= self.middleRight[0] and mouseCoords[1] >= self.middleTop[1] and mouseCoords[1] <= self.middleBottom[1]:
                    clicked = True
            if clicked:
                self.released = False
                self.onClick()


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

def clickingBuisiness():
    """
    Does all the checks and updates related to clicking a sprite
    """
    global mouseIsClicked, mousePosition
    if mouseIsClicked:
        for sprite in spriteList:
            sprite.clickChecker(mousePosition)
    else:
        for sprite in spriteList:
            sprite.released = True

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
        testBall = Sprite((300,300), True, size = (100,100), isButton = True)
        print("did a thing")
        testBall.smoothSlideThird((600,600), slideFrameAmount = 40)
        testBall.resizeSlide((200,200), slideFrameAmount = 60)
        #testBall.resize((200,200))
        print("lol")


    if frameCount == 200:
        #testBall.resizeSlide((200,200), slideFrameAmount = 60)
        #testBall.teleport((600,600))
        #testBall.onClick()
        print("other thing")
    print(frameCount)
    refreshSprites() 
    clickingBuisiness

    pygame.display.flip()
    time.sleep(1/60)
    frameCount += 1
