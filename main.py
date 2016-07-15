import pygame, sys, random, time
from pygame.locals import *

from global_vars import *
import bgspace 
import bgboard 
import bgplayer 
import bgmove

# define colors

RED = 	(255,  0,  0)
BLUE =  (  0,  0,255)
GREEN = (  0,255,  0)
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
N_RED = (232, 14,116)
N_GREEN=( 14,232,130)
N_BLUE =( 21, 14,232)
N_YELLOW = (225,232,14)

CORNFLOWERBLUE = (100,149,237)
LIGHTCORK = (187, 138, 85)

# define color scheme
colorScheme =  {'pieceColorA' : N_RED,
'pieceColorB' : N_GREEN, 
'dieColorA': {'cube':N_RED, 'pip':WHITE},
'dieColorB':{'cube':N_GREEN,'pip':WHITE},
'backgroundColor': LIGHTCORK, 
'spaceColorA': N_RED, 
'spaceColorB':N_GREEN,
'boarderColor': CORNFLOWERBLUE, 
'messageBoxColor':BLACK, 
'messageTextColor':WHITE, 
'holderColor':LIGHTCORK,
'chipBoarderColor':BLACK}


FPS = 60
FPSCLOCK = pygame.time.Clock()

pygame.display.set_caption('Backgammon')

pygame.init()

def main():

	board = bgboard.BGBoard(colorScheme)
	opponentCPU = bgplayer.BGPlayer(color = colorScheme['pieceColorB'])
	p = None
	q = None

	board.rollOff = True # used for the first move rolling procedure
	waitingForPlayerClick = False # wait for the player to click the board to role
	assembledRole = None
	doubles = False
	doubleCount = 0
	holdingChip = False

	while True:

		DISPLAYSURF.fill(WHITE) # fill the screen white
		board.displayBoard() # display the board onto the screen

		if holdingChip == True: # if the player is currently dragging a piece
			pygame.draw.circle(DISPLAYSURF, colorScheme['pieceColorA'], pygame.mouse.get_pos(),25) # makes player's cursor a chip.


		if board.rollOff == True: # first roll-off
			board.message = 'It\'s the roll-off!\nClick anywhere to roll your die.'


		for event in pygame.event.get():

			if event.type == QUIT:
				pygame.quit() # quit pygame
				sys.exit() # terminate

			if event.type == MOUSEBUTTONDOWN: # mouse button is clicked down

				if board.rollOff == True: # player clicked and the roll-off was occurring:
					board.rollA, board.rollB = [random.randint(1,6) for x in range(2)]

					if board.rollA > board.rollB: # player wins
						board.message = 'You win the roll-off!'
						assembledRole = {board.rollA:False,board.rollB:False}
						break
						
					elif board.rollB > board.rollA: # computer wins
						board.message = 'Sorry! You lose the roll-off.'
						pygame.display.update()
						time.sleep(2)

						for m in opponentCPU.bogoMove((board.rollA, board.rollB), board):
							board.makeMove(m)

						

					else: # there is a tie:
						board.message = 'A tie has occurred! roll again.'

				if assembledRole == None: # the player has yet to role the dice:
					board.diceRolled = True # makes it so that the board displays the dice as being rolled
					board.diceRolledColor = colorScheme['pieceColorA']

					board.rollA, board.rollB = [random.randint(1,6) for x in range(2)]

					if board.rollA == board.rollB: # player rolled doubles:
						doubles = True
						doubleCount = 4

					else:
						assembledRole = {board.rollA:False, board.rollB:False}

				p = board.getClickedSpace(event.pos, True) # see if any chips were clicked

				if p != -1: # valid space clicked:

					if p == 'bar':
						# remove one of a's pieces from the bar
						board.removeChipFromBar(colorScheme['pieceColorA'])

					else:
						board.spaceList[p].removeOne()

					pygame.mouse.set_visible(False)
					holdingChip = True

			if event.type == MOUSEBUTTONUP: # player releases the mouse button

				if p != None: # player was making a move

					q = board.getClickedSpace(event.pos) # finds the spot that was landed on

					if q == None: # if the player made an incomplete move:
						holdingChip = False
						p = None

					else: # if the player made a completed move:

						moveObject = bgmove.BGMove(abs(p-q), colorScheme['pieceColorA'], p, q)

						ev = board.makeMove(moveObject)

						if ev == -1: # move made was invalid:
							p = None
							q = None

							board.makeMove(moveObject.moveInverse()) # undoes the move

							board.message = 'Invalid move!'

						else: #player made a completed, valid move:

							if doubles == False:

								assembledRole[moveObject.roll] = True

							else: # player rolled doubles
								doubleCount -= 1

							if board.hasWon(colorScheme['pieceColorA']): # color has won

								board.message = 'You have won!'
								pygame.display.update()
								time.sleep(5)

								board.message = None

								board.resetBoard()

							if (doubles == True and doubleCount == 0) or all(assembledRole.values()): # player has used up all of his moves

								if rollOff == True: rollOff = False
								# its time for the computer:
								board.diceRolled = False
								board.rollA, board.rollB = None, None

								'''
								firstTime = time.time() # seconds since epoch

								while time.time() < firstTime + 2:
									DISPLAYSURF.fill(WHITE) # fill the screen white
									board.displayBoard() # display the board onto the screen

									pygame.display.update()
									FPSCLOCK.tick(FPS)'''

								board.rollA, board.rollB = [random.randint(1,6) for x in range(2)]
								board.diceRolled = True
								board.diceRolledColor = colorScheme['pieceColorB']

								for move in opponentCPU.bogoMove((board.rollA, board.rollB), board):
									board.move(move)

									firstTime = time.time() # seconds since epoch
									while time.time() < firstTime + 1:
										DISPLAYSURF.fill(WHITE) # fill the screen white
										board.displayBoard() # display the board onto the screen

										pygame.display.update()
										FPSCLOCK.tick(FPS)

								if board.hasWon(colorScheme['pieceColorB']): # human player has lost
									board.message = 'You lost!'
									pygame.display.update()

									time.sleep(5)

									board.resetBoard()

								board.diceRolled = False

		pygame.display.update()
		FPSCLOCK.tick(FPS)

if __name__ == '__main__':
	'''
	o = bgplayer.BGPlayer(colorScheme['pieceColorB'])

	b = bgboard.BGBoard(colorScheme)

	roll = (4,3)

	print o.bogoMove(roll,b)'''

	main()