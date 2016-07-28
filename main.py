import pygame, sys, random, time, copy
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

RANDCOLOR1, RANDCOLOR2 = [tuple([random.randint(0,255) for x in range(3)]) for y in range(2)]

CORNFLOWERBLUE = (100,149,237)
LIGHTCORK = (187, 138, 85)

# define color scheme
colorScheme =  {'pieceColorA' : N_RED,
'pieceColorB' : N_GREEN, 
'dieColorA': {'cube':N_RED, 'pip':WHITE},
'dieColorB':{'cube':N_GREEN,'pip':WHITE},
'backgroundColor': LIGHTCORK, 
'spaceColorA': N_YELLOW, 
'spaceColorB':N_BLUE,
'boarderColor': CORNFLOWERBLUE, 
'messageBoxColor':BLACK, 
'messageTextColor':WHITE, 
'holderColor':LIGHTCORK,
'chipBoarderColor':BLACK}


FPS = 60
FPSCLOCK = pygame.time.Clock() # initializes FPS clock object.

pygame.display.set_caption('Backgammon') # sets the title of the application.

pygame.init() # initiates pygame

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
	tie = False

	board.message = "Roll off! Click"
	
	while True:

		DISPLAYSURF.fill(WHITE) # fill the screen white
		board.displayBoard() # display the board onto the screen

		
		if holdingChip == True: # if the player is currently dragging a piece
			pygame.draw.circle(DISPLAYSURF, colorScheme['pieceColorA'], pygame.mouse.get_pos(),25) # makes player's cursor a chip.

		for event in pygame.event.get():

			if event.type == QUIT:
				pygame.quit() # quit pygame
				sys.exit() # terminate

			if event.type == MOUSEBUTTONDOWN: # mouse button is clicked down

				if board.rollOff == True and assembledRole == None: # player clicked and the roll-off was occurring:
					board.rollA, board.rollB = [random.randint(1,6) for x in range(2)]
					board.diceRolled = True

					if board.rollA > board.rollB: # player wins
						board.message = 'You win the roll-off!'
						assembledRole = {board.rollA:False,board.rollB:False}
						
						tie = False
						
						
					elif board.rollB > board.rollA: # computer wins
						board.message = 'Sorry! You lose the roll-off.'

						DISPLAYSURF.fill(WHITE) # fill the screen white
						board.displayBoard() # display the board onto the screen
						pygame.display.update()
						time.sleep(1)

						for m in opponentCPU.bogoMove((board.rollA, board.rollB), copy.deepcopy(board)):
							
							print m
							board.makeMove(m)

							DISPLAYSURF.fill(WHITE) # fill the screen white
							board.displayBoard() # display the board onto the screen
							pygame.display.update()

							time.sleep(1)

						board.rollA, board.rollB = None, None
						board.diceRolled = False

						board.rollOff = False
						tie = False

					else: # there is a tie:
						board.message = 'A tie has occurred! roll again.'
						tie = True

					pygame.display.update()
					#for i,y in enumerate(range(chipY, chipY + 750 + 1,50 if top else -50)):
					'''
					if board.rollOff == True and tie == False: 
						board.rollOff = False
						board.message = '''

					break

				elif board.diceRolled == False: # the player has yet to role the dice:
					

					board.rollA, board.rollB = [random.randint(1,6) for x in range(2)]

					board.diceRolledColor = colorScheme['pieceColorA']
					board.diceRolled = True # makes it so that the board displays the dice as being rolled

					if board.rollA == board.rollB: # player rolled doubles:
						doubles = True
						doubleCount = 4

						assembledRole = {1:False}

					else:
						assembledRole = {board.rollA:False, board.rollB:False}

				else:
					p = board.getClickedSpace(event.pos, True) # see if any chips were clicked
					
					if p != -1 and p != None: # valid space clicked:

						if p == 'bar':
							# remove one of a's pieces from the bar
							board.removeChipFromBar(colorScheme['pieceColorA'])

						
						holdingChip = True

			if event.type == MOUSEBUTTONUP: # player releases the mouse button

				if p != -1 and p != None: # player was making a move

					q = board.getClickedSpace(event.pos) # finds the spot that was landed on

					if q == -1 or q == None: # if the player made an incomplete move:
						p = None

					else: # if the player made a completed move:

						if p == 'bar': # player is moving off the board
							rollMove = 24 - q # always moving off the bar at the top of the board.

						elif q == 'offboard': # player is moving off the board:
							rollMove = p + 1
						else:
							rollMove = abs(p-q)
						'''
						incorrectMove = False
						if rollMove not in [board.rollA, board.rollB]:
							incorrectMove = True

						if assembledRole[rollMove] == True: # move already used
							incorrectMove = True

						if incorrectMove == False:'''
						moveObject = bgmove.BGMove(rollMove, colorScheme['pieceColorA'], p, q, assembledRole)
						
						ev = board.makeMove(moveObject)

						if ev == -1: # move made was invalid:
							p = None
							q = None

							#board.makeMove(moveObject.moveInverse()) # undoes the move

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
								
								if board.rollOff == True: board.rollOff = False
								doubles = False
								
								
								# its time for the computer:
								board.diceRolled = False
								board.rollA, board.rollB = None, None

								board.rollA, board.rollB = [random.randint(1,6) for x in range(2)]
								board.diceRolledColor = colorScheme['pieceColorB']
								board.diceRolled = True

								DISPLAYSURF.fill(WHITE) # fill the screen white
								board.displayBoard() # display the board onto the screen

								pygame.display.update()
								FPSCLOCK.tick(FPS)

								time.sleep(2)


								if board.rollA == board.rollB:
									t = 2

								else:
									t = 1

								for x in range(t):
									for i, move in enumerate(opponentCPU.bogoMove((board.rollA, board.rollB), copy.deepcopy(board))):

										if i == 2: break
										
										board.makeMove(move)

										
										
										DISPLAYSURF.fill(WHITE) # fill the screen white
										board.displayBoard() # display the board onto the screen

										pygame.display.update()
										FPSCLOCK.tick(FPS)
										time.sleep(1.5)

								#print 'Opponent done!'

								p = None
								q = None

								if board.hasWon(colorScheme['pieceColorB']): # human player has lost
									board.message = 'You lost!'
									pygame.display.update()

									time.sleep(5)

									board.resetBoard()

								board.diceRolled = False

						holdingChip = False

		

		pygame.display.update()
		FPSCLOCK.tick(FPS)

if __name__ == '__main__':
	'''
	o = bgplayer.BGPlayer(colorScheme['pieceColorB'])

	b = bgboard.BGBoard(colorScheme)

	roll = (4,3)

	print o.bogoMove(roll,b)
	print b
	'''
	main()