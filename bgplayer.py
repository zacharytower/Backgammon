import bgmove
import random
from global_vars import *
class BGPlayer(object):
	'''
	the BGPlayer class is used in the players in the game.
	It is capable of creating BGMove class objects, that dictate a move made by one of the players.

	The class can act as either a human player or computer player.
	'''

	def __init__(self, color):

		self.color = color
		

	def bogoMove(self, roll, board):
		''' simplest and worst computer AI.
		Given the role, tries random use of the rolls and returns the first valid solution that was found.
		Roll is expected to be a tuple of BOTH the die rolls. ex (5,6) and not (5)
		Returns a BGMove object.'''

		'''
		moveList = []
		if roll[0] == roll[1]: # doubles
			roll = [roll[0]] * 4'''

		moveList = []

		while len(moveList) < len(roll):


			'''
			if roll[0] == roll[1]:
				rollA, rollB = roll[0],roll[0]

			else:'''
			
			rollA, rollB = roll

			ownedSpaceIndeces = [space.index for space in board if space.spaceOwner == self.color]

			fromWhere =  random.choice(ownedSpaceIndeces)
			dieUsed = rollB if len(moveList) != 1 else rollA
			toWhere = fromWhere + dieUsed

			if self.color in board.chipsOnBar:
				fromWhere = 'bar'
				toWhere = dieUsed - 1
			
			elif all(map(lambda x: 18 <= x <= 23, [i.index for i in board.spaceList])): # all pieces are in home base
				fromWhere = 24 - dieUsed
				toWhere = 'offboard'
			
			moveObject = bgmove.BGMove(dieUsed, self.color,fromWhere,toWhere, {rollA:False,rollB:False}) # don't even bother with using the roll dict
			
			ev = board.makeMove(moveObject)
			assert ev in [-1,0], 'ev is invalid.'

			if ev == -1:
				moveList = []


			if ev == 0:
				moveList.append(moveObject)


		return tuple(moveList)
		






