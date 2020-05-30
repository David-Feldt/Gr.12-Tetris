

#Importing all neccessary modules
import pygame
import sys
import time
import random

#Initialzing pygame
pygame.init()

#block = 32 * 32
#w = 320
#h = 576

#Starting posistions for the grid (x,y coordinates)
top_left_x = 169
top_left_y = 45

#Inner block dimensions
block_size = 30

#Grid has 2 width of pixels to give look, (1 pixel outline on each block)
space_size = 32

#Dimensions for the mini "next block" section  
nxt_block_size = 20

#Gives outline like the grid for next block area
nxt_space_size = 22

#Dimensions for the screen
display_width = 748
display_height = 653

#Setting up our screen with screen dimensions
screen = pygame.display.set_mode((display_width,display_height))
#Creating a window caption that says "Tetris"
pygame.display.set_caption("Tetris")

#Picture Imports
t_menu = pygame.image.load("large_t_start.jpg")
g_menu = pygame.image.load("large_n_grid.jpg")
c_menu = pygame.image.load("large_t_controls.jpg")
g_over_menu = pygame.image.load("t_game_over.jpg")
p_menu = pygame.image.load("t_pause.jpg")
nxt_block = pygame.image.load("next_block_space.jpg")
hover_play = pygame.image.load("hover_t_play_button.jpg")
hover_controls = pygame.image.load("hover_t_controls_button.jpg")
hover_stats = pygame.image.load("hover_t_stats_button.jpg")
hover_cmenu_exit = pygame.image.load("hover_cmenu_exit.jpg")
hover_resume = pygame.image.load("resume_button.jpg")
hover_restart = pygame.image.load("restart_button.jpg")
hover_main_menu = pygame.image.load("mmenu_button.jpg")
hover_exit = pygame.image.load("quit_button.jpg")

#Colour Initialization
#Pygame is RGB, (Red, Gree, Blue) -> with values ranging from 0 - 255
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
orange = (255,127,0)
yellow = (255,255,0)
l_green = (0,255,0)
blue = (0,0,255)
l_blue = (0,255,255)
purple = (255,0,255)


#Shape Formats
"""
Shapes are lists of different rotations
Posistion blocks on grid are either filled "0" or empty "."
"""
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '...0.',
      '..00.',
      '..0..',
      '.....']]

I = [['..0..',
      '..0..',
      '..0.',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

#List of all the shapes^
shapes = [S,Z,I,O,J,L,T]
#List of shape colours that match with shape list^
shape_colours = [l_green,red,l_blue,yellow,blue,orange,purple]

#Fonts
smallFont = pygame.font.SysFont('Tetris.tff',25)
largeText = pygame.font.Font('Tetris.ttf',115)

#Each piece has x,y,shape,colour,and rotation value
class Piece(object):
  def __init__(self,x,y,shape):
    self.x = x
    self.y = y
    self.shape = shape
    self.colour = shape_colours[shapes.index(shape)]
    self.rotation = 0 #posistion in shape list


#Draw pictures onto our screen given image and x, y coordinates
def main_menu(x,y):
    screen.blit(t_menu,(x,y))

def game_grid(x,y):
    screen.blit(g_menu,(x,y))

def control_menu(x,y):
    screen.blit(c_menu,(x,y))

def pause_menu(x,y):
    screen.blit(p_menu,(x,y))
    
def game_over_menu(x,y):
    screen.blit(g_over_menu,(x,y))
    
def hover_play_button(x,y):
    screen.blit(hover_play,(x,y))

def hover_controls_button(x,y):
    screen.blit(hover_controls,(x,y))

def hover_stats_button(x,y):
    screen.blit(hover_stats,(x,y))

def hover_c_exit(x,y):
    screen.blit(hover_cmenu_exit,(x,y))

def hover_resume_button(x,y):
    screen.blit(hover_resume,(x,y))

def hover_restart_button(x,y):
    screen.blit(hover_restart,(x,y))

def hover_mmenu_button(x,y):
    screen.blit(hover_main_menu,(x,y))

def hover_exit_button(x,y):
    screen.blit(hover_exit,(x,y))

def next_block_space(x,y):
    screen.blit(nxt_block,(x,y))

#creates a matrix corisponding to the visual grid (all RGB colours)
def create_grid(locked_pos = {}):
#Creates dictionary with the locked blocks (key = coordinates in grid, value = colour)

#Creates a matrix of colours (all black, (0,0,0))
  grid = [[(0,0,0) for x in range(10)] for y in range(18)]

#Adds all the locked block colours into the grid 
  for i in range(18):
    for j in range(10):
      if (j,i) in locked_pos:
        temp = locked_pos[(j,i)] #temp is colour value from key
        grid[i][j] = temp #grid being manipulated 
  
  return grid
#end of create_grid()

#Takes shape posistions and formats them with x y coordinates used for grid 
def convert_shape_format(shape):
  positions = []
  format = shape.shape[shape.rotation % len(shape.shape)] #each letter rotation is a format for the given letter

  for i, line in enumerate(format): #Looking through the dots and zeros and numbers them
    row = list(line)
    for j, column in enumerate(row):
      if column == '0':
        positions.append((shape.x + j, shape.y + i)) #0's are block locations so they are formatted with x and y coordiantes to be usable (no one cares about . x,y coordinates only used to mold the shape)

  for i, pos in enumerate(positions):
    #38:40
    positions[i] = (pos[0] - 2, pos[1] - 4)

  return positions #posistions of blocks "0"'s now have x y coordinates and no more .'s
#end of convert_shape_format()

def valid_space(shape,grid):
  accepted_pos = [[(x,y) for x in range(10) if grid[y][x] == (0,0,0)] for y in range(18)] #Good posistions are blac (0,0,0)
  accepted_pos = [x for sub in accepted_pos for x in sub] #removes sub lists in previous lists [[(0,1),(2,3)]] --> [(0,1),(2,3)]

  formatted = convert_shape_format(shape) #posistions coordinates for blocks

#Makes sure all posistions have acceptable posisition by checking y coordinate below them
  for pos in formatted:
    if pos not in accepted_pos:
      if pos[1] > -1:
        return False
  return True #Means block can fall
#end of valid_space()

#Check if block some how is below the screen
def check_lost(positions):
  for pos in positions:
    x, y = pos
    if y < 1:
      return True
  
  return False
#end of check_lost()

#Randomizes piece selection 
def get_shape(shapes):
  return Piece(5,0,random.choice(shapes)) 
#end of get_shape()

#Code for clearing rows 
def clear_rows(grid, locked):
  inc = 0
  for i in range(len(grid)-1,-1,-1): #goes through row number
    row = grid[i]
    if (0,0,0) not in row: #If row is full with non blacks
      inc += 1 #increases for every complete row, determines how many rows to move down for each row clear
      ind = i #row needed to be cleared
      for j in range(len(row)): #run through each value in "ind" row to be cleared
        try: #similar to a True statement but parameters are functional running code 
          del locked[(j,i)] #deletes each block in row 
        except: #The else to the try statement
          continue
  if inc > 0: #1:10:00
    for key in sorted(list(locked), key = lambda x: x[1])[::-1]: #goes through the list backwards (bottom row to top row: prevents block overriding)
      x, y = key #Takes the x & y pos of each block in locked pos
      if y < ind: #only affects blocks above removed row
        newKey = (x, y + inc) #shifts down the rows above by adding # of cleared rows to it
        locked[newKey] = locked.pop(key) #adds a new row y value to dictionary of locked blocks 

  return inc #used for # of lines cleared for score 
#end of clear_rows()

#Code for mini shape that comes next
def draw_next_shape(shape, surface):

#setup for next block dimensions
  x = 480
  y = 100 
  format = shape.shape[shape.rotation % len(shape.shape)] #formats grid coordinates from shape posistion 

  for i, line in enumerate(format):
    row = list(line)
    for j, column in enumerate(row):
      if column == '0':
        pygame.draw.rect(surface,shape.colour,(x + j*nxt_space_size,y + i*nxt_space_size,nxt_block_size,nxt_block_size),0) #only draws shape for blocks in grid area 
#end of draw_next_shape()

#Draws a blocks based on grid of colours
"""
To draw a rect you need
- dimensions - preset from before
- y and x location -> block dimensions * block colour index
- colour -> got from colour grid
"""
def draw_window(surface, grid):
  for y in range(len(grid)):
    for x in range(len(grid[y])):
      pygame.draw.rect(surface,grid[y][x],(top_left_x + x*space_size,top_left_y + y*space_size,block_size,block_size))
#end of draw_window()

#Code for displaying text - Formatted for the score
def display_score(surface,x,y,score=0):
  font = pygame.font.Font('FreeSansBold.ttf',35)
  label = font.render(str(score),1,white)

  surface.blit(label,(x,y))
#end of display_score()


def pause2(): #pause loop function

#setup for loop
  paused = True
  pause_menu(0,0)
  pygame.display.update()

#start of actual loop
  while paused:
    for i in pygame.event.get(): #if the red x is clicked end the game
      if i.type == pygame.QUIT:
          pygame.quit()
          sys.exit()

#check mouse posistion
    mouse = pygame.mouse.get_pos()

    if 226 <= mouse[0] <= 525 and 188 <= mouse[1] <= 247: #resume button (checks mouse posisition) -> displays ligher resume button
      hover_resume_button(226,188) 
      pygame.display.update()

      for i in pygame.event.get():
        if i.type == pygame.MOUSEBUTTONDOWN: #checks if mouse click happens -> goes back to game
          game_grid(0,0)
          pygame.display.update()
          paused = False #ends loop
    elif 226 <= mouse[0] <= 525 and 286 <= mouse[1] <= 345: #does same for restart button
      hover_restart_button(226,286)
      pygame.display.update()
      for i in pygame.event.get():
        if i.type == pygame.MOUSEBUTTONDOWN:
          game_loop()
    elif 226 <= mouse[0] <= 525 and 379 <= mouse[1] <= 438: #does same for menu button
      hover_mmenu_button(226,379)
      pygame.display.update()
      for i in pygame.event.get():
        if i.type == pygame.MOUSEBUTTONDOWN:
          game_intro()
    elif 226 <= mouse[0] <= 525 and 472 <= mouse[1] <= 531: #does same for exit button
      hover_exit_button(226,472)
      pygame.display.update()
      for i in pygame.event.get():
        if i.type == pygame.MOUSEBUTTONDOWN:
          pygame.quit()
          sys.exit()
    else:
      pause_menu(0,0)
      pygame.display.update() #end of pause2() - loop resets if not exited
      
#If game is lost, menu is reset, game is over
def game_lost2(score):
  game_over = True
  game_over_menu(0,0)
  display_score(screen,345,175,score)
  pygame.display.update()

  while game_over: #End of game code
    for i in pygame.event.get():
      if i.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    mouse = pygame.mouse.get_pos()

    if 226 <= mouse[0] <= 525 and 286 <= mouse[1] <= 345: #checks mouse within the reset button coordinates
      hover_restart_button(226,286)
      pygame.display.update()
      for i in pygame.event.get():
        if i.type == pygame.MOUSEBUTTONDOWN:
          game_loop() #goes starts game loop with mouse click
    elif 226 <= mouse[0] <= 525 and 379 <= mouse[1] <= 438: #checks mouse within the menu button coordinates
      hover_mmenu_button(226,379)
      pygame.display.update()
      for i in pygame.event.get():
        if i.type == pygame.MOUSEBUTTONDOWN:
          game_intro() #goes to game menu with click
    elif 226 <= mouse[0] <= 525 and 472 <= mouse[1] <= 531: #checks mouse within the exit button coordinates
      hover_exit_button(226,472)
      pygame.display.update()
      for i in pygame.event.get():
        if i.type == pygame.MOUSEBUTTONDOWN:
          pygame.quit() #quits game with click
          sys.exit()
    else: #displays menu, score if all else fails
      game_over_menu(0,0) 
      display_score(screen,345,175,score)
      pygame.display.update()
#end of game_lost2()

def game_intro(): #menu screen loop function  
#setup for loop
  intro = True
  main_menu(0,0)
  pygame.display.update()

#actual beginning of loop   
  while intro:
    for i in pygame.event.get(): #Checks if red x on window is clicked, terminates program
      if i.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    mouse = pygame.mouse.get_pos()

    if 330 <= mouse[0] <= 417 and 340 <= mouse[1] <= 405: #play button (hover + click check)-> goes to game loop
      hover_play_button(330,340)
      pygame.display.update()
      for i in pygame.event.get():
        if i.type == pygame.MOUSEBUTTONDOWN:
          game_loop()
    elif 330 <= mouse[0] <= 417 and 421 <= mouse[1] <= 486: #controls button(hover + click check) -> goes to controls loop 
      hover_controls_button(330,421)
      pygame.display.update()
      for i in pygame.event.get():
        if i.type == pygame.MOUSEBUTTONDOWN:
          game_controls()
    elif 330 <= mouse[0] <= 417 and 505 <= mouse[1] <= 570: #stats button (hover + click check) -> potential for stats menu loop
      hover_stats_button(330,505)
      pygame.display.update()
      for i in pygame.event.get():
        if i.type == pygame.MOUSEBUTTONDOWN:
          print('Stats')
    else:
      main_menu(0,0) #Keeps loop running
      pygame.display.update()

#end of game_intro()

def game_controls(): #controls menu loop function 

#setup for loop
  menu_exit = False
  control_menu(0,0)
  pygame.display.update()

#Beginning of actual loop 
  while not menu_exit: #Checks if red x on window is clicked, terminates program
    for i in pygame.event.get():
      if i.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
          
    mouse = pygame.mouse.get_pos()

    if 698 <= mouse[0] <= 726 and 614 <= mouse[1] <= 642: #exit button (hover + click check) -> returns to main menu
      hover_c_exit(698,614)
      pygame.display.update()
      for i in pygame.event.get():
        if i.type == pygame.MOUSEBUTTONDOWN:
          game_intro() 
    else:
      control_menu(0,0)
      pygame.display.update()
#end of game_controls()
    
def game_loop(): #The big man himself

#Setup for game loop
  game_exit = False

  locked_positions = {}
  grid = create_grid(locked_positions) 

  change_piece = False
  current_piece = get_shape(shapes)#First piece
  next_piece = get_shape(shapes) #Second piece 
  clock = pygame.time.Clock() #Time mechanic for game
  fall_time = 0
  fall_speed = 0.27 #Actual seconds using clock
  level_time = 0
  score = 0
  
  game_grid(0,0)
  pygame.display.update()

#Actual beginning of loop   
  while not game_exit:
    grid = create_grid(locked_positions) #grid must be constantly updated (uses grid creation function^)
    fall_time += clock.get_rawtime()#fall time = time passed (1000ms = 1 second)

    clock.tick()

    if fall_time/1000 > 5: #Every 5 secs
      level_time = 0
      if fall_speed > 0.12:
        fall_speed -= 0.005 
    
    if fall_time/1000 > fall_speed:
      fall_time = 0 
      current_piece.y += 1
      if not(valid_space(current_piece, grid)) and current_piece.y > 0: #once the falling block has hit something, stop moving shape & change piece
        current_piece.y -= 1
        change_piece = True
    
    for i in pygame.event.get():#Checks for exit
      if i.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
        game_exit = True
        
      if i.type == pygame.MOUSEBUTTONDOWN:
        mx, my = pygame.mouse.get_pos()
        print(mx, my) #prints every mouse posistion 
        
      if i.type == pygame.KEYDOWN: #When clicks down (any key)
        if i.key == pygame.K_LEFT: #Moves to left only if grid is free
          current_piece.x -= 1
          if not(valid_space(current_piece,grid)):
            current_piece.x += 1
        if i.key == pygame.K_RIGHT:#Moves right only if grid is free
          current_piece.x += 1
          if not(valid_space(current_piece,grid)): 
            current_piece.x -= 1
        if i.key == pygame.K_DOWN:#Moves down one if grid is free
          current_piece.y += 1
          score += 1
          if not(valid_space(current_piece,grid)):
            current_piece.y -= 1
        if i.key == pygame.K_UP: #Rotates if grid is free
          current_piece.rotation += 1
          if not(valid_space(current_piece,grid)):
            current_piece.rotation -= 1
        if i.key == pygame.K_SPACE: #Has mini loop that makes it keep falling until there is no more space and then puts to the last spot 
          temp = current_piece.y
          while(valid_space(current_piece, grid)) and current_piece.y > 0:
            current_piece.y += 1
          else:
            current_piece.y -= 1
            last_block_y = current_piece.y
            score += last_block_y - temp
            
        if i.key == pygame.K_ESCAPE: #goes to pause loops when "esc" is hit
          pause2()

    shape_pos = convert_shape_format(current_piece) #formats shape
    
    for i in range(len(shape_pos)): #checks all shape posistions
      x, y = shape_pos[i]
      if y > -1:
        grid[y][x] = current_piece.colour #adds pieces x,y to grid of colours 

    draw_window(screen,grid)
     
    if change_piece: #When piece is locked 
      for pos in shape_pos:
        p = (pos[0],pos[1])
        locked_positions[p] = current_piece.colour #locked_postions = dic w/ pos of block and its colour
      current_piece = next_piece #piece is changed to next one
      next_piece = get_shape(shapes) #new piece is randomized 
      change_piece = False
      clear_rows(grid, locked_positions) #rows are cleared with new pieces in locked posistion 
      score += clear_rows(grid, locked_positions)*10 #score is changed ^
      
    next_block_space(491,37) #Space for the next block area
    display_score(screen,510,300,score) #area for displaying score
    draw_next_shape(next_piece,screen) #Draws next shape
    pygame.display.update()
    
    if check_lost(locked_positions): #Back up stuff for crashes involving blocks that stay 
      game_lost2(score) #retains old high score if thre is a crash

  else:
    pygame.display.quit()
#end of game_loop()

game_intro() #If game is never quit, game goes back to main menu 
