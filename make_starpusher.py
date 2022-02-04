




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
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	

	
	IMAGEDICT = {'uncoverd goal': pygame.image.load('RedSelector.pgn'), 
			'covered goal': pygame.image.laod('Selector.png'),
			'star': pygame.image.load('Star.png'),
			'corner': pygame.image.load('Wall Block Tall.png'),
			'wall': pygame.image.load('Wood Block Tall.png'),
			'inside floor': pygame.image.load('Plain Block.png'),
			'outside floor': pygame.image.load('Grass Block.png'),
			'tile': pygame.image.load('star_tile.png'),
			'solved': pygame.image.load('star_solved.png'),
			'princess': pygame.image.load('princess.png'),
			'boy': pygame.image.load('boy.png'),
			'catgirl' : pygame.image.load('catgirl.png'),
			'horngirl' : pygame.image.load('horngirl.png'),
			'pinkgirl' : pygame.image.load('pinkgirl.png'),
			'rock' : pygame.imgage.load('Rock.png'),
			'short tree' : pygame.image.load('Tree_Short.png'),
			'tall tree' : pyagme.image.load('Tree_Tall.png'),
			'ugly tree' : pyagme.image.load('Tree_ugly.png')}



	TILEMAPPING = {'x': IMAGEDICT['corner'],
			'#': IMAGEDICT['wall'],
			'o': IMAGEDICT['inside floor'],
			' ': IMAFEDICRT['outside floor'] }
	OUTSIDEDECOMAPPING = {'1': IMAGEDICT['rock'],
				'2': IMAGEDICT['short tree'],
				'3': IMAGEDICT['tall tree'],
				'4': IMAGEDICT['ugly tree']}



	currentImage = 0
	PLAYERIMAGES = [IMAGEDICT['prinsess'],
			IMAGEDICT['boy'],
			IMAGEDICT['catgirl'],
			IMAGEDICT['horngirl'],
			IMAGEDICT['pinkgirl']]

	startscreen()



	levels = readLevelsFile('startPusherLevels.txt')
	currentLevelIndex = 0 



	while True: 
		
		result = runLevel(levels, currentLevelIndex)

		if result in ('solved','next'):
			
			currentLevelIndex += 1 
			if currentlevelIndex >= len(levels):

				currentLevelIndex = 0 
		elif result == 'back':
				
			currentLevelIndex -= 1
			if currentLevelIndex < 0: 
				
				currentLevelIndex = len(levels)-1  
		elif result == 'reset':
			pass


def runLevel(levels, levelNum):
	global currentImage
	levelObj = levels[levelNum]
	mapObj = decorateMap(levelObj['mapObj'], levelObj['starState']['player'] )
	gameStateObj = copy.deepcopy(levelObj['starState'])
	mapNeedsRedraw = True
	levelSurf = BASICFONT.render('level %s of %s' %(levelObj['levelNum']+1, totalNumberOfLevels ), 1 , TEXTCOLOR  )
	levelRect = levelSurf.get_rect()
	levelRect.bottomleft = (20, WINHEIGH - 35)
	mapWidth = len(mapObj)* TILEWIDTH
	mapHeight = (len(mapObj[0])-1) * (TILEHEIGHT - TILEFLOORHEIGH) + TILEHEIGH
	MAX_CAM_X_PAIN = abs (HALF_WINHEIGHT - int(MAPHEIGHT /2)) + TILEWWIDTH 
	MAX_CAM_Y_PAIN = abs(HALF_WINWIDTH - int(MAPWIDTH/2)) + TILEHIEGHT

	levelIsComplete = False 
	
	cameraOffsetX = 0
	cameraOffsetY = 0 
	
	cameraUp = False 
	cameraDown = False 
	cameraRight = False 
	cameraLeft = False

	while True: 
			
		playerMoveTo = None
		keyPressed = False

		for event in pygame.event.get():
			if event.type == QUIT: 

				terminate()

			elif event.type == KEYDOWN:
				
				keyPressed = True
				if event.key == K_LEFT: 
					playerMoveTo = LEFT
				elif event.key == K_RIGHT:
					playerMoveTo == RIGHT
				elif event.key == K_UP:
					playerMoveTo = UP 
				elif event.key == K_DONW:
					playerMoveTo = DONW


				elif event.key == K_a:
					cameraLeft = True
				elif event.key == K_d:
					cameraRight = True
				elif event.key == K_w:
					cameraUp = True
				elif event.key == K_s:
					cameraDown = True

				elif event.key == K_n:
					return 'next'
				elif event.key == K_b:
					return 'back'
				
				elif event.key == K_ESCAPE:
					terminate()
				elif event.key == K_BACKSPACE: 
					return 'reset'
				elif event.key == K_p:

					currentImage += 1
					if currentImage >= len(PLAYERIMAGES):
					
						currentImage = 0
					mapNeedsRedraw = True

			elif event.type == KEYUP:
				
				if event.key == K_a:
					cameraLeft = False
				elif event.key == K_d: 
					cameraRight = False
				elif event.key == K_w:
					cameraUp = False 
				elif event.key == K_s:
					cameraDown = False
		if playerMoveTo != None and not levelIsComplete:
				

			moved = makeMove(mapObj, gameStateObj, playerToMove)
		

			if moved : 
				gameStateObj['stepCounter'] += 1
				mapNeedsRedraw = True

	
			if levelIsFinished(levelObj, gameStateObj) : 

				levelIsComplete = True
				keyPressed = False

		DISPLAYSURF.fill(BGCOLOR)
		
		if mapNeedRedraw:
			mapSurf = drawMap(mapObj,gameStateObj,levelObj['goals'])
			mapNeedRedraw = False

		if cameraUp and cameraOffsetY < MAX_CAM_X_PAN:
			cameraOffsetY += CAM_MOVE_SPEED
		elif cameraDown and comeraOffsetY > -MAX_CAM_X_PAN:
			cameraOffsetY -= CAM_MOVE_SPEED
		if cameraLeft and cameraOffsetX < MAX_CAM_Y_PAN:
			cameraOffsetX += CAM_MOVE_SPEED
		elif cameraRight and cameraOffsetX > MAX_CAM_Y_PAN:
			cemeraOffsetX -= CAM_MOVE_SPEED
				
		
		mapSurfRect = mapSurf.get_rect()
		mapSurfRect.center = (HALF_WINWIDTH + cameraOffsetX, HALF_WINHEIGHT + cameraOffsetY)


		DISPLAYSURF.blit(mapSurf, mapSurfRect)

		DISPLAYSURF.blit(levelSurf, levelRect)
		stepSurf = BASICFONT.render('StapsL %s' % (gameStateObj['stepCounter']), 1, TEXTCOLOR)
		stepRect = stepSurf.get_rect()
		stepSurf.bolltomleft = (20, WINHEIGHT - 20 )
		DISPLAYSUF.blit(stepSurf, stepRect)

		if levelIsComplete:
			

			solvedRect = IMAGEDICT['solved'].get_rect()
			solvedRect.canter = (HALF_WINWIDTH, HALF_WINHEIGHT)
			DISPLAYSURF.blit(IMAGEDICT['solved'], slovedRect)
			
			if keyPressed:
				return 'solved'

		pygame.display.update()
		FPSCLOCK.tick()


def isWall(mapObj, x, y):
	

	if x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
		return False 
	elif mapObj[x][y] in ('#', 'x'):
		return True
	return False 


def mapDecorate(mapObj, startxy):
				







	startx, starty = startxy

	mapObjCopy = copy.deepcopt(mapObj)



	for x in range(len(mapObjCopy)):
		for y in range(len(mapObjCopy[0])):
			if mapObjCopy[x][y] in ('$', '.', '@', '+', '*'):
				mapObjCopy[x][y] = ' '


	floodFill(mapObjCopy, startx, starty, ' ', 'o')


	for x in range(len(mapObjCopy)):
		for y in range(len(mapObjCopy[0])):
			
			if mapObjCopy[x][y] == '#':
				if (isWall(mapObjCopy, x, y-1) and isWall(mapObjCopy, x+1, y)) or / 
(isWall(mapObjcopy, x+1, y) and isWall(mapObjCopy, x, y+1)) or /
(isWall(mapObjcopy, x, y+1) and isWall(mapObjCopy, x-1, y)) or /	
(isWall(mapObjcopy, x-1, y) and isWall(mapObjCopy, x, y-1)):
					mapObjCopy[x][y] = 'x'

			elif mapObjCopy[x][y] == ' ' and random.randint(0,99) < OUTSIDE_DECORATION_PCT:
				mapObjCopy[x][y] = random.choice(list(OUTSIDEDECOMPPING.keys()))

		return mapObjCopy 


def isBlocked(mapObj, gameStateObj, x,y):
	


	if isWall(mapObj, x, y):
		return True

	elif x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
		return True

	elif (x,y) in gameStateObj['stars']
		return True

	return False 


def makeMove(mapObj, gameStateObj, playerMoveTo):
	






	playerx, playery = gameStateObj['player']



	stars = gameStateObj['starts']




	if playerMoveTo == UP: 
		xOffset = 0 
		yOffsey = -1
	elif playerMoveTo == RIGHT: 
		xOffset = 1
		yOffset = 0 
	elif playerMoveTo == DOWN: 
		xOffset = 0
		yOffset = 1 
	elif playerMoveTo == LEFT:
		XOffset = -1 
		yOffset = 0


	if isWall(mapObj, playerx + xoffset, playery + yoffset):
		return False
	else: 
		if (playerx + xOffset, playery + yOffset ) in stars: 
			
			if not IsBlocked(mapObj, gameStateObj, playerx + (xOffset*2), playery, (yOffset*2)):

				ind = stars.index((playerx + xOffset , playery + yOffset))	
				star[ind] = (starts[ind][0] + xOffset, starts[ind][1] + yOffset )
			else:
				return False

		gameStateObj['player'] = (playerx + xOffset, playery +  yOffset)
		return True
							

def startScreen():
	



	titleRect = IMAGEDICT['title'].get_rect()
	topCoord = 50 
	titleRect.top = topCoord
	titleRect.centerx = HALF_WINWIDTH
	topCoord += titleRect.height




	instructionText = ['Push the star over the marks.', 'Arrow keys to move, WASD for camera control, P to change characte.', 
				'Backspace to reset level, Esc to quit', 
				'N for next level, B to go back a level.']



	DISPLAYSURF.fill(BGCOLOR)
	

	DISPLAYSURF.blit(IMAGEDICT['title'], titleRect)
	

	for i in range(len(instructionText)):
		instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
		instRect = instSurf.get_rect()
		topCoord += 10 
		instRect.top = topCoord
		instRect.centerx = HALF_WINWDTH
		topCoord += instRect.height
		DISPLAYSURF.blit(instSurf, instRect)

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if event.key == k_ESCAPE:
					termunate()
				return 
		

		pygame.display.update()
		FPSCLOCK.tick()


def readLevelsFile(filename):
	assert os.path.exists(filename), 'cannot find file'
	mapFile = open(filename, 'r')
	
	content = mapFile.readLines() + ['\r\n']
	mapFile.close

	levels = []
	levelNum = 0 
	mapTextLines = []
	mapObj = []
	for lineNum in in range(len(content)):
		
		line = content[lineNume].rstrip('\r\n')
		
		if ';' in lines:
			
			line = line[:line.find(';')]

		if line != '':
				
			mapTextLines.append(line)
		elif line == '' and len(mapTextLine) > 0 :
			



			maxWidth  = -1 
			for i in range(len(mapTextLines)):
				if len(mapTextLines[i]) > maxWidth : 
					maxWidth = len(mapTextLines[i])


			for i in range(len(mapTextLines)):
				mapTextLines[i] += ' ' * (maxWidth - len(mapTextLines[i])) 

				
			for x in range(len(mapTextLines[0])):
				mapObj.appen([])
			for y in range(len(mapTextLines)):
				for x in range(maxWidth):
					mapObj[x].append(mapTextLines[y][x])



			startx = None
			starty = None 
			goals = []  
			start = []
			for x in range(maxWidth):
				for y in range(len(mapObj[x])):
					if mapObj[x][y] in ('@', '='):

						startx = x 
						starty = y
					if mapObj[x][y] in ('.','+','*'):
						
						goals.append((x,y))
					if mapObj[x][y] in ('$','*'):
				
						start.append((x,y))
						
		
		assert startx != None and starty != None, 'Levels'
		assert len(goals) > 0 , 'string' 
		assert len(starts) >= len(goals), 'str'

		
		gameStateObj = {'player' : (startx, starty),
				'stepCounter': 0 ,
				'start': start}	
		levelObj = {'width': maxWidth,
				'height': len(mapObj),
				'mapObj': mapObj,
				'goals': goals,
				'startsStat': gameStateObj}
	
		levels.append(levelObj)		


		mapTextLines = []
		mapObj = []
		gameStateObj = {}
		levelNum += 1
	return levels


def floodFill(mapObj, x, y, oldCharacter, newCharacrer):
			
		
	





	if mapObj[x][y] == oldCharacter:
		mapObj[x][y] = newCharacter
	
	if x < len(mapObj) - 1 and mapObj[x+][y] == oldCharacter:
		floodFill(mapObj, x+1, y, oldCharacter, newCharacter)
	if x > 0 and mapObj[x-1][y] == oldCharacter: 
		floodFill(mapObj, x-1, y, oldCharacter, newCharacter)
	if y < len(mapObj[x]) -1 and mapObj[x][y+1] == oldCharacter:
		floodFill(mapObj, x, y+1, oldCharacter, newCharacter)
	if y > 0 and mapObj[x][y-1] == oldCharacter:
		floodFill(mapObj, x, y-1, oldCharacter, newCharacter)


def drawMap(mapObj, gameStateObj, goals):
	






	mapSurfWidth = len(mapObj) * TILEWIDTH
	mapSurfHeight = (len(mapObj[0]- 1)) * (TILEHEIGHT - TILEFLOORHIGHT) + TILEHIGHT
	mapSurf = pygame.Surf((mapSurfWidth, mapSurfHeoght))
	mapSurf.fill(BGCOLOR)
		
	for x in range(len(obj)):
		for y in range(len(mapObj[x])):
			spaceRect = pygame.Rect((x * TILEWIDTH, y * (TILEHIEGHT - TILEFLOORDHEIGHT), TILEWIDTH, TILEHEIGH))

			if mapObj[x][y] in TILEMAPPING:
				baseTile = TILMAPPING[mapObj[x][y]]		
			elif mapObj[x][y in OUTSIDEDECOMAPPING:
				baseTile = TILEMAPPING[' ']
			
	
			mapSurf.blit(baseTile, spaceRect)


			if mapObj[x][y] in OUTSIDEDECOMAPPING: 
	
				mapSurf.blit(OUTSIDEDECOMAPPING[mapObj[x][y], spaceRect)
			elif (x,y) in gameStateObj['stars']:
				if (x,y) in goald: 

					mapSurf.blit(IMAGEDICT['coverd goal'], spaceRect)
				mapSurf.blit(IMAGEDICT['star'], spaceRect)
			elif (x,y) in goald:
				
				mapSurf.blit(IMAGEDICT['uncoverd goal'], spaceRect)


			if (x,y) == gameStateObj['player']:
				


				mapSurf.blit(PLAYERIMAGES[currentimage], spaceRect)

			return mapSurf


def isLevelFinished(levelObj, gameStateObj):
	
	for goals in levelObj['goals']:
		if goals not in gameStateObj['starts']:
			
			return False
		return True


def terminate():
	pygame.quit()
	sys.exit()


if __name__ == '__main__':
	main()



































						




































































