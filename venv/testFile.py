import pygame



class Grid():
    def __init__(self,position_x,position_y,color):
        self.position_x = position_x
        self.position_y = position_y
        self.length = 5
        self.width = 5
        self.color = col


# https://www.pygame.org/docs/ref/mouse.html#comment_pygame_mouse_get_pressed


pygame.init()

# creating screen
screen = pygame.display.set_mode((800, 800))

drawingGrid = []

def initializeGrid():
    initialize_grid_x = 0
    initialize_grid_y = 0
    initialize_color = (0,0,0)
    for i in range(160):
        for j in range(160):
            drawingGrid.append((initialize_grid_x, initialize_grid_y, initialize_color))
            initialize_grid_y += 5
        initialize_grid_x += 5

initializeGrid()

print("Done")
#
# def drawGrid():
#     x = 0
#     y = 0
#     global drawingGrid
#     for i in range(500):
#         for j in range (500):
#             pygame.draw.rect(screen, (0,0,255), [x, y, 10, 10])  # 2 means not filled
#             y+=10
#         x+=10
#
#


def getGridPosition(mx,my):
    if mx%5==0 and my%5==0:
        return mx,my
    elif mx%5!=0 and my%5==0:
        return mx-(mx%5), my
    elif mx%5==0 and my%5!=0:
        return mx, my-(my%5)
    else:
        return mx-(mx%5), my-(my%5)


def updateGrid(mx,my):
    grid_index_x = mx/5
    grid_index_y = my/5



running = True
# Game loop
firstTime = True
mouseButtonPressed = False
while running:
    if firstTime:
        screen.fill((255, 255, 255))  # R G B This must always be at top or it will
        firstTime = False

    for event in pygame.event.get():  # this will capture every event that occurs
        if event.type == pygame.QUIT:  # when the cross button of top right of the
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseButtonPressed = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouseButtonPressed = False

    if mouseButtonPressed:
        mx, my = pygame.mouse.get_pos()
        mx, my = getGridPosition(mx, my)
        pygame.draw.rect(screen, (0, 0, 255), [mx, my, 5, 5])  # 2 means not filled

    if event.type == pygame.KEYDOWN:  # This is called whenever a key is pressed DOWN
        if event.key == pygame.K_SPACE:
            print("hi")


    pygame.display.update()



#    drawGrid()





#
#
# running = True
# # Game loop
# firstTime = True
# mouseButtonPressed = False
# while running:
#     if firstTime:
#         screen.fill((255, 255, 255))  # R G B This must always be at top or it will
#         firstTime = False
#
#     for event in pygame.event.get():  # this will capture every event that occurs
#         if event.type == pygame.QUIT:  # when the cross button of top right of the
#             running = False
#
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             mouseButtonPressed = True
#
#         if event.type == pygame.MOUSEBUTTONUP:
#             mouseButtonPressed = False
#
#     if mouseButtonPressed:
#         mx, my = pygame.mouse.get_pos()
#         pygame.draw.rect(screen, (0, 0, 255), [mx, my, 5, 5])  # 2 means not filled
#         print(mx, my)
#
#
#     pygame.display.update()
#
# #    drawGrid()
#
