### ONLINE GAMEPLAY ###

import connectfour_gameplay
import connectfour_socket
import connectfour

def prompt_connection() -> 'Connection':
    '''Prompts user to enter host and port number. Used at the start of the
       online version of the game. True and False indicates whether the
       connection is successful or not''' 
    host = input('Please enter a hostname: ')
    host_name = host.strip()
    while True:
        try:
            port_number = int(input('Please enter a port number: '))
            break
        except:
            print('Please enter a valid port number')

    try:
        connection = connectfour_socket.connect(host_name, port_number)
        return connection
    except:
        print('...Unable to connect with the game server at this time.')


def red_turn(game_state: connectfour.GameState, connection: connectfour_socket.GameConnect) -> connectfour.GameState:
    '''Takes user input from the client, prompting whether to drop or
       pop and handles the turns sequence.'''
    while True:
        turn = (input('Drop or Pop?: '))
        action = turn.upper()
        if action == 'DROP':       
            try: 
                col_num = int(input('Column to drop between 1-7: '))
            except:
                print('Please enter a valid column number.')
            else:
                if 1 <= col_num <= 7:                   
                    game = connectfour.drop(game_state, col_num-1)
                    message = '{} {}'.format(action, col_num)
                    print(message)
                    connectfour_socket._write_line(connection, message)
                    if not connectfour.InvalidMoveError:
                        print('Column is too full to drop')
                    else:
                        break
                else:
                    print('Invalid move')
        elif action == 'POP':
            try:
                col_num = int(input('Column to pop between 1-7: '))
            except:
                print('Please enter a valid column number.')
            else:
                if 1 <= col_num <= 7:               
                    try:
                        game = connectfour.pop(game_state, col_num-1)
                        message = '{} {}'.format(action, col_num)
                        connectfour_socket._write_line(connection, message)
                        if not connectfour.InvalidMoveError:
                            print('Cannot pop at '+str(col_num))
                        else:
                            break
                    except:
                        print('Cannot pop at '+str(col_num))
                else:
                    print('Invalid move')

    return game


def yellow_turn(game_state: connectfour.GameState, connection: connectfour_socket.GameConnect) -> connectfour.GameState:
    '''Takes input from the server and handles turn sequence.'''
    turn_message = connectfour_socket.receive_message(connection)
    message_split = turn_message.split()
    action = message_split[0]
    col_num = int(message_split[-1])
    print("Yellow's move: {} {}".format(action, col_num))
    print()
    if action == 'DROP':       
        game = connectfour.drop(game_state, col_num-1)
        if not connectfour.InvalidMoveError:
            connection.socket.close()
            print('Game connection closed due to improper server action.')
        else:
            pass
    elif action == 'POP':
        game = connectfour.pop(game_state, col_num-1)
        message = '{} {}'.format(action, col_num)
        connectfour_socket._write_line(connection, message)
        if not connectfour.InvalidMoveError:
            connection.socket.close()
            print('Game connection closed due to improper server action.')
        else:
            pass

    else:
        connection.socket.close()
        print('Game connection closed due to improper server action.')

    return game



def online_gameplay(connection: connectfour_socket.GameConnect):
    '''Runs the Connect Four game on the user interface.'''
    game_state = connectfour.new_game()
    x = 0
    connectfour_gameplay.numbers(x)
    connectfour_gameplay.dot_rows(game_state)
    while True:
        x = connectfour_gameplay.name_turn(game_state)
        if x == connectfour.RED:
            game_state = red_turn(game_state, connection)
            connectfour_gameplay.numbers(x)
            connectfour_gameplay.dot_rows(game_state)
            x = connectfour.winner(game_state)
        elif x == connectfour.YELLOW:
            game_state = yellow_turn(game_state, connection)
            connectfour_gameplay.numbers(x)
            connectfour_gameplay.dot_rows(game_state)
            x = connectfour.winner(game_state)
        elif x == connectfour.NONE:
            print('hi')
            
        
        if x == connectfour.NONE:
            continue
        elif x == connectfour.RED:
            print ('GAME OVER. The winner is red.')
            break
        elif x == connectfour.YELLOW:
            print ('GAME OVER. The winner is yellow player.')
            break
        connectfour_gameplay.name_turn(game_state)
    






if __name__ == '__main__':
    connection = prompt_connection()
    if connection == None:
        print('Connection closed.')
    else:
        connectfour_socket.greetings(connection)
        connectfour_socket.initialize(connection)
        print('WELCOME TO CONNECT FOUR')
        print('Version: Online')
        online_gameplay(connection)


    
        
