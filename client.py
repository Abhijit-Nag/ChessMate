import socket
import threading
import pickle
import pygame
import copy


pygame.init()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)

client_socket.connect(server_address)
print("You're now connected to the server.")


thread_state_lock = threading.Lock()

player =''

white_options =[]
black_options=[]

game_over = False
winner = ""
initial_position=(0,0)

def recv_message():
    global white_locations
    global black_locations
    global white_pieces
    global black_pieces
    global turn_step
    global player
    global captured_pieces_white
    global captured_pieces_black
    global black_options
    global white_options
    global two_moved_white_pawns
    global two_moved_black_pawns
    global stalemate
    try:
        while True:
            response = client_socket.recv(4096)
            response= pickle.loads(response)
            temp_white_locations= response[0]
            temp_black_locations= response[1]
            white_pieces= response[2]
            black_pieces= response[3]
            turn_step= response[4]
            player= response[5]
            captured_pieces_white = response[6]
            captured_pieces_black = response[7]
            two_moved_white_pawns= response[8]
            two_moved_black_pawns= response[9]
            stalemate= response[10]

            
            white_locations= temp_white_locations
            black_locations= temp_black_locations
            print(white_locations)
            print(black_locations)

            black_options= check_options(black_pieces, black_locations, 'black', black_locations, white_locations)
            white_options= check_options(white_pieces, white_locations, 'white', black_locations, white_locations)
            
    except Exception as e:
        print("Client-side error: ", e)
    finally:
        client_socket.close()

def alterBoard(white_locations, black_locations):
    alternate_white_locations= []
    alternate_black_locations= []
    for pos in white_locations:
        alternate_white_locations.append((7-pos[0], 7-pos[1]))
    for pos in black_locations:
        alternate_black_locations.append((7-pos[0], 7-pos[1]))
    white_locations=alternate_white_locations
    black_locations=alternate_black_locations
        
threading.Thread(target=recv_message, args=()).start()


WIDTH = 900
HEIGHT = 765

screen= pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Chess!')
font= pygame.font.Font('freesansbold.ttf', 20)
big_font = pygame.font.Font('freesansbold.ttf', 40)

timer= pygame.time.Clock()
fps = 60

# game variables and images


white_pieces= ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
               'pawn', 'pawn', 'pawn', 'pawn', 'pawn','pawn', 'pawn', 'pawn']

white_locations=[(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                 (0,1), (1,1), (2,1), (3, 1), (4,1), (5,1), (6,1), (7,1)]

black_pieces= ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
               'pawn', 'pawn', 'pawn', 'pawn', 'pawn','pawn', 'pawn', 'pawn']


black_locations=[(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7),
                 (0,6), (1,6), (2,6), (3, 6), (4,6), (5,6), (6,6), (7,6)]


captured_pieces_white =[]
captured_pieces_black =[]

turn_step =0
selection= 100

valid_moves= []

two_moved_white_pawns=[0,0,0,0,0,0,0,0]
two_moved_black_pawns=[0,0,0,0,0,0,0,0]

white_promotion= False
black_promotion = False
promo_index = 100

white_promotion_pieces=['bishop', 'knight', 'rook', 'queen']
black_promotion_pieces=['bishop', 'knight', 'rook', 'queen']

white_king_side_rook_moved= False
white_queen_side_rook_moved= False
black_king_side_rook_moved= False
black_queen_side_rook_moved= False

white_king_moved= False
black_king_moved= False

draw_type=""

stalemate= False


# load in game piece images (queen, king, rook, bishop, knight, pawn)

black_queen= pygame.image.load('./assets/black_queen.png')
black_queen = pygame.transform.scale(black_queen, (60, 60))
black_queen_small = pygame.transform.scale(black_queen, (35,35))
white_queen= pygame.image.load('./assets/white_queen.png')
white_queen = pygame.transform.scale(white_queen, (60, 60))
white_queen_small = pygame.transform.scale(white_queen, (35,35))
black_king= pygame.image.load('./assets/black_king.png')
black_king = pygame.transform.scale(black_king, (60, 60))
black_king_small = pygame.transform.scale(black_king, (35,35))
white_king= pygame.image.load('./assets/white_king.png')
white_king = pygame.transform.scale(white_king, (60, 60))
white_king_small = pygame.transform.scale(white_king, (35,35))
black_rook= pygame.image.load('./assets/black_rook.png')
black_rook = pygame.transform.scale(black_rook, (60, 60))
black_rook_small = pygame.transform.scale(black_rook, (35,35))
white_rook= pygame.image.load('./assets/white_rook.png')
white_rook = pygame.transform.scale(white_rook, (60, 60))
white_rook_small = pygame.transform.scale(white_rook, (35,35))
black_bishop= pygame.image.load('./assets/black_bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (60, 60))
black_bishop_small = pygame.transform.scale(black_bishop, (35,35))
white_bishop= pygame.image.load('./assets/white_bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (60, 60))
white_bishop_small = pygame.transform.scale(white_bishop, (35,35))
black_knight= pygame.image.load('./assets/black_knight.png')
black_knight = pygame.transform.scale(black_knight, (60, 60))
black_knight_small = pygame.transform.scale(black_knight, (35,35))
white_knight= pygame.image.load('./assets/white_knight.png')
white_knight = pygame.transform.scale(white_knight, (60, 60))
white_knight_small = pygame.transform.scale(white_knight, (35,35))
black_pawn= pygame.image.load('./assets/black_pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (55, 55))
black_pawn_small = pygame.transform.scale(black_pawn, (35,35))
white_pawn= pygame.image.load('./assets/white_pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (60, 60))
white_pawn_small = pygame.transform.scale(white_pawn, (35,35))

white_images=[white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images=[white_pawn_small, white_queen_small, white_king_small, white_knight_small, white_rook_small, white_bishop_small]
black_images=[black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images=[black_pawn_small, black_queen_small, black_king_small, black_knight_small, black_rook_small, black_bishop_small]

piece_list =['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

# check variables/ flashing counter
counter = 0


# draw main game board

def draw_board():
    for i in range(32):
        col= i%4
        row= i // 4

        if row % 2 ==0:
            pygame.draw.rect(screen, (255,255,255), [480- (col * 160), row*80, 80, 80])
        else:
            pygame.draw.rect(screen, (255,255,255), [560- col*160, row*80, 80, 80])

        
        for i in range(9):
            pygame.draw.line(screen, (0,0,0), (0, 80*i), (640, 80*i),2)
            pygame.draw.line(screen, (0,0,0), (80*i, 0), (80*i, 640),2)

        pygame.draw.rect(screen, 'gray', [0,640, 700, 80])
        pygame.draw.rect(screen, 'gray', [640,0, 60, HEIGHT])
        pygame.draw.rect(screen, 'gold', [0,640, 640, HEIGHT-640],5)
        pygame.draw.rect(screen, 'gold', [640, 0, WIDTH-640, HEIGHT],5)

        status_text= ['White: Select a Piece to Move!', 'White: Select a Destination!', 'White: Select piece to promote',
                      'Black: Select a Piece to Move!', 'Black: Select a Destination!', 'Black: Select piece to promote']

        for i in range(len(status_text)):
            if player=='white':
                if turn_step<=2:
                    screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 680))
                else:
                    screen.blit(big_font.render('Opponents turn!', True, 'black'), (20, 680))
            else:
                if turn_step>2:
                    screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 680))
                else:
                    screen.blit(big_font.render('Opponents turn!', True, 'black'), (20, 680))


        # screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 680))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0,80*i), (640, 80*i), 2)
            pygame.draw.line(screen, 'black', (80*i, 0), (80*i, 640), 2)



# draw pieces onto board

def draw_pieces():
    for i in range(len(white_pieces)):
        try:
            index = piece_list.index(white_pieces[i])
        except IndexError:
            print("Index error.")

        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 80+10 , white_locations[i][1] *80+10))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 80 + 10, white_locations[i][1] *80 +10))
        if turn_step<2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] *80+1, white_locations[i][1]*80 +1, 80, 80], 2)
    
    for i in range(len(black_pieces)):
        try:
            index = piece_list.index(black_pieces[i])
        except:
            print("Index error.")

        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 80 + 10, black_locations[i][1] *80 +10))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 80 + 10, black_locations[i][1] *80 +10))
        
        if turn_step>=2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] *80+1, black_locations[i][1]*80 +1, 80, 80], 2)


# draw for white player board
def draw_board_opposite():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])

        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, ((7-white_locations[i][0]) * 80+10 , (7-white_locations[i][1]) *80+10))
        else:
            screen.blit(white_images[index], ((7-white_locations[i][0]) * 80 + 10, (7-white_locations[i][1]) *80 +10))
        if turn_step<2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [(7-white_locations[i][0]) *80+1, (7-white_locations[i][1])*80 +1, 80, 80], 2)
    
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])

        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, ((7-black_locations[i][0]) * 80 + 10, (7-black_locations[i][1]) *80 +10))
        else:
            screen.blit(black_images[index], ((7-black_locations[i][0]) * 80 + 10, (7-black_locations[i][1]) *80 +10))
        
        if turn_step>=2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [(7-black_locations[i][0]) *80+1, (7-black_locations[i][1]*80) +1, 80, 80], 2)
    

# function to check all pieces valid options on board


# check valid pawn moves          
def check_pawn(position, color, black_locations, white_locations):

    moves_list=[]
    if color == 'white':
        if(position[0], position[1]+1) not in white_locations and (position[0], position[1]+1) not in black_locations and position[1]<7:
            moves_list.append((position[0], position[1]+1))
        if(position[0], position[1]+2) not in white_locations and (position[0], position[1]+1) not in white_locations and (position[0], position[1]+1) not in black_locations and (position[0], position[1]+2) not in black_locations and position[1]==1:
            moves_list.append((position[0], position[1]+2))
        if(position[0]+1, position[1]+1) in black_locations:
            moves_list.append((position[0]+1, position[1]+1))
        if(position[0]-1, position[1]+1) in black_locations:
            moves_list.append((position[0]-1, position[1]+1))
        if(position[1] == 4):
            if(position[0]>0):
                # check for the left hand side pawn if exists
                if ((position[0]-1, position[1]) in black_locations) :
                    index= black_locations.index((position[0]-1, position[1]))
                    piece= black_pieces[index]
                    if piece=='pawn':
                        # en-passant may occur and now we have to check whether the opponent pawn if 2-moved or not
                        if two_moved_black_pawns[index-8] == 2 and (position[0]-1, position[1]+1) not in black_locations and (position[0]-1, position[1]+1) not in white_locations:
                            moves_list.append((position[0]-1, position[1]+1, 'en-passant'))
            if (position[0] <7) :
                # check for the right hand side pawn if exists
                if ((position[0]+1, position[1]) in black_locations) :
                    index= black_locations.index((position[0]+1, position[1]))
                    piece= black_pieces[index]
                    if piece=='pawn':
                        # en-passant may occur and now we have to check whether the opponent pawn if 2-moved or not
                        if two_moved_black_pawns[index-8]==2 and (position[0]+1, position[1]+1) not in black_locations and (position[0]+1, position[1]+1) not in white_locations:
                            moves_list.append((position[0]+1, position[1]+1, 'en-passant'))
    else:
        if(position[0], position[1]-1) not in white_locations and (position[0], position[1]-1) not in black_locations and position[1]>0:
            moves_list.append((position[0], position[1]-1))
        if(position[0], position[1]-2) not in white_locations and (position[0], position[1]-1) not in white_locations and (position[0], position[1]-1) not in black_locations and (position[0], position[1]-2) not in black_locations and position[1]==6:
            moves_list.append((position[0], position[1]-2))
        if(position[0]+1, position[1]-1) in white_locations:
            moves_list.append((position[0]+1, position[1]-1))
        if(position[0]-1, position[1]-1) in white_locations:
            moves_list.append((position[0]-1, position[1]-1))
        if(position[1] == 3):
            if(position[0]>0):
                # check for the left hand side pawn if exists
                if ((position[0]-1, position[1]) in white_locations) :
                    index= white_locations.index((position[0]-1, position[1]))
                    piece= white_pieces[index]
                    if piece=='pawn':
                        # en-passant may occur and now we have to check whether the opponent pawn if 2-moved or not
                        if two_moved_white_pawns[index-8] == 2 and (position[0]-1, position[1]-1) not in black_locations and (position[0]-1, position[1]-1) not in white_locations:
                            moves_list.append((position[0]-1, position[1]-1, 'en-passant'))
            if (position[0] <7) :
                # check for the right hand side pawn if exists
                if ((position[0]+1, position[1]) in white_locations) :
                    index= white_locations.index((position[0]+1, position[1]))
                    piece= white_pieces[index]
                    if piece=='pawn':
                        # en-passant may occur and now we have to check whether the opponent pawn if 2-moved or not
                        if two_moved_white_pawns[index-8]==2 and (position[0]+1, position[1]-1) not in black_locations and (position[0]+1, position[1]-1) not in white_locations:
                            moves_list.append((position[0]+1, position[1]-1, 'en-passant'))
    
    return moves_list




# perform en-passant

def perform_enpassant(move):
    if player=='white':
        white_locations[selection]=move
        try:
            b_l= black_locations.index((move[0], move[1]-1))
        except IndexError:
            print("not in the list.")
        captured_pieces_white.append(black_pieces[b_l])
        black_locations.pop(b_l)
        black_pieces.pop(b_l)
    else:
        black_locations[selection]= move
        try:
            w_l= white_locations.index((move[0], move[1]+1))
        except IndexError:
            print("not in the list.")
        captured_pieces_black.append(white_pieces[w_l])
        white_locations.pop(w_l)
        white_pieces.pop(w_l)


# check valid rook moves

def check_rook(position, color, black_locations, white_locations):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4): 
        path = True
        chain = 1
        if i == 0:
            x=0
            y=1
        elif i== 1:
            x=0
            y=-1
        elif i==2:
            x=1
            y=0
        else:
            x=-1
            y=0
        while path:
            if  (position[0] + (chain * x), position[1]+(chain * y)) not in friends_list and 0<=position[0] + (chain *x) <= 7 and 0 <= position[1]+chain*y <=7 :
                moves_list.append((position[0]+ (chain *x), position[1] + (chain*y)))
                
                if(position[0] + (chain*x), position[1] +(chain*y)) in enemies_list:
                    path =False
                chain+=1
            else:
                path= False
    
    return moves_list


# check valid knight moves
def check_knight(position, color, black_locations, white_locations):
    moves_list= []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list= black_locations
        enemies_list= white_locations
    
    # 8 sqaures to check for knights, they can go two squares in one direction and one in another
    
    targets=[(1,2), (1,-2), (2,1),  (2,-1), (-1,2), (-1, -2), (-2, 1), (-2,-1)]

    for i in range(8):
        target = (position[0] + targets[i][0], position[1]+ targets[i][1])
        if target not in friends_list and 0<= target[0] <= 7 and 0<=target[1]<=7:
            moves_list.append(target)
    return moves_list


# check valid bishop moves
def check_bishop(position, color, black_locations, white_locations):
    moves_list =[]
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    
    for i in range(4):  #up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x=1
            y=-1
        elif i== 1:
            x=-1
            y=-1
        elif i==2:
            x=1
            y=1
        else:
            x=-1
            y=1
        while path:
            if  (position[0] + (chain * x), position[1]+(chain * y)) not in friends_list and 0<=position[0] + (chain *x) <= 7 and 0 <= position[1]+chain*y <=7 :
                moves_list.append((position[0]+ (chain *x), position[1] + (chain*y)))
                
                if(position[0] + (chain*x), position[1] +(chain*y)) in enemies_list:
                    path =False
                chain+=1
            else:
                path= False

    return moves_list


# check valid queen moves
def check_queen(position, color, black_locations, white_locations):
    moves_list = check_bishop(position, color, black_locations, white_locations)
    second_list = check_rook(position, color, black_locations, white_locations)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])

    return moves_list

# check valid king moves
def check_king(position, color, black_locations, white_locations):
    moves_list=[]
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    
    targets=[(1,0), (1,1), (1,-1),  (-1,0), (-1,1), (-1, -1), (0, 1), (0,-1)]
    castling_targets=[(-2,0),(2,0)]

    for i in range(8):
        target = (position[0] + targets[i][0], position[1]+ targets[i][1])
        if target not in friends_list and 0<= target[0] <= 7 and 0<=target[1]<=7:
            moves_list.append(target)
        if check_king_side_castle() == True:
            # castle_move= (position[0]+castling_targets[0][0], position[1]+ castling_targets[0][1])
            moves_list.append((position[0]+castling_targets[0][0], position[1]+ castling_targets[0][1], 'king-side-castle'))
        if check_queen_side_castle()== True:
            # castle_move= (position[0]+castling_targets[1][0], position[1]+ castling_targets[1][1])
            moves_list.append((position[0]+castling_targets[1][0], position[1]+ castling_targets[1][1], 'queen-side-castle'))
    return moves_list



def is_in_check(color, copy_white_locations, copy_white_pieces, copy_black_locations, copy_black_pieces):
    if color == 'white':
        king_location = copy_white_locations[copy_white_pieces.index('king')]
        print("white_locations: ", copy_white_locations)
        # opponent_options = copy_black_options
        opponent_options = check_options(copy_black_pieces, copy_black_locations, 'black', copy_black_locations, copy_white_locations)
    else:
        king_location = copy_black_locations[copy_black_pieces.index('king')]
        print("black locations: ", copy_black_locations)
        # opponent_options = copy_white_options
        opponent_options= check_options(copy_white_pieces, copy_white_locations, 'white', copy_black_locations, copy_white_locations)

    # return king_location in opponent_options
    res= False
    print("Opponent option: ", opponent_options)
    for option in opponent_options:
        # print(opponent_options.i)
        res= res or (king_location in option)
    return res


def check_king_side_castle():
    if player=='white':
        if white_king_side_rook_moved == False and white_king_moved== False:
            square_to_be_checked= [(1,0), (2,0), (3,0)]
            for sqaure in square_to_be_checked:
                for options in black_options:
                    if sqaure in options:
                        return False
            square_between_king_rook= [(1,0), (2,0)]
            for square in square_between_king_rook:
                if square in white_locations or square in black_locations:
                    return False
        else:
            return False
        return True
    else:
        if black_king_side_rook_moved == False and black_king_moved== False:
            square_to_be_checked= [(1,7), (2,7), (3,7)]
            for sqaure in square_to_be_checked:
                for options in white_options:
                    if sqaure in options:
                        return False
            square_between_king_rook= [(1,7), (2,7)]
            for square in square_between_king_rook:
                if square in white_locations or square in black_locations:
                    return False
        else:
            return False
        return True
    
def check_queen_side_castle():
    if player=='white':
        if white_queen_side_rook_moved == False and white_king_moved== False:
            square_to_be_checked= [(3,0), (4,0), (5,0)]
            for sqaure in square_to_be_checked:
                for options in black_options:
                    if sqaure in options:
                        return False
            square_between_king_rook= [(4,0), (5,0), (6,0)]
            for square in square_between_king_rook:
                if square in white_locations or square in black_locations:
                    return False
        else:
            return False
        return True
    else:
        if black_queen_side_rook_moved == False and black_king_moved== False:
            square_to_be_checked= [(3,7), (4,7), (5,7)]
            for sqaure in square_to_be_checked:
                for options in white_options:
                    if sqaure in options:
                        return False
            square_between_king_rook= [(4,7), (5,7), (6,7)]
            for square in square_between_king_rook:
                if square in white_locations or square in black_locations:
                    return False
        else:
            return False
        return True


def perform_king_side_castle():
    if player=='white':
        king_side_rook_position=None
        queen_side_rook_position=None
        for index, item in enumerate(white_pieces):
            if item== "rook":
                if king_side_rook_position is None:
                    king_side_rook_position= index
                else:
                    queen_side_rook_position= index
        white_locations[king_side_rook_position]=(2,0)
    else:
        king_side_rook_position=None
        queen_side_rook_position=None
        for index, item in enumerate(black_pieces):
            if item== "rook":
                if king_side_rook_position is None:
                    king_side_rook_position= index
                else:
                    queen_side_rook_position= index
        black_locations[king_side_rook_position]=(2,7) # moving the king-side rook


def perform_queen_side_castle():
    if player=='white':
        king_side_rook_position=None
        queen_side_rook_position=None
        for index, item in enumerate(white_pieces):
            if item== "rook":
                if king_side_rook_position is None:
                    king_side_rook_position= index
                else:
                    queen_side_rook_position= index
        white_locations[queen_side_rook_position]=(4,0)
    else:
        king_side_rook_position=None
        queen_side_rook_position=None
        for index, item in enumerate(black_pieces):
            if item== "rook":
                if king_side_rook_position is None:
                    king_side_rook_position= index
                else:
                    queen_side_rook_position= index
        black_locations[queen_side_rook_position]=(4,7) 


def is_checkmate(color):
    copy_white_locations= copy.copy(white_locations)
    copy_black_locations= copy.copy(black_locations)
    copy_white_pieces= copy.copy(white_pieces)
    copy_black_pieces= copy.copy(black_pieces)
    if color == 'white':
        options = copy.copy(white_options)
        # method will be like this
        # first this is turn for white player and hence first iterate over all white pieces to check to check valid moves possible
        # so that it can avoid the check by considering opponent here black locations
        # then if check is avoided for any move then return false that is it is not the checkmate
        # at the end return true if not a single move found to avoid check for the white king from the current black locations

        for option in options:
            piece= options.index(option)
            for move in option:
                copy_white_locations[piece]=move
                if move in copy_black_locations:
                    bl_piece= copy_black_locations.index(move)
                    copy_black_locations.pop(bl_piece)
                    copy_black_pieces.pop(bl_piece)
                if not is_in_check('white', copy_white_locations, copy_white_pieces, copy_black_locations, copy_black_pieces):
                    return False
                
                copy_white_locations=copy.copy(white_locations)
                copy_black_locations=copy.copy(black_locations)
                copy_white_pieces= copy.copy(white_pieces)
                copy_black_pieces= copy.copy(black_pieces)
        
        return True
    
    else:
        options = copy.copy(black_options)
        # method will be like this
        # first this is turn for white player and hence first iterate over all white pieces to check to check valid moves possible
        # so that it can avoid the check by considering opponent here black locations
        # then if check is avoided for any move then return false that is it is not the checkmate
        # at the end return true if not a single move found to avoid check for the white king from the current black locations

        for option in options:
            piece= options.index(option)
            for move in option:
                copy_black_locations[piece]=move
                if move in copy_white_locations:
                    wt_piece= copy_white_locations.index(move)
                    copy_white_locations.pop(wt_piece)
                    copy_white_pieces.pop(wt_piece)
                if not is_in_check('black', copy_white_locations, copy_white_pieces, copy_black_locations, copy_black_pieces):
                    return False
                
                copy_white_locations=copy.copy(white_locations)
                copy_black_locations=copy.copy(black_locations)
                copy_white_pieces= copy.copy(white_pieces)
                copy_black_pieces= copy.copy(black_pieces)
        
        return True




def check_pin(moves, color, piece):
    final_valid_moves=[]
    if color == "white":
        print("White's turn.")
        copy_black_pieces= copy.copy(black_pieces)
        copy_black_locations= copy.copy(black_locations)
        copy_white_pieces= copy.copy(white_pieces)
        copy_white_locations= copy.copy(white_locations)
        for move in moves:
            print("before move calc: ", move, "and ,", copy_white_locations[piece])
            copy_white_locations[piece]=move
            print("After move calc: ", move, "and ,", copy_white_locations[piece])
            if move in copy_black_locations:
                copy_black_piece= copy_black_locations.index(move)
                copy_black_pieces.pop(copy_black_piece)
                copy_black_locations.pop(copy_black_piece)
            
            # print(is_in_check(color, copy_white_locations, copy_white_pieces, copy_black_locations, copy_black_pieces))
            if not is_in_check(color, copy_white_locations, copy_white_pieces, copy_black_locations, copy_black_pieces):
                final_valid_moves.append(move)
            copy_black_pieces= copy.copy(black_pieces)
            copy_black_locations= copy.copy(black_locations)
            copy_white_pieces= copy.copy(white_pieces)
            copy_white_locations= copy.copy(white_locations)
    else:
        print("Black's turn.")
        copy_black_pieces= copy.copy(black_pieces)
        copy_black_locations= copy.copy(black_locations)
        copy_white_pieces= copy.copy(white_pieces)
        copy_white_locations= copy.copy(white_locations)
        for move in moves:
            print("before move calc: ", move, "and ,", copy_black_locations[piece])
            copy_black_locations[piece]=move
            print("After move calc: ", move, "and ,", copy_black_locations[piece])
            if move in copy_white_locations:
                copy_white_piece= copy_white_locations.index(move)
                copy_white_pieces.pop(copy_white_piece)
                copy_white_locations.pop(copy_white_piece)
            
            # print(is_in_check(color, copy_white_locations, copy_white_pieces, copy_black_locations, copy_black_pieces))
            
            if not is_in_check(color, copy_white_locations, copy_white_pieces,copy_black_locations, copy_black_pieces):
                final_valid_moves.append(move)
            # else:
                # print(is_in_check(color, copy_white_locations, copy_white_pieces, copy_white_options, copy_black_locations, copy_black_pieces, copy_black_options))
            copy_black_pieces= copy.copy(black_pieces)
            copy_black_locations= copy.copy(black_locations)
            copy_white_pieces= copy.copy(white_pieces)
            copy_white_locations= copy.copy(white_locations)
    
    return final_valid_moves



def is_stalemate():
    global stalemate
    copy_white_locations=copy.copy(white_locations)
    copy_black_locations=copy.copy(black_locations)
    copy_white_pieces=copy.copy(white_pieces)
    copy_black_pieces=copy.copy(black_pieces)
    copy_white_options= copy.copy(white_options)
    copy_black_options= copy.copy(black_options)

    white_player_result= True
    black_player_result= True

    if player=='white':
        for options in copy_white_options:
            piece_index= copy_white_options.index(options)
            for move in options:
                copy_white_locations[piece_index]=move
                if move in copy_black_locations:
                    b_p= copy_black_locations.index(move)
                    copy_black_locations.pop(b_p)
                    copy_black_pieces.pop(b_p)
                if not is_in_check('white', copy_white_locations, copy_white_pieces, copy_black_locations, copy_black_pieces):
                    return False
                copy_white_locations=copy.copy(white_locations)
                copy_black_locations=copy.copy(black_locations)
                copy_white_pieces=copy.copy(white_pieces)
                copy_black_pieces=copy.copy(black_pieces)
        
        # stalemate= True
        return True
    


    else:    
        for options in copy_black_options:
            piece_index= copy_black_options.index(options)
            for move in options:
                copy_black_locations[piece_index]=move
                if move in copy_white_locations:
                    b_p= copy_white_locations.index(move)
                    copy_white_locations.pop(b_p)
                    copy_white_pieces.pop(b_p)
                if not is_in_check('black', copy_white_locations, copy_white_pieces, copy_black_locations, copy_black_pieces):
                    return False
                copy_white_locations=copy.copy(white_locations)
                copy_black_locations=copy.copy(black_locations)
                copy_white_pieces=copy.copy(white_pieces)
                copy_black_pieces=copy.copy(black_pieces)
        # stalemate=True
        return True
    

def is_draw():
    if len(white_pieces) ==1 and white_pieces[0] =='king' and len(black_pieces)==1 and black_pieces[0]=='king':
        return True
    # if len(white_pieces)==2 :
    #     if ('king' in white_pieces and 'bishop' in white_pieces) and ('king' in black_pieces and 'bishop' in black_pieces) :
    #         return true
    return False


def draw_game_draw(type):
    if player=="white" or player=="black":
        pygame.draw.rect(screen, 'black', [80, 200, 450, 80])
        if type =="stalemate":
            screen.blit(font.render(f"Game Draw due to Stalemate!", 'True', 'white'), (90, 210))
        elif type =="draw":
            screen.blit(font.render(f"Game draw due to less sufficient pieces!", 'True', 'white'), (90, 210))
        screen.blit(font.render(f'Press Enter to Restart!', 'True', 'white'), (90, 250))


def draw_game_over(player):
    pygame.draw.rect(screen, 'black', [200, 200, 400, 80])
    if player==winner:
        screen.blit(font.render(f"Congrats! You've won the game!", 'True', 'white'), (210, 210))
    else:
        screen.blit(font.render(f'{winner} player won the game!', 'True', 'white'), (210, 210))
    screen.blit(font.render(f'Press Enter to Restart!', 'True', 'white'), (210, 250))

# check for valid moves for just selected piece
def check_valid_moves():
    if turn_step< 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


def check_pawn_promotion():
    white_promotion= False
    black_promotion= False
    promo_index = 100
    white_pawn_index=[]
    black_pawn_index=[]
    for i in range(len(white_pieces)):
        if white_pieces[i]=='pawn':
            white_pawn_index.append(white_locations[i])
    for i in range(len(black_pieces)):
        if black_pieces[i]=='pawn':
            black_pawn_index.append(black_locations[i])
    if player=="white":
        for item in white_pawn_index:
            if item[1] == 7:
                white_promotion= True
                promo_index= white_locations.index(item)
                break
    else:
        for item in black_pawn_index:
            if item[1] == 0:
                black_promotion= True
                promo_index= black_locations.index(item)
                break
    
    return white_promotion, black_promotion, promo_index


def draw_promotion():
    pygame.draw.rect(screen, 'gray', [640, 0, WIDTH-640, 350])
    if player== 'white':
        for i in range(len(white_promotion_pieces)):
            piece= white_promotion_pieces[i]
            index= piece_list.index(piece)
            screen.blit(white_images[index], (660, 80*i, 45, 45))
    else:
        for i in range(len(black_promotion_pieces)):
            piece= black_promotion_pieces[i]
            index= piece_list.index(piece)
            screen.blit(black_images[index], (660, 80*i, 45, 45))


def check_promo_select():
    mouse_pos=pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]

    x_pos= mouse_pos[0] // 80
    y_pos= mouse_pos[1] // 80
    print("promotion left click: ", left_click, x_pos, y_pos)
    if white_promotion and player=='white' and left_click and y_pos<4 and x_pos>7:
        print(white_promotion_pieces[y_pos], "is selected for promotion.")
        white_pieces[promo_index] = white_promotion_pieces[y_pos]
    elif black_promotion and player=='black' and left_click and y_pos<4 and x_pos>7:
        black_pieces[promo_index]= black_promotion_pieces[y_pos]

    
    return left_click and y_pos<4 and x_pos>7

# draw valid moves on screen
def draw_valid(moves):
    if turn_step<2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        if player=='white':
            pygame.draw.circle(screen, color, ((7-moves[i][0])* 80 +45, (7-moves[i][1])* 80 +45 ),5)
        else:
            pygame.draw.circle(screen, color, (moves[i][0]* 80 +45, moves[i][1]* 80 +45 ),5)

def check_options(pieces, locations, turn, copy_black_locations, copy_white_locations):

    moves_list =[]
    all_moves_list = []
    for i in range(len(pieces)):
        location= locations[i]
        piece= pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn, copy_black_locations, copy_white_locations)
        elif piece == 'rook':
            moves_list = check_rook(location, turn, copy_black_locations, copy_white_locations)
        elif piece == 'knight':
            moves_list = check_knight(location, turn, copy_black_locations, copy_white_locations)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn, copy_black_locations, copy_white_locations)
        elif piece == 'queen':
            moves_list = check_queen(location, turn, copy_black_locations, copy_white_locations)
        elif piece == 'king':
            moves_list = check_king(location, turn, copy_black_locations, copy_white_locations)
        all_moves_list.append(moves_list)
    return all_moves_list


# draw captured pieces on side of screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece= captured_pieces_white[i]
        index= piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (720, 15 + 50*i))
    for i in range(len(captured_pieces_black)):
        captured_piece= captured_pieces_black[i]
        index= piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (800, 15 + 50*i))

# draw a flashing square around king if in check
def draw_check():
    checked= False
    if turn_step <2 :
        
        king_index= white_pieces.index('king')
        king_location = white_locations[king_index]
        for i in range(len(black_options)):
            if king_location in black_options[i]:
                
                if counter < 15:
                    if player=='white':
                        pygame.draw.rect(screen, 'red', [(7-white_locations[king_index][0])*80 +1, (7-white_locations[king_index][1])*80 +1, 80, 80], 5)
                    else:
                        pygame.draw.rect(screen, 'red', [white_locations[king_index][0]*80 +1, white_locations[king_index][1]*80 +1, 80, 80], 5)
    else:
        # if is_checkmate('black'):
        #     print("Black checkmate")
        #     return
        king_index= black_pieces.index('king')
        king_location = black_locations[king_index]
        for i in range(len(white_options)):
            if king_location in white_options[i]:
                
                if counter < 15:
                    if player=='white':
                        pygame.draw.rect(screen, 'blue', [(7-black_locations[king_index][0])*80 +1, (7-black_locations[king_index][1])*80 +1, 80, 80], 5)
                    else:
                        pygame.draw.rect(screen, 'blue', [black_locations[king_index][0]*80 +1, black_locations[king_index][1]*80 +1, 80, 80], 5)
        


response_to_send = (
                            white_locations, black_locations, white_pieces, black_pieces, turn_step, captured_pieces_white, captured_pieces_black, two_moved_white_pawns, two_moved_black_pawns, stalemate
                        )
                # if turn_step == 2 or turn_step == 0:
                    
client_socket.sendall(pickle.dumps(response_to_send))



# main game loop

run = True
with thread_state_lock:
    while run:
        timer.tick(fps)
        if counter< 3:
            counter +=1
        else:
            counter =0 
        # screen.fill('gray')
        screen.fill((169,169,169))
        print(white_locations)
        print(black_locations)
        print(f"{player} player promotion: ", promo_index)
        print(f"{player} player, stalemate status: ", stalemate)
        draw_board()
        if player== 'white':
            draw_board_opposite()
        else:
            draw_pieces()
        draw_captured()
        draw_check()
        

        if is_in_check('white', white_locations, white_pieces, black_locations, black_pieces):
            if is_checkmate('white'):
                game_over=True
                winner='black'
                # break
        elif is_in_check('black', white_locations, white_pieces, black_locations, black_pieces):
            if is_checkmate('black'):
                # print(f"{player} player is checkmate")
                game_over=True
                winner='white'
        elif not is_in_check('white', white_locations, white_pieces, black_locations, black_pieces) and is_stalemate():
            game_over=True
            stalemate= True
            draw_type= "stalemate"
            response_to_send = (
                            white_locations, black_locations, white_pieces, black_pieces, turn_step, captured_pieces_white, captured_pieces_black, two_moved_white_pawns, two_moved_black_pawns, stalemate
                        )
                # if turn_step == 2 or turn_step == 0:
                    
            client_socket.sendall(pickle.dumps(response_to_send))

        elif not is_in_check('black', white_locations, white_pieces, black_locations, black_pieces) and is_stalemate():
            game_over=True
            stalemate= True
            draw_type= "stalemate"
            response_to_send = (
                            white_locations, black_locations, white_pieces, black_pieces, turn_step, captured_pieces_white, captured_pieces_black, two_moved_white_pawns, two_moved_black_pawns, stalemate
                        )
                # if turn_step == 2 or turn_step == 0:
                    
            client_socket.sendall(pickle.dumps(response_to_send))

        if  is_draw():
            game_over=True
            draw_type= "draw" 
        
        if game_over == False:
            # white_promotion, black_promotion, promo_index= check_pawn_promotion()

            if turn_step==2 and player=='white':
                # turn_step=1
                draw_promotion()
                is_promoted= check_promo_select()
                if is_promoted:
                    turn_step=3
                    response_to_send = (
                            white_locations, black_locations, white_pieces, black_pieces, turn_step, captured_pieces_white, captured_pieces_black, two_moved_white_pawns, two_moved_black_pawns, stalemate
                        )
                # if turn_step == 2 or turn_step == 0:
                    
                    client_socket.sendall(pickle.dumps(response_to_send))
                
            if turn_step==5 and player=='black':
                # turn_step=3
                draw_promotion()
                is_promoted= check_promo_select()
                if is_promoted:
                    turn_step=0
                    response_to_send = (
                            white_locations, black_locations, white_pieces, black_pieces, turn_step, captured_pieces_white, captured_pieces_black, two_moved_white_pawns, two_moved_black_pawns, stalemate
                        )
                # if turn_step == 2 or turn_step == 0:
                    
                    client_socket.sendall(pickle.dumps(response_to_send))
                
                
        if selection != 100:
            valid_moves = check_valid_moves()
            print("valid moves_initial: ", valid_moves)
            valid_moves= check_pin(valid_moves, player, selection)
            print("valid moves_final: ", valid_moves)
            print("two_moved_white_pawns", two_moved_white_pawns)
            print("two_moved_black_pawns", two_moved_black_pawns)
            draw_valid(valid_moves)
        # if turn_step == 2 :
        #     if is_checkmate('black'):
        #         print("black is checkmate.")
        # elif  turn_step ==0:
        #     if is_checkmate('white'):
        #         print("White is checkmate.")  
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 and game_over == False:
                x_coord= event.pos[0] // 80
                y_coord= event.pos[1] // 80
                click_coords = (x_coord, y_coord)
                temp_click_coords=click_coords
                if turn_step <= 1 and player=='white':
                    click_coords=(7-click_coords[0], 7-click_coords[1])


                    if click_coords in white_locations:
                        selection = white_locations.index(click_coords)
                        if turn_step == 0:
                            initial_position= copy.copy(click_coords)
                            turn_step =1
                    
                   
                    print("running valid_moves: ", valid_moves)
                    print("current coord: ", click_coords)
                    if ((click_coords[0], click_coords[1]) in valid_moves and selection != 100) or (click_coords[0], click_coords[1], 'en-passant') in valid_moves or (click_coords[0], click_coords[1], 'king-side-castle') in valid_moves or (click_coords[0], click_coords[1], 'queen-side-castle') in valid_moves:
                        white_locations[selection] = (click_coords[0], click_coords[1])
                        if (click_coords[0], click_coords[1], 'en-passant') in valid_moves:
                            # it is en-passant
                            print("En-passant is being called.")
                            perform_enpassant((click_coords[0], click_coords[1]))
                            # perform_enpassant((click_coords[0], click_coords[1]))
                            response_to_send = (
                                white_locations, black_locations, white_pieces, black_pieces, turn_step, captured_pieces_white, captured_pieces_black, two_moved_white_pawns, two_moved_black_pawns, stalemate
                                 )
                        # if turn_step == 2 or turn_step == 0:
                    
                            client_socket.sendall(pickle.dumps(response_to_send))
                        # print("for white piece: ", click_coords, initial_position)
                        elif abs(click_coords[1]-initial_position[1]) ==2 and white_pieces[selection]=='pawn' :
                            two_moved_white_pawns[selection-8]=2
                        elif abs(click_coords[1]-initial_position[1]) ==1 and white_pieces[selection]=='pawn' :
                            two_moved_white_pawns[selection-8]=1
                        
                        if white_pieces[selection]=='king':
                            white_king_moved= True
                        if white_pieces[selection]=='rook':
                            king_side_rook= None
                            queen_side_rook= None
                            for index, item in enumerate(white_pieces):
                                if item == 'rook':
                                    if king_side_rook == None:
                                        king_side_rook=index
                                    else:
                                        queen_side_rook= index
                            # if selection==0:
                            if selection == king_side_rook:
                                white_king_side_rook_moved= True
                            # elif selection==7:
                            elif selection == queen_side_rook:
                                white_queen_side_rook_moved= True
                        
                        if (click_coords[0], click_coords[1], 'king-side-castle') in valid_moves:
                            perform_king_side_castle()
                        if (click_coords[0], click_coords[1], 'queen-side-castle') in valid_moves:
                            perform_queen_side_castle()

                            
                        if click_coords in black_locations:
                            black_piece = black_locations.index(click_coords)
                            captured_pieces_white.append(black_pieces[black_piece])
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)
                            response_to_send = (
                                white_locations, black_locations, white_pieces, black_pieces, turn_step, captured_pieces_white, captured_pieces_black, two_moved_white_pawns, two_moved_black_pawns, stalemate
                                 )
                        # if turn_step == 2 or turn_step == 0:
                    
                            client_socket.sendall(pickle.dumps(response_to_send))
                        
                        black_options = check_options(black_pieces, black_locations, 'black', black_locations, white_locations)
                        white_options = check_options(white_pieces, white_locations, 'white', black_locations, white_locations)


                        selection = 100
                        valid_moves= []
                        white_promotion, black_promotion, promo_index= check_pawn_promotion()
                        if white_promotion:
                            turn_step = 2
                        else:
                            turn_step= 3
                        

                        response_to_send = (
                            white_locations, black_locations, white_pieces, black_pieces, turn_step, captured_pieces_white, captured_pieces_black, two_moved_white_pawns, two_moved_black_pawns, stalemate
                        )
                        # if turn_step == 2 or turn_step == 0:
                    
                        client_socket.sendall(pickle.dumps(response_to_send))
                        

                        
                            

                       
                            
                if turn_step > 2 and player=='black':
                    if click_coords in black_locations:
                        selection = black_locations.index(click_coords)
                        if turn_step == 3:
                            initial_position= copy.copy(click_coords)
                            turn_step =4
                    if ((click_coords[0], click_coords[1]) in valid_moves and selection != 100) or (click_coords[0], click_coords[1], 'en-passant') in valid_moves or (click_coords[0], click_coords[1], 'king-side-castle') in valid_moves or (click_coords[0], click_coords[1], 'queen-side-castle') in valid_moves:
                        black_locations[selection] = (click_coords[0], click_coords[1])
                        print("for black piece: ", click_coords, initial_position)
                        if (click_coords[0], click_coords[1], 'en-passant') in valid_moves:
                            print("En-passant is being called.")
                            perform_enpassant((click_coords[0], click_coords[1]))
                            response_to_send = (
                                white_locations, black_locations, white_pieces, black_pieces, turn_step, captured_pieces_white, captured_pieces_black, two_moved_white_pawns, two_moved_black_pawns, stalemate
                                 )
                        # if turn_step == 2 or turn_step == 0:
                    
                            client_socket.sendall(pickle.dumps(response_to_send))
                        elif abs(click_coords[1]-initial_position[1]) ==2 and black_pieces[selection]=='pawn' :
                            two_moved_black_pawns[selection-8]=2
                        elif abs(click_coords[1]-initial_position[1]) ==1 and black_pieces[selection]=='pawn' :
                            two_moved_black_pawns[selection-8]=1
                        if black_pieces[selection]=='king':
                            black_king_moved= True
                        if black_pieces[selection]=='rook':
                            king_side_rook= None
                            queen_side_rook= None
                            for index, item in enumerate(black_pieces):
                                if item == 'rook':
                                    if king_side_rook == None:
                                        king_side_rook=index
                                    else:
                                        queen_side_rook= index
                            

                            if selection == king_side_rook:
                            # if selection==0:
                                black_king_side_rook_moved= True
                            # elif selection==7:
                            elif selection == queen_side_rook:
                                black_queen_side_rook_moved= True
                        if (click_coords[0], click_coords[1], 'king-side-castle') in valid_moves:
                            perform_king_side_castle()
                        if (click_coords[0], click_coords[1], 'queen-side-castle') in valid_moves:
                            perform_queen_side_castle()
                        
                                
                        if click_coords in white_locations:
                            white_piece = white_locations.index(click_coords)
                            captured_pieces_black.append(white_pieces[white_piece])
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)
                            response_to_send = (
                                white_locations, black_locations, white_pieces, black_pieces, turn_step, captured_pieces_white, captured_pieces_black, two_moved_white_pawns, two_moved_black_pawns, stalemate
                                 )
                        # if turn_step == 2 or turn_step == 0:
                    
                            client_socket.sendall(pickle.dumps(response_to_send))
                        

                        black_options = check_options(black_pieces, black_locations, 'black', black_locations, white_locations)
                        white_options = check_options(white_pieces, white_locations, 'white', black_locations, white_locations)

                        selection = 100
                        valid_moves= []



                        


                        white_promotion, black_promotion, promo_index= check_pawn_promotion()
                        if black_promotion:
                            turn_step=5
                        else:
                            turn_step = 0


                        response_to_send = (
                            white_locations, black_locations, white_pieces, black_pieces, turn_step, captured_pieces_white, captured_pieces_black, two_moved_white_pawns, two_moved_black_pawns, stalemate
                        )
                        # if turn_step == 2 or turn_step == 0:
                    
                        client_socket.sendall(pickle.dumps(response_to_send))
                        
                # if player =='white':
                #     alterBoard(white_locations, black_locations)
                response_to_send = (
                    white_locations, black_locations, white_pieces, black_pieces, turn_step, captured_pieces_white, captured_pieces_black, two_moved_white_pawns, two_moved_black_pawns, stalemate
                )
                # if turn_step == 2 or turn_step == 0:
                    
                client_socket.sendall(pickle.dumps(response_to_send))

            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_RETURN:
                    white_pieces= ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn','pawn', 'pawn', 'pawn']

                    white_locations=[(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                                    (0,1), (1,1), (2,1), (3, 1), (4,1), (5,1), (6,1), (7,1)]

                    black_pieces= ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn','pawn', 'pawn', 'pawn']


                    black_locations=[(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7),
                                        (0,6), (1,6), (2,6), (3, 6), (4,6), (5,6), (6,6), (7,6)]


                    captured_pieces_white =[]
                    captured_pieces_black =[]

                    turn_step =0
                    selection= 100

                    valid_moves= []
                    counter=0
                    winner=''
                    game_over=False


                    two_moved_white_pawns=[0,0,0,0,0,0,0,0]
                    two_moved_black_pawns=[0,0,0,0,0,0,0,0]

                    white_promotion= False
                    black_promotion = False
                    promo_index = 100

                    white_promotion_pieces=['bishop', 'knight', 'rook', 'queen']
                    black_promotion_pieces=['bishop', 'knight', 'rook', 'queen']

                    white_king_side_rook_moved= False
                    white_queen_side_rook_moved= False
                    black_king_side_rook_moved= False
                    black_queen_side_rook_moved= False

                    white_king_moved= False
                    black_king_moved= False
                    draw_type=""
                    stalemate = False
                
                    
                    
        if winner!='':
            draw_game_over(player)
        if stalemate:
            draw_game_draw("stalemate")
        if game_over and draw_type== 'draw':
            draw_game_draw(draw_type)
        pygame.display.flip()