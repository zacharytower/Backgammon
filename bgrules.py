def isValidMove(self,move):

		''' returns true if the roll is valid given the current board.'''

		# make sure the owner is moving existing pieces
		if self.spaceList[move.fromWhere].howManyChips == 0: # no chips on requested space
			return False

		# make sure the owner is not moving onto a spot owned by the opponent

		if self.spaceList[move.toWhere].howManyChips >= 2 and self.spaceList[move.toWhere].spaceOwner() != move.color:
			return False

		# make sure the owner is not moving pieces outside of the barriers of the board.
		if 0 <= move.toWhere <= 23 == False:
			return False

		# make sure pieces are not on the bar while move is being made
		if move.fromWhere != 'bar' and move.color in self.chipsOnBar:
			return False

		# make sure roll is consistent with the move made.
		moveDistance = abs(move.fromWhere - move.toWhere)
		if moveDistance not in self.roll:
			return False

		# make sure that the owner is moving pieces that belong to him.
		if move.color != self.spaceList[move.fromWhere].spaceOwner:
			return False

		# make sure player has all of his chips in home base before moving chips off

		if move.toWhere == 'offboard':


			homeBase = range(6) if move.color == self.pieceColorA else range(18,24)

			for space in self.spaceList:
				if space.index not in homeBase and space.spaceOwner == move.color:
					return False

		return True
