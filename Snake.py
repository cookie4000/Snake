import pygame
import sys
import random
from pygame.math import Vector2
from pygame import mixer

cellSize = 40
cellNumber = 20

class Cookie:
    def __init__(self):
        self.x = random.randint(0,cellNumber-1) #-1 is so you are always on the screen
        self.y = random.randint(0,cellNumber-1)
        self.pos = Vector2(self.x,self.y)
        
    
    def drawCookie(self):

        # Create a Rectangle
        cookieRec = pygame.Rect(self.pos.x * cellSize,self.pos.y * cellSize,cellSize,cellSize)
        # Draw Rectangle
        screen.blit(cookie,cookieRec)


    def reposition(self):
        self.x = random.randint(0,cellNumber-1) #-1 is so you are always on the screen
        self.y = random.randint(0,cellNumber-1)
        self.pos = Vector2(self.x,self.y)
        
class Snake:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.newBlock = False
        self.score = 0
        self.eatSound = pygame.mixer.Sound('audio/eat.wav')
        self.bumpSound = pygame.mixer.Sound('audio/bump.wav')
        
        # Load Graphics
        self.head_up = pygame.image.load('graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('graphics/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('graphics/body_bl.png').convert_alpha()

        # Starting positions
        self.head= self.head_right
        self.tail= self.tail_right
    
    def draw_snake(self):
    
        self.updateHeadGraphics()
        self.updateTailGraphics()
        
        # loop through all snake blocks knowing our index
        for index,block in enumerate(self.body):
            
            # Rectangle for positioning
            xPos = block.x*cellSize
            yPos = block.y*cellSize
            blockRec = pygame.Rect(xPos,yPos,cellSize,cellSize)
            
            # 2. what direction is the snake looking
            if index==0:
                screen.blit(self.head,blockRec)

            # Tail
            elif index == len(self.body) -1: 
                screen.blit(self.tail,blockRec)

            else: 
                # Subtrack vectors to see the relationships in the midle of the
                # snake
                previousBlock = self.body[index+1] - block
                nextBlock = self.body[index-1] - block

                # are you in a vertical position
                if previousBlock.x == nextBlock.x:
                    screen.blit(self.body_vertical,blockRec)
                # are you horizontal 
                elif previousBlock.y == nextBlock.y:
                    screen.blit(self.body_horizontal,blockRec)
                # corners
                else: 
                    
                    # check x and y of both the previous and 
                    # next block
                    if previousBlock.x == -1 and nextBlock.y == -1 or previousBlock.y== -1 and nextBlock.x==-1:
                        screen.blit(self.body_tl,blockRec)
                    elif previousBlock.x == -1 and nextBlock.y == 1 or previousBlock.y== 1 and nextBlock.x==-1:
                        screen.blit(self.body_bl,blockRec)
                    elif previousBlock.x == 1 and nextBlock.y == -1 or previousBlock.y== -1 and nextBlock.x==1:
                        screen.blit(self.body_tr,blockRec)
                    elif previousBlock.x == 1 and nextBlock.y == 1 or previousBlock.y== 1 and nextBlock.x==1:
                        screen.blit(self.body_br,blockRec)
    
    def moveSnake(self):
        if self.newBlock == True:
            # Don't remove the head - just add a piece
            copyOfBody = self.body[:]
            copyOfBody.insert(0,copyOfBody[0] + self.direction)

        else: 
            # Copy the body removing the last item
            copyOfBody = self.body[:-1]
            # Add new piece to the list in the direction of travel
            copyOfBody.insert(0,copyOfBody[0] + self.direction) # add a new item to the list based on direction
        self.body=copyOfBody[:]
        self.newBlock = False

    def growSnake(self):
        self.newBlock = True
        self.score+=1
        self.eatSound.play()
    
    def updateHeadGraphics(self):
        # subtrack one vector from another and from the result
        # you get something symbolisng direction
        
        headPositionRelation = self.body[1]- self.body[0]
        
        # head facing left
        if headPositionRelation == Vector2(1,0): self.head = self.head_left
        # head facing left
        elif headPositionRelation == Vector2(-1,0): self.head = self.head_right
        # head facing up
        elif headPositionRelation == Vector2(0,1): self.head = self.head_up
        # head facing down
        elif headPositionRelation == Vector2(0,-1): self.head = self.head_down
       
    def updateTailGraphics(self):
        # subtrack one vector from another and from the result
        # you get something symbolisng direction
        
        tailPositionRelation = self.body[-2] - self.body[-1]
        
        # tail facing left
        if tailPositionRelation == Vector2(1,0): self.tail = self.tail_left
        # tail facing left
        elif tailPositionRelation == Vector2(-1,0): self.tail = self.tail_right
        # tail facing up
        elif tailPositionRelation == Vector2(0,1): self.tail = self.tail_up
        # tail facing down
        elif tailPositionRelation == Vector2(0,-1): self.tail = self.tail_down



class Main:

    def __init__(self):
        self.snake = Snake()
        self.cookie = Cookie()
        self.gameActive = True


    def update(self):
        self.snake.moveSnake()
        self.checkCollision()
        self.checkFail()

    def drawElements(self):
        self.cookie.drawCookie()
        self.snake.draw_snake()
    
    def checkCollision(self):
        # is the head of the snake the same as the cookie
        if self.cookie.pos == self.snake.body[0]:
           # Move the cookie
           self.cookie.reposition() 
           # Add a block to the snake
           self.snake.growSnake()


    def checkFail(self):
        # are you out the screen
        # if the head is not between 0 and the number of cells
        if not 0 <= self.snake.body[0].x < cellNumber or not 0 <= self.snake.body[0].y < cellNumber:
                self.setGameOver()
                
        
        # have you hit yourself (is the head of the snake in any of its parts)
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.setGameOver()

    def setGameOver(self):
            self.snake.bumpSound.play()
            self.gameActive = False

    def resetGame(self): 
        self.gameActive = True
        self.snake = Snake()
        self.cookie = Cookie()
    
    def displayGameOver(self):

        screen.fill((175,215,70))
        # Write the text for Game Over
        font = pygame.font.SysFont(None, 35)
        smallFont = pygame.font.SysFont(None, 20)
        gameOver = font.render('Game Over', True, 'blue')
        score = font.render('Score: ' + str(mainGame.snake.score), True, 'blue')
        restart = smallFont.render('Press Esc to Restart', True, 'blue')

        # we want to centre the text so we need the midpoint of the screen. 
        screenMid = screen.get_rect().centerx
        padding = 5
        # we divide the width of the messages by 2 to centre them
        gameOverRec = pygame.Rect(screenMid- gameOver.get_width()/2,screen.get_rect().centery,cellSize,cellSize)
        scoreRec = pygame.Rect(screenMid - score.get_width()/2,gameOverRec.centery + padding,cellSize,cellSize)
        restartRec = pygame.Rect(screenMid - restart.get_width()/2,scoreRec.centery + padding,cellSize,cellSize)

        # Display the messages 
        screen.blit(gameOver,gameOverRec)
        screen.blit(score, scoreRec)
        screen.blit(restart, restartRec)


# bring in py game assets and set size
pygame.mixer.init()
pygame.init()


# 800*800 screen
screen = pygame.display.set_mode((cellNumber*cellSize,cellNumber*cellSize))

# Create a Clock object to regulate time in the game
clock = pygame.time.Clock()
framerate=60

# Set logo and caption on window
pygame.display.set_caption("Snake by Cookie Codes")
cookie = pygame.image.load('graphics/cookie.png').convert_alpha()
pygame.display.set_icon(cookie)


# Create an even to trigget ever 150ms
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

mainGame = Main()

while True:
    # Check for all possible events
    for event in pygame.event.get():
        
        # Handle quit event
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
        
        # if the game is over
        if mainGame.gameActive == False:
            
            # we arent to restart
            restart = False

            # until the user presses esc
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    restart = True
            
            if restart== False and mainGame.gameActive==False:
                mainGame.displayGameOver()
            else: 
                # reset everything
                restart = True
                mainGame.resetGame()
        else: 
            if event.type == SCREEN_UPDATE:
                mainGame.update()
            if event.type == pygame.KEYDOWN:

                # Stop the snake going into itself
                # if we are moving down dont move up etc..
                if event.key == pygame.K_UP:
                    if mainGame.snake.direction.y != 1:
                        mainGame.snake.direction = Vector2(0,-1)
                if event.key == pygame.K_DOWN:
                    if mainGame.snake.direction.y != -1:
                        mainGame.snake.direction = Vector2(0,1)
                if event.key == pygame.K_LEFT:
                    if mainGame.snake.direction.x != 1:
                        mainGame.snake.direction = Vector2(-1,0)
                if event.key == pygame.K_RIGHT:
                    if mainGame.snake.direction.x != -1:
                        mainGame.snake.direction = Vector2(1,0)
            
            screen.fill((175,215,70))
            mainGame.drawElements()
    
    # Update Display
    pygame.display.update()
    clock.tick(framerate)
