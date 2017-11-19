### Game user interface ###

import connectfour

def numbers(x: int) -> int:
    '''Prints numbers on top of the columns of the game board.'''
    for x in range(1, connectfour.BOARD_COLUMNS+1):
        print(x, end = " ")
    print("")



def dot_rows(game_state: connectfour.GameState) -> 'GameState':
    '''Shows the game board by reflecting the GameState.'''
    string = ''
    y = game_state.turn
    for row in range(connectfour.BOARD_ROWS):
        for col in range(connectfour.BOARD_COLUMNS):
            if game_state.board[col][row] == 0:
                string += ". "
            elif game_state.board[col][row] == 1:
                string += "R "
            elif game_state.board[col][row] == 2:
                string += "Y "
        string += "\n"
    print(string)

def name_turn(game_state: connectfour.GameState) -> connectfour.GameState:
    '''Declares the current player's turn.'''
    if game_state.turn == connectfour.RED:
        print('Red player\'s turn\n')
    elif game_state.turn == connectfour.YELLOW:
        print('Yellow player\'s turn\n')

    return game_state.turn


          
def turn(game_state: connectfour.GameState) -> connectfour.GameState:
    '''Takes user input, prompting whether to drop or
        pop and handles the turns sequence.'''
    while True:
        turn = (input('Drop or Pop?: '))
        if turn.upper() == 'DROP':       
            try: 
                col_num = int(input('Column to drop between 1-7: '))
            except:
                print('Please enter a valid column number.')
            else:
                if 1 <= col_num <= 7:
                    try:
                        game = connectfour.drop(game_state, col_num-1)
                        if not connectfour.InvalidMoveError:
                            print('Column is too full to drop')
                        else:
                            break
                    except:
                        print('Column too full to drop.')
                else:
                    print('Invalid move')
        elif turn.upper() == 'POP':
            try:
                col_num = int(input('Column to pop between 1-7: '))
            except:
                print('Please enter a valid column number.')
            else:
                if 1 <= col_num <= 7:               
                    try:
                        game = connectfour.pop(game_state, col_num-1)
                        if not connectfour.InvalidMoveError:
                            print('Cannot pop at '+str(col_num))
                        else:
                            break
                    except:
                        print('Cannot pop at '+str(col_num))
                else:
                    print('Invalid move')
    return game
                

