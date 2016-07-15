from global_vars import *

class BGMove(object):

	'''
	The BGMove class acts as a 'move packet'.
	That is, a BGMove object tells how to move one piece of the move.
	BGMove can either be computer generated or dictated by a human player.

	BGMove assumes the parameters passed are valid.
	'''

	def __init__(self, roll, color, fromWhere, toWhere, inverse = False):

		assert type(roll) == int, 'roll is old roll.'
		self.roll = roll # one integer representing the die element that was used on this role.
		
		self.color = color # RGB color tuple representing the mover.

		self.fromWhere = fromWhere
		self.toWhere = toWhere
		self.inverse = inverse

	def setMove(self, fromWhere, toWhere):
		'''
		sets the dimensions of the move.
		fromWhere is the starting position of the piece.
		toWhere is where the piece will land.

		'''
		
		self.fromWhere = fromWhere
		self.toWhere = toWhere

	def moveInverse(self):
		'''
		returns a move object that would negate the affects of the original move object.
		If move is applied to a board, then move.moveInverse() would revert the board
		back to its original state.'''

		return BGMove(self.roll, self.color, self.toWhere, self.fromWhere, True)

	def __repr__(self):
		return 'Moving color {} from {} to {}.'.format(self.color, self.fromWhere, self.toWhere)

		
