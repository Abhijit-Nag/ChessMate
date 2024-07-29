import socket
import pickle
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address= ('localhost', 12345)
server_socket.bind(server_address)

print("Server is started now.")
server_socket.listen(2)
print("Server is listening now..")
print("Waiting for the connections...")

clients=[]

turn=0

white_pieces= ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
               'pawn', 'pawn', 'pawn', 'pawn', 'pawn','pawn', 'pawn', 'pawn']

white_locations=[(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                 (0,1), (1,1), (2,1), (3, 1), (4,1), (5,1), (6,1), (7,1)]

black_pieces= ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
               'pawn', 'pawn', 'pawn', 'pawn', 'pawn','pawn', 'pawn', 'pawn']


black_locations=[(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7),
                 (0,6), (1,6), (2,6), (3, 6), (4,6), (5,6), (6,6), (7,6)]
turn_step =0

player='white'

def handle_client(client_socket, client_number):
    try:
        while True:
            message_recv= client_socket.recv(4096)
            message_recv=pickle.loads(message_recv)
            white_locations= message_recv[0]
            black_locations= message_recv[1]
            white_pieces= message_recv[2]
            black_pieces= message_recv[3]
            turn_step= message_recv[4]
            captured_pieces_white= message_recv[5]
            captured_pieces_black= message_recv[6]
            two_moved_white_pawns= message_recv[7]
            two_moved_black_pawns= message_recv[8]
            stalemate= message_recv[9]

           
            game_on = False
            
            if len(clients)>1:
                game_on= True

            for i in range(len(clients)):
                if i == 0:
                    clients[i].sendall(pickle.dumps((white_locations, black_locations, white_pieces, black_pieces, turn_step, 'white', captured_pieces_white, captured_pieces_black, two_moved_white_pawns, two_moved_black_pawns, stalemate, game_on)))
                else:
                    clients[i].sendall(pickle.dumps((white_locations, black_locations, white_pieces, black_pieces, turn_step, 'black', captured_pieces_white, captured_pieces_black, two_moved_white_pawns, two_moved_black_pawns, stalemate, game_on)))
                    
    except Exception as e:
        print("Server-side error while handling client: ", e)
    finally:
        server_socket.close()


try:
    for client in range(2):
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, client)).start()
except Exception as e:
    print("Server-side error: ", e)
finally:
    server_socket.close()
