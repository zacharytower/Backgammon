from global_vars import *
import itertools
class BGSpace(object):

	'''
	The BGSpace object contains the data for any given space on the BGBoard board.
	It contains what color pieces are on the given space, and whether or not they may be hit.
	'''

	def __init__(self,index, spaceColor, startPieceColor = None, startPieceQuantity = 0):

		# color scheme must already be valid by this point.

		self.index = index
		self.spaceColor = spaceColor
		self.spaceOwner = startPieceColor
		self.howManyChips = startPieceQuantity

		if 12 <= self.index <= 23: # on the top row
			self.x = 50 * (self.index - 12) + (100 if self.index >= 18 else 50)
			self.y = 50
		else: # on the bottom row
			self.x = 50 * (11 - self.index) + (100 if self.index <= 5 else 50)
			self.y = 350


	def changePosession(self, newOwner = None):

		self.spaceOwner = newOwner

	def changeQuantity(self, newQuantity):

		assert 15 >= self.howManyChips >= 0, 'Invalid number of chips on one space!'
		self.howManyChips = newQuantity

	def addOne(self):

		assert self.howManyChips + 1 != 15, 'Too many chips on the board!'

		self.howManyChips += 1

	def removeOne(self):
		''' removes one checker from itself.'''

		assert self.howManyChips - 1 != -1, 'Negative amount of chips on one space!'

		self.howManyChips -= 1

	def entireRectangle(self):
		''' returns a rectangle of the entire space.'''

		return pygame.Rect(self.x, self.y, 50, 250)

	def reducedRectangle(self):
		''' returns a rectangle that encases only the pieces on that space.'''

		return pygame.Rect(self.x, self.y if 12 <= self.index <= 23 else self.y + (5-(5 if self.howManyChips >= 5 else self.howManyChips)) * 50, 50, 50 * self.howManyChips)


	def drawToBoard(self):

		''' draws self onto DISPLAYSURF. '''

		# first, lets determine y.
		if self.index in range(12,23 + 1): # on the upper part of the board
			top = True
			y = 50

		else: # on the lower part of the board
			top = False
			y = 600

			'''
		if self.index in range(6, 17 + 1): # between 6 and 17 inclusive; Not beyond the 'BAR'
			modifier = 50

			# the subtractor is the number that is used to determine how many 
			# spaces away the given space is to the edge of the board.

			if top:
				subtractor = 11

			else:
				subtractor = 12

		else: # Beyond the 'BAR'
			modifier = 400

			if top:
				subtractor = 18

			else:
				subtractor = 5'''

		if top == True:
			a_base = 50 * (self.index-12) + (50 if self.index < 18 else 100)

		else: # bottom
			a_base = 50 * abs(self.index - 11) + (50 if self.index > 5 else 100)

		a = (a_base,y)
		
		b = (a[0] + 50, a[1])

		if top: # we are on the top
			# c should be DOWN
			c = (a[0] + 25, a[1] + 250)

		else: # we are on the bottom
			# c should be UP
			c = (a[0] + 25, a[1] - 250)

		
		pygame.draw.polygon(DISPLAYSURF, self.spaceColor, (a,b,c)) # draws to board

		# now, draw chips to board
		# we will use the inverse color tecnique for this.

		if self.howManyChips == 0 or self.spaceOwner == None: return 0
		
		if self.spaceOwner != None:

			inverseColor = tuple([256 - x for x in self.spaceOwner])


		chipX = a[0] + 25
		
		for i,chipY in enumerate(itertools.count(y + (25 if top else -25), 50 if top else -50)):
		
			i += 1

			if self.howManyChips < i:
				break

			if i > 10:
				i -= 10
			elif i > 5:
				i -= 5

			pointToDraw = (chipX,chipY)
			
			colorToDraw = inverseColor if 6 <= i <= 10 else self.spaceOwner
			
			pygame.draw.circle(DISPLAYSURF, colorToDraw, pointToDraw, 25)	

		return 0



	def __repr__(self):
		return 'Space {} with {} pieces owned by {}.'.format(self.index,self.howManyChips,self.spaceOwner)
		
			