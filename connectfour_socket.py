### Connect Four socket connections ###

from collections import namedtuple
import socket

GameConnect = namedtuple('GameConnect', ['socket', 'input', 'output'])

class GameConnectError(Exception):
    pass


def connect(host: str, port: int) -> GameConnect:
    '''Attempts to connect to the connect four server, given the host
        and the port and returns a GameConnect stating describing whether
        the connection is successful or not.'''
    c4_socket = socket.socket()
    c4_socket.connect((host, port))

    c4_input = c4_socket.makefile('r')
    c4_output = c4_socket.makefile('w')

    return GameConnect(c4_socket, c4_input, c4_output)
                         
### Game initialization protocol
def greetings(connection: GameConnect) -> str:
    '''Handles the opening protocol messages between the server and client.'''
    username = input('Username: ')
    _write_line(connection, 'I32CFSP_HELLO '+ username)
    
    response = _read_line(connection)
    if response == 'WELCOME '+username:           
        return response
    else:
        connection.socket.close()
        print('Closed connection due to improper server action.')

def initialize(connection: GameConnect) -> None:
    '''Sends protocol message after initial greeting.'''
    _write_line(connection, 'AI_GAME')
    response = _read_line(connection)
    if response != 'READY':
        raise GameConnectError()


### In-game client-server dialogue
def message_turn(connection: GameConnect, action: str, col_num: int) -> str:  
    '''Sends information to the server of the move made by the user'''
    message = '{} {}'.format(action, col_num)
    _write_line(connection, message)

def receive_message(connection: GameConnect) -> str:
    '''Receives information of the server's move and checks if server messages follow the
       protocol.'''
    message = _read_line(connection)
    if message == 'WINNER_RED':
        return message
    
    elif message == 'INVALID':
        _handle_ready_message(connection)
        return message
    

    elif message == 'OKAY':
        turn_message = _read_line(connection)
        _handle_ready_message(connection)
        return turn_message
   
    
    else:
        connection.socket.close()
        print('Connection closed due to improper server action.')
        

#Handles 'READY' message piece of the protocol
def _handle_ready_message(connection: GameConnect):
    message = _read_line(connection)
    if message != 'READY' and message != 'WINNER_YELLOW':
        connection.socket.close()
        print('Connection closed due to improper server action.')


    
### Message handlers
def _read_line(connection: GameConnect) -> str:
    '''Reads a line sent from the server and takes out the newline at the end
       of it.'''
    rcvd_line = connection.input.readline()
    line = rcvd_line[:-1]
    return line
    


def _write_line(connection: GameConnect, line: str) -> None:
    '''Writes line from the client to the server.'''
    connection.output.write(line + '\r\n')
    connection.output.flush()


    

