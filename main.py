# Coded using Anaconda3(Python 3.5.2) and pygame

import pygame
import copy
import random

#static variables, ugly
lastTime = False

def main():

    #intitialize pygame
    pygame.init()

    #game variables
    width = 1000
    height = 700

    black = ( 0, 0, 0 )
    white = ( 255, 255, 255 )
    red = ( 255, 0, 0 )

    #the terrain array
    terrain = createArray( width, height )

    #the player
    player = ( 505, 355 )

    #movement variables
    moveleft = False
    moveright = False
    moveup = False
    movedown = False

    # Framerate
    clock = pygame.time.Clock()
    fps = 15
    framecount = 0

    # Screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("MazeGameGenerationTest001")

    gameExit = False

    while not gameExit:

        #player x, y
        x = (player[0] - 5) // 10
        y = (player[1] - 5) // 10

        # Event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    moveleft = True
                elif event.key == pygame.K_RIGHT:
                    moveright = True
                elif event.key == pygame.K_UP:
                    moveup = True
                elif event.key == pygame.K_DOWN:
                    movedown = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    moveleft = False
                elif event.key == pygame.K_RIGHT:
                    moveright = False
                elif event.key == pygame.K_UP:
                    moveup = False
                elif event.key == pygame.K_DOWN:
                    movedown = False
        
        if framecount >= 10:
            #shift the terrain down
            terrain = shiftArray( terrain )

            #shift the player down
            player = ( player[0] - 10, player[1] )

            #create the new layer of terrain
            terrain = addNewColumn( terrain )
            
            framecount = 0

        #move the player
        if moveleft and terrain[x-1][y] == 0:
            player = ( player[0] - 10, player[1] )
        elif moveright and terrain[x+1][y] == 0:
            player = ( player[0] + 10, player[1] )
        elif moveup and terrain[x][(y-1)%len(terrain[0])] == 0:
            player = ( player[0], (player[1] - 10) % height )
        elif movedown and terrain[x][(y+1)%len(terrain[0])] == 0:
            player = ( player[0], (player[1] + 10) % height )

        #draw the terrain
        for i in range( len( terrain ) ):
            for j in range( len( terrain[0] ) ):
                rect = ( i*10, j*10, 10, 10 )
                if terrain[i][j]:
                    screen.fill( white, rect )
                else:
                    screen.fill( black, rect )

	#draw the player
        pygame.draw.circle( screen, red, player, 5, 0 )

        # Update the screen
        pygame.display.update()

        # Set the fps
        clock.tick(fps)

        framecount += 1

def createArray( width, height ):
    #creates the initial terrain for the game
    cArray = []
    for i in range( width // 10 ):
        column = []
        for j in range( height // 10 ):
            if j == 35:
                column.append( 0 )
            else:
                column.append( 1 )
        cArray.append( column )

    return cArray

def shiftArray( inputArray ):
    #takes in a 2d array where the inner lists are columns and shifts them to the left one, looping around

    temp = copy.deepcopy( inputArray[0] )
    for i in range( 1, len(inputArray) ):
        inputArray[i-1] = copy.deepcopy( inputArray[i] )
    inputArray[-1] = temp

    return inputArray

def addNewColumn( inputArray ):
    #adds a new column to the end of the array
    #this is the part we want to modify

    global lastTime

    newCol = []
    for i in range( len( inputArray[-2] ) ):
        newCol.append( 1 )
    l = len( newCol )
    pathPos = []
    for i in range(len(newCol)):
        if inputArray[-2][i] == 0 and ( inputArray[-3][i] + inputArray[-2][(i-1)%l] + inputArray[-2][(i+1)%l] == 2 ):
            pathPos.append(i)
            newCol[i] = 0

    #for each spot where the path must continue
    for pos in pathPos:
        chance = random.random()
        #random chance that the path will continue straight or turn, this should not occure if the previous run was a turn
        if chance < 0.1 and not lastTime:
            length = int( random.random() * len( newCol ) / 2 )
            #random chance that it goes down or up
            if chance < 0.05:
                for j in range( 0, length, 1 ):
                    newCol[(pos+j)%l] = 0
            else:
                for j in range( 0, -length, -1 ):
                    newCol[(pos+j)%l] = 0
            lastTime = True
        else:
            lastTime = False

    inputArray[-1] = newCol

    return inputArray

# Main Program
if __name__ == "__main__":
    main(  )