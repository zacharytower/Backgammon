'''
function takes in board state, color and roll and produces all the possible moves that could be made.
'''
import bgmove

def possibleStates(board, color, roll):

    assert type(roll) != int, 'roll must be iterable.'
    roll = list(roll)
    if board.pieceColorA == color: downwards = -1
    else: downwards = 1

    moveList = []
    for space in board:

        for r in roll:
            move = bgmove.BGMove(roll = r, color = color, 
                fromWhere = space.index, toWhere = space.index + (r * downwards), rollDict = {}, 
                ignoreRollDict = True) # ignore roll Dict

            print move
            raw_input()
            if board.makeMove(move) == -1:
                continue
            else:

                if len(roll) == 1:
                    moveList.append(move)

                else:
                    roll.remove(r)
                    for m in possibleStates(board, color,roll):
                        moveList.append((move,m))
                    roll.add(r)

    return moveList

