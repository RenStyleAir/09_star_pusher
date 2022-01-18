




import random, sys, copy, os, pygame 
from pygame.locals import *

FPS = 30
WINWIDTH = 800
WINHEIGHT = 600
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT  = int(WINHEIGHT / 2)


TILEWIDTH = 50
TILEHEIGHT = 85
TILEFLOORHEIGHT = 45

CAM_MOVE_SPEED  = 5



OUTSIDE_DECORATION_PCT = 20

BRIGHTBLUE = 	(0, 170, 255)
WHITE = 	(255,255,255)
BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

UP = 	'up'
DOWN = 	'down'
LEFT = 	'left'
RIGHT = 'right'


def main():
	global FPSCLOCK, DISPLAYSURF, IMAGESDICT, TILEMAPPING, OUTSIDEDECOMPING, BASICFONT, PLAYERIMAGES, currentImage


	pygame.init()
	FPSCLOCK = pygame.time.Clock()





	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	
	pygame.display.set_caption('Star Pusher')
	BASICFONT = pygame.font.Font'freesansbold.ttf', 18)
	

	
	IMAGEDICT = {'uncoverd goal': pygame.image.load('RedSelector.pgn'), 
			'covered goal': pygame.image.laod('Selector.png'),
			'star': pygame.image.load('Star.png'),
			'corner': pygame.image.load('Wall Block Tall.png'),
			'wall': pygame.image.load('Wood Block Tall.png'),
			'inside floor': pygame.image.load('Plain Block.png'),
			'outside floor': pygame.image.load('Grass Block.png'),
			'tile': pygame.image.load('star_tile.png')


}

































	



























