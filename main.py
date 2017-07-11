# Shoutout to sentdex for introducing me to pygame
# Coded by: Akash Gheewala

# Importing modules
import pygame
import random
import time

# High score file *WIP*
HS_FILE = "highscore.txt"

# Initialize pygame
pygame.init()

# Frequency, size, channels, buffersize
pygame.mixer.pre_init(44100, 16, 2, 4096)

# Load in the crashing sound and game theme song
crash_sound = pygame.mixer.Sound('crash.wav')
pygame.mixer.music.load('dhoom.wav')

# Window dimension variables
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))

# Color variables to be used for background and objects
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
bright_red = (255,0,0)
grey = (169,169,169)
green = (0,200,0)
bright_green = (0,255,0)
block_color = (53,115,255)

# Setting caption for app window
pygame.display.set_caption('Cube Runner')
clock = pygame.time.Clock()

# Loading in player object image
carImg = pygame.image.load('new_triangle.png')
gameIcon = pygame.image.load('icon_triangle.png')

# Setting app window icon
pygame.display.set_icon(gameIcon)

pause = False

"""
***** FUNCTIONS *****
"""
# Pauses game
def paused():

	pygame.mixer.music.pause()

	largeText = pygame.font.Font('freesansbold.ttf', 115)
	TextSurf, TextRect = text_objects("Paused", largeText)
	TextRect.center = ((display_width / 2), (display_height / 2))
	gameDisplay.blit(TextSurf, TextRect)

	while pause:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					unpause()
				if event.key == pygame.K_q:
					pygame.quit()
					quit()

		button("Continue",150,450,150,60,green,bright_green,unpause)
		button("Quit",550,450,150,60,red,bright_red,quitgame)

		pygame.display.update()
		clock.tick(15)

# Unpauses game
def unpause():
	global pause
	pygame.mixer.music.unpause()
	pause = False

# Quits pygame and program
def quitgame():
	pygame.quit()
	quit()

# High score function *WIP*
def high_score(score):
	font = pygame.font.SysFont(None, 25)
	text = font.render("high score: " + str(score), True, black)
	gameDisplay.blit(text, (0,20))

# Displays the current score
def blocks_dodged(count):
	font = pygame.font.SysFont(None, 25)
	text = font.render("Score: " + str(count), True, black)
	gameDisplay.blit(text, (0, 0))

# Creating the cubes
def blocks(block_x_list, blocky, blockw, blockh, color):
	for block_x in block_x_list:
		pygame.draw.rect(gameDisplay, color, [block_x, blocky, blockw, blockh])

# Displays player object image
def car(x,y):
	gameDisplay.blit(carImg, (x,y))

def text_objects(text, font):
	textSurface	= font.render(text, True, white)
	return textSurface, textSurface.get_rect()

# Crash function 
def crash():

	pygame.mixer.music.stop()
	pygame.mixer.Sound.play(crash_sound)

	largeText = pygame.font.Font('freesansbold.ttf', 115)
	TextSurf, TextRect = text_objects("Game Over", largeText)
	TextRect.center = ((display_width / 2), (display_height / 2))
	gameDisplay.blit(TextSurf, TextRect)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					game_loop()
				if event.key == pygame.K_q:
					pygame.quit()
					quit()

		button("Play Again",150,450,150,60,green,bright_green,game_loop)
		button("Quit",550,450,150,60,red,bright_red,quitgame)

		pygame.display.update()
		clock.tick(15)

# Creates the "button" GUI
def button(msg,x,y,w,h,ic,ac,action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
		
	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
		if click[0] == 1 and action != None:
			action()
	else:	
		pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

	smallText = pygame.font.Font("freesansbold.ttf", 20)
	textSurf, textRect = text_objects(msg, smallText)
	textRect.center = ( (x + (w/2)), (y + (h/2))  )
	gameDisplay.blit(textSurf, textRect)

# Display for start of program
def game_intro():

	#display_msg("Ghee Inc.", 40, bright_red, (display_width / 2), (display_height * 0.1))

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					game_loop()
				if event.key == pygame.K_q:
					pygame.quit()
					quit()

		gameDisplay.fill(grey)
		largeText = pygame.font.Font('freesansbold.ttf', 115)
		TextSurf, TextRect = text_objects("Cube Runner", largeText)
		TextRect.center = ((display_width / 2), (display_height / 2))
		gameDisplay.blit(TextSurf, TextRect)

		button("Start",150,450,150,60,green,bright_green,game_loop)
		button("Quit",550,450,150,60,red,bright_red,quitgame)

		pygame.display.update()
		clock.tick(15)

# Main loop consisting of game logic
def game_loop():
	global pause

	# Plays music indefinitely
	pygame.mixer.music.play(-1)

	# Variables for player object starting position
	x = (display_width * 0.35)
	y = (display_height * 0.8)

	# Change in the players position
	car_x_change = 0

	# Variables for the blocks that will be generated
	block_startx = random.randrange(0, display_width)
	block_starty = -600
	block_speed = 5
	block_width = random.randrange(100,101)
	block_height = 100
	block_count = 1
	block_x_list = [random.randrange(0, display_width - block_width)] 

	# Amount of cubes dodged
	dodged = 0

	# High score logic *WIP*
	f = open(HS_FILE, 'w')
	try:
		highscore = int(f.read())
	except:
		highscore = 0


	gameExit = False

	while not gameExit:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					car_x_change += -7
				elif event.key == pygame.K_RIGHT:
					car_x_change += 7
				if event.key == pygame.K_p:
					pause = True
					paused()
				if event.key == pygame.K_m:
					pygame.mixer.music.fadeout(1000)

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					car_x_change = 0

		x += car_x_change

		gameDisplay.fill(grey)
		blocks(block_x_list, block_starty, block_width, block_height, block_color)
		block_starty += block_speed
		car(x,y)
		blocks_dodged(dodged)
		high_score(highscore)

		# Crashing the player if they go past the window borders
		if x > display_width - 85 or x < 0:
			crash()

		# Cubes will randomly appear along the x-axis of the window
		if block_starty > display_height:
			block_x_list = []
			block_starty = 0 - block_height
			for x in range(block_count):
				block_x_new = random.randrange(0, display_width - block_width)
				block_x_list.append(block_x_new)

			blocks(block_x_list, block_starty, block_width, block_height, block_color)
			#block_startx = random.randrange(0, display_width)
			dodged += 1
			if dodged % 5 == 0:
				block_speed += 1

			if dodged % 10 == 0:
				if block_count < 4:
					block_count += 1

		# Crashing the user if they hit a cube
		if y < block_starty + block_height:
			for block_startx in block_x_list:
				if x > block_startx and x < block_startx + block_width or x + 85 > block_startx and x + 85 < block_startx + block_width:
					crash()

		pygame.display.update()
		clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()