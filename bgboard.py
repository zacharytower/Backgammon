import bgspace, pygame, time
from global_vars import *
class BGBoard(object):
	'''
	The BGBoard Class is the object that contains the game state. That is, the
	position of each piece on the board.
	This class deals with drawing the board onto DISPLAYSURF and processing BGMove requests.
	This class can also reset the board, draw pieces that are moved off and displays the win animation.
	Furthermore, this object will also handle click positions and return data about the item clicked.

	'''
	def __init__(self,colorScheme):

		'''
		initiates object. The only data needed is the color scheme, a dictionary of colors.
		{pieceColorA, pieceColorB, dieColorA, dieColorB, backgroundColor, spaceColorA, spaceColorB}

		'''

	
		self.pieceColorA = colorScheme['pieceColorA']
		self.pieceColorB = colorScheme['pieceColorB']
		
		self.dieColorA = colorScheme['dieColorA']['cube']
		self.pipColorA = colorScheme['dieColorA']['pip']

		self.dieColorB = colorScheme['dieColorB']['cube']
		self.pipColorB = colorScheme['dieColorB']['pip']

		self.spaceColorA = colorScheme['spaceColorA']
		self.spaceColorB = colorScheme['spaceColorB']

		self.backgroundColor = colorScheme['backgroundColor']

		self.boarderColor = colorScheme['boarderColor']

		self.messageBoxColor = colorScheme['messageBoxColor']
		self.messageTextColor = colorScheme['messageTextColor']

		self.holderColor = colorScheme['holderColor']
		self.chipBoarderColor = colorScheme['chipBoarderColor']

		self.chipsOnBar = []


		# set default board
		a,b = self.pieceColorA, self.pieceColorB
		self.defaultBoardValues = {0: {'player': b, 'chips':2}, 5:{'player':a, 'chips':5},7:{'player':a, 'chips':3}, 11:{'player':b,'chips':5},
		12:{'player':a,'chips':5},16:{'player':b,'chips':3},18:{'player':b,'chips':5},23:{'player':a,'chips':2}}
		
		self.movedOff = {self.pieceColorA:0, self.pieceColorB:0}

		self.message = ''

		self.diceRolled = False
		self.diceRolledColor = None
		
		self.rollOff = True
		self.rollA, self.rollB = None,None

		self.resetBoard()

	
	def __getitem__(self,key):
		return self.spaceList[key]
		
	def getClickedSpace(self,clickPos, reduced = False):
		''' returns the index of the clicked space.
		If click did not click any space, then -1 is returned.
		If reduced is set to true, then the space rectangle will be reduced to the rectangle
		surrounding the pieces. (see BGSpace.entireRectangle() vs. BGSpace.reducedRectangle())'''

		for space in self.spaceList:
			
			if reduced == False:
				r = space.entireRectangle()

			else:
				r = space.reducedRectangle()

			
			#pygame.draw.rect(DISPLAYSURF,(0,0,0),space.reducedRectangle())
			#pygame.display.update()
			#time.sleep(1)

			#raw_input()
			
			if r.collidepoint(clickPos): # space was clicked:
				return space.index

		for i,owner in enumerate(self.chipsOnBar):

			x,y = (375, 325 + (50 * i * -1 if i % 2 != 0 else 1))

			if (clickPos[0] - x) ** 2 + (clickPos[1] - y) ** 2 <= (25) ** 2:
				return 'bar'

		for y in [50,450]:
			if pygame.Rect(700,y,125,150).collidepoint(clickPos): return 'offboard'

		return -1

	def resetBoard(self):

		self.spaceList = []


		for x in range(24):

			try:
				owner, quantity = self.defaultBoardValues[x]['player'], self.defaultBoardValues[x]['chips']
			except KeyError:
				owner, quantity = None, 0

			self.spaceList.append(bgspace.BGSpace(x, self.spaceColorB if x % 2 == 0 else self.spaceColorA, owner,quantity))

	def displayBoard(self):
		''' draws the board to DISPLAYSURF. Draws all of the spaces as well as other pieces of the board.'''

		# draw background rectangles

		for x in [50,400]:
			# rectangle with a x value of (x), y value of 50, width of 300, and height of 550.
			pygame.draw.rect(DISPLAYSURF, self.backgroundColor, (x,50,300,550))
		'''
		# draw each space
		for space in self.spaceList:

			space.drawToBoard()'''

		# draw outline perimeter

		# first, lets draw the board boarders and the bar.
		
		# [boarder,
		# bar,
		# seperates (C,D) from chip holders,
		# seperates chip holders from message box]
		rectectTuples = [(0,0,925,50), (0,0,50,650), (0,600,925,50), (875,0,50,650),
		(350,0,50,650),
		(700,0,50,650),
		(750,200,125,25),
		(750,425,125,25)]

		for rectectTuple in rectectTuples:
			pygame.draw.rect(DISPLAYSURF, self.boarderColor, rectectTuple)

		# draw chip holders
		for y in [50,450]:
			pygame.draw.rect(DISPLAYSURF, self.holderColor,(750,y,125,150))

		# draw chips that are moved off.
		for i in range(self.movedOff[self.pieceColorA]):
			ys = [[f] * 5 for f in range(15)]
			rt = (700 + (5*i) % 30,ys[i],25,50)

			pygame.draw.rect(DISPLAYSURF, self.pieceColorA, rt )
			# draw boarder around the chip.
			pygame.draw.rect(DISPLAYSURF, self.chipBoarderColor, rt + tuple([5]) )


		# draws the chips that are on the bar.
		if self.chipsOnBar != []:
			# the chips on the bar are only expressed by their owner

			for i, owner in enumerate(self.chipsOnBar):
				pygame.draw.circle(DISPLAYSURF, owner, (375, 325 + (50 * i * -1 if i % 2 != 0 else 1)), 25)

		# draws the message box as well as the message.
		pygame.draw.rect(DISPLAYSURF, self.messageBoxColor, (750,225,125,200))
		self.displayText((762,325))

		# show rolled dice.

		if self.diceRolled == True: # dice are rolled:

			if self.rollOff == True:
				xTup = (150,550)
				color = 'A'

			elif self.diceRolledColor == self.pieceColorA: # if player A rolled
				xTup = (450,550)
				color = 'A'

			else: # B rolled
				xTup = (150,250)
				color = 'B'

			cube, pip = [eval('self.{}Color{}'.format(h,color)) for h in ['die','pip']] #sets cube and pip to their respective colors.

			if self.rollOff == True:
				colorAlt = 'A' if color == 'B' else 'B'
				cubeAlt, pipAlt = [eval('self.{}Color{}'.format(h,colorAlt)) for h in ['die','pip']]

			for i,x in enumerate(xTup):

				if self.rollOff == True:
					colorSequence = ((cube,pip),(cubeAlt,pipAlt))

				else:
					colorSequence = ((cube,pip),(cube,pip))


				pygame.draw.rect(DISPLAYSURF,colorSequence[i][0],(x,300,50,50)) # draw cube rectangle to board

				# in the case of a roll off, then rollA is the roll of player A and roll B is the role of player B.
				if x in [450,150]:
					roll = self.rollA

				else:
					roll = self.rollB


				o = {1:((x+25,325,10),),2:((x+35,315,5),(x+15,335,5))}
				p = {3:o[2] + ((x+25,325,5),), 4: tuple([(x + m,300 + n,5) for m in [15,35] for n in [15,35]])}
				q = {5:(p[4]+ p[3]), 6:(tuple([(x+m,300+n,5) for m in [15,35] for n in [10,25,40]]))}

				rollDict = merge_two_dicts(o,p); rollDict = merge_two_dicts(rollDict,q)
				
				for c in rollDict[roll]:
					
					pygame.draw.circle(DISPLAYSURF,colorSequence[i][1],c[:2],c[2])

		for space in self.spaceList:
			space.drawToBoard()

		#pygame.display.update()

	def displayText(self, pos, textSize = 20):

		'''
		displays string 'text' at position 'pos'
		you may also define the text size.
		'''
		# DroidSerif = /usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf
		fontObj = pygame.font.Font('freesansbold.ttf',textSize)
		textSurfaceObj = fontObj.render(self.message, True, self.messageTextColor)

		textRectObj = textSurfaceObj.get_rect()
		textRectObj.center = (pos)

		DISPLAYSURF.blit(textSurfaceObj, textRectObj)
		

	def addChipToBar(self, color):

		self.chipsOnBar.append(color)

	def removeChipFromBar(self, color):
		

		self.chipsOnBar.remove(color)

		

	def makeMove(self, move):

		''' makes the move and edits the board state.
		Returns 0 if the move was valid. Returns -1 if move was invalid.'''
		
		if move.inverse == False: # move is not an inverse move:
			if self.isValidMove(move) == False: return -1

		
		hit = False

		if self.spaceList[move.toWhere].spaceOwner != move.color and self.spaceList[move.toWhere].howManyChips == 1 and self.spaceList[move.toWhere].spaceOwner != None: # hit the opponent

			hit = True
			self.spaceList[move.toWhere].spaceOwner = move.color
			self.spaceList[move.toWhere].howManyChips = 1


			hitColor = self.pieceColorA if move.color == self.pieceColorB else self.pieceColorB
			self.addChipToBar(hitColor)

			#return 0
		if move.fromWhere == 'offboard':
			self.removeFromSideColumn(move.color)

		elif move.toWhere == 'offboard':
			self.addToSideColumn(move.color)

		
		if type(move.fromWhere) != str:

			try:
				
				self.spaceList[move.fromWhere].howManyChips -= 1

				if self.spaceList[move.fromWhere].howManyChips == 0: # no one is on the space
					self.spaceList[move.fromWhere].spaceOwner = None
			except IndexError: # space was bogus
				pass

		else:
			if move.fromWhere == 'bar':
					self.removeChipFromBar(move.color)
			


		if type(move.toWhere) != str:
			#print move.toWhere

			if hit == False:
				self.spaceList[move.toWhere].howManyChips += 1
			self.spaceList[move.toWhere].spaceOwner = move.color

		return 0

	def addToSideColumn(self,color):
		''' adds a piece to the side column. If the side column reaches 15, then that player wins!'''
		self.movedOff[color] += 1

	def removeFromSideColumn(self, color):
		self.movedOff[color] -= 1

	def hasWon(self,color):
		''' returns if the color has won'''
		return self.movedOff[color] == 15

	def isValidMove(self,move):
		
		''' returns true if the roll is valid given the current board.'''

		
		assert type(move.roll) == int, 'Roll not passed as integer.'
		# make sure the owner is moving existing pieces


		# make sure the owner is not moving pieces outside of the barriers of the board.
		if type(move.toWhere) != str:
			if (0 <= move.toWhere < 24) == False:
				return False

		if type(move.fromWhere) != str:
			if (0 <= move.fromWhere < 24) == False: return False

			if self.spaceList[move.fromWhere].howManyChips == 0: # no chips on requested space
				return False

			# make sure that the owner is moving pieces that belong to him.
			if move.color != self.spaceList[move.fromWhere].spaceOwner:
				return False

		else:
			if move.color not in self.chipsOnBar: return False

		# make sure the owner is not moving onto a spot owned by the opponent
		if move.toWhere != 'offboard':
			
			if self.spaceList[move.toWhere].howManyChips >= 2 and self.spaceList[move.toWhere].spaceOwner != move.color:
				return False

		# make sure pieces are not on the bar while move is being made
		if move.fromWhere != 'bar' and move.color in self.chipsOnBar:
			return False

		# make sure roll is consistent with the move made.

		if type(move.fromWhere) == str or type(move.toWhere) == str: # moving off the bar

			if type(move.fromWhere) == str:
				x = move.toWhere

			else:
				x = move.fromWhere

			if move.color == self.pieceColorA:
				moveDistance = 24 - x

			elif move.color == self.pieceColorB:
				moveDistance = x + 1

		elif move.fromWhere != str and move.toWhere != str:

			moveDistance = abs(move.fromWhere - move.toWhere)

		if moveDistance != move.roll:
			print 'triggered'
			return False

		# make sure player already hasn't used that roll yet.

		if move.ignoreRollDict == False:
			try:
				if move.rollDict[moveDistance] == True: # move already used
					return False

			except KeyError:
				return False

		# make sure player has all of his chips in home base before moving chips off

		if move.toWhere == 'offboard':


			homeBase = range(6) if move.color == self.pieceColorA else range(18,24)

			for space in self.spaceList:
				if space.index not in homeBase and space.spaceOwner == move.color:
					return False

		# make sure if player is moving off the bar that the player is moving into the other player's home base. (and not anywhere else)
		if move.fromWhere == 'bar':
			if move.color == self.pieceColorA and move.toWhere not in range(18, 23 + 1): return False
			if move.color == self.pieceColorB and move.toWhere not in range(5+1): return False


		elif move.toWhere != 'offboard': # make sure player is moving in the right direction.

			if move.color == self.pieceColorA and move.fromWhere <= move.toWhere: 
				
				return False
			if move.color == self.pieceColorB and move.fromWhere >= move.toWhere:

				return False



		return True

	def __repr__(self):
		return str([x for x in self.spaceList])

def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z
