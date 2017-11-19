### LOCAL GAMEPLAY ###

import connectfour_gameplay
import connectfour

def local_gameplay():
    '''Runs the Connect Four game on the user interface.'''
    game_state = connectfour.new_game()
    x = 0
    connectfour_gameplay.numbers(x)
    connectfour_gameplay.dot_rows(game_state)
    connectfour_gameplay.name_turn(game_state)
    while True:
        game_state = connectfour_gameplay.turn(game_state)
        connectfour_gameplay.numbers(x)
        connectfour_gameplay.dot_rows(game_state)
        x = connectfour.winner(game_state)
        if x == connectfour.NONE:
            pass
        elif x == connectfour.RED:
            print ('GAME OVER. The winner is red.')
            break
        elif x == connectfour.YELLOW:
            print ('GAME OVER. The winner is yellow.')
            break
        connectfour_gameplay.name_turn(game_state)


        

if __name__ == '__main__':
    print('WELCOME TO CONNECT FOUR')
    print('Version: Local')
    local_gameplay()
    
    
