import pygame
import random

from pygame import surface

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

# 꼭지점 설정하기!
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# 붕어빵 틀(class)과 붕어빵(object)
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[ shapes.index(shape) ]
        self.rotation = 0

# Grid 생성하기 // grid는 color
def create_grid( locked_pos={} ): # locked_pos: 위치랑 color
    grid = [ [ (0,0,0) for x in range(10) ] for x in range(20) ]

    # 모든걸 다 읽고 싶을때 많이 쓰는 코드
    for y in range ( len(grid) ):
        for x in range ( len(grid[y]) ):
            if (x, y) in locked_pos: #locked pos에 있으면 >>> ???? 이해안감
                grid[y][x] = locked_pos[ (x,y) ] #색깔을 넣어라

    return grid

# 모양의 위치를 정해주고, 모양 바뀐것도 위치 정해주기// shape: current_piece
def convert_shape_format(shape):
    # 위치만 저장, 길이는 나중에 저장할것임
    position = [] #튜플의 형태로 블록의 위치를 저장해놓고 있음
    ''' 예를 들어, 아래와 같은 형태로 format에 저장하는거지. 
    ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']
    '''
    format = shape.shape[ shape.rotation % len(shape.shape)] 

    # enumerate: 위치랑 값이랑 다 읽어옴 // format: 특정 shape의 rotation까지 읽는거.
    for y, line in enumerate(format): # '.'과 '0'의 위치와 값 읽음
        for x, each in enumerate(line):
            if each == '0': 
                # shape의 x, y 시작점에서 x랑 y만큼 위치 저장 >> shape에서 보면, 블럭 모양 대로 위치를 저장했으니까. // position에 current piece의 shape의 위치가 저장되어있음.
                position.append( (shape.x + x, shape.y + y) )

    # 내려오는 위치 살짝 변경해서 가운데로 맞추려고.
    for i, pos in enumerate(position): #index, value
        position[i] = (pos[0] - 2, pos[1] - 4)

    return position

# shape: current piece, grid: color
def valid_space(shape, grid):
    #검은색인 배경은 valid니까 저장해도 된다.
    accepted_pos = [ [ (x, y) for x in range(10) if grid[y][x] == (0, 0, 0)] for y in range(20) ]
    #2차원을 1차원으로 저장/굉장히 많이 쓰는 코드/빨리 계산하기 위해/검정색인 위치만 저장해놓는거.
    accepted_pos = [ j for sub in accepted_pos for j in sub] # j를 일렬로 정렬하기

    # 로테이션하면 어떤 shape? 그 위치를 저장
    format = convert_shape_format( shape )

    # shape을 좌표로 바꿔야해. 위치를 전부 다 가져오기.
    for pos in format: #format에 x,y만 다 들어있음!
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False

    return True

    # lock pos : 위치랑 모양 둘 다 

# positions : locked_positions // 블록이 맨위(y=0)에 닿으면
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < -1:
            return True

    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes)) # random.choice 랜덤으로 뽑을때 많이 쓰는 코드

def draw_text_middle(text, size, color, surface):

    pygame.font.init()

    font = pygame.font.SysFont( 'comicsans', 60 )
    label = font.render( text, size, color )

    surface.blit( label, ( s_width/2 - (label.get_width()/2 ) , s_height/2 ) )

    pygame.display.update()

#그리드 그리기!
def draw_grid(surface, grid):
    
    #가로선 그리기
    # len(grid) : 그리드 가로길이 
    for i in range( len(grid) ):
        pygame.draw.line( surface, (255,255,255), ( top_left_x, top_left_y + i*block_size), ( top_left_x + play_width, top_left_y + i*block_size), 2)
        # 왜 그리드 세로줄을 10번씩
        for j in range( len(grid[i]) ):
            pygame.draw.line( surface, (255,255,255), (top_left_x + j*block_size, top_left_y), (top_left_x + j*block_size, top_left_y + play_height), 2)


# grid: color/ locked: 위치, 컬러
def clear_rows(grid, locked):
    inc = 0 #몇 줄 지웠는지 찾기 위해

    for y in range( len( grid ) - 1, -1, -1 ):
        if ( 0,0,0 ) not in grid[y]:
            inc += 1
            ind = y
            for x in range( len(grid[y]) ): # x 찾아서 그 줄 (x,y)를 다 지운다.
                del locked[ (x,y) ]

    # 지운 줄이 있으면 실행: 위에 있는 거 내려야하니까.
    if inc > 0 :
        # dictionary 를 list로 바꾸면 key만 가져옴 { (key) : (value) }
        for key in sorted ( list(locked), key = lambda x:x[1] )[::-1]: # locked를 list로 바꾸면 key(위치)값이 저장되고 key가 지금 튜플이니까 y값인 x[1] 값을 sort하기, reverse하기
            x,y = key
            if y < ind :
                newKey = ( x, y + inc ) #밑으로 내렸을때 새로운 위치
                locked[ newKey ] = locked.pop(key) # key의 locked를 newkey에 내려주는데 내려주기 전에 없애줌

    return inc

# shape = next_shape
def draw_next_shape(shape, surface): #넥스트 쉐입 그려주기

    next_shape_x = top_left_x + play_width + 50
    next_shape_y = top_left_y

    # next_shape 그리드 그리기
    pygame.draw.rect( surface, (255,255,255), ( next_shape_x, next_shape_y, 150, 150 ), 3)

    format = shape.shape[ 0 ] 

    for y, line in enumerate(format):
        for x, each in enumerate(line):
            if each == '0': 
                pygame.draw.rect( surface, shape.color, ( next_shape_x + x * block_size, next_shape_y + y * block_size, block_size, block_size ), 0 )


def update_score(nscore):
    score = max_score()

    with open('study/scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open('study/scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


# 글씨, 바깥 네모칸 그리기
def draw_window(surface, grid, score, last_score):
    surface.fill( (0,0,0) ) #색칠하기
    pygame.font.init() #폰트 쓰려면 init 해줘야함

    font = pygame.font.SysFont( 'comicsans', 60 )
    label = font.render( "Tetris Girls", 1, (255,0,0) ) #폰트 만들기

    surface.blit( label, ( s_width/2 - (label.get_width()/2 ) , 30) ) # 화면에 보여준다(글씨, 위치). #tuple:수정안됨

    #current score
    font = pygame.font.SysFont( 'comicsans', 30 )
    label = font.render( "Score : " + str(score), 1, (255,255,255) )

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))

    #last score
    label = font.render( "High Score : " + last_score, 1, (255,255,255) )

    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx + 20, sy + 160))

    # 모든 그리드에 색깔을 채운다. // grid에 지금 블록의 색깔들이 들어있음. 그걸 채우는거야.
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (top_left_x + x*block_size, top_left_y + y*block_size, block_size, block_size), 0) 

    # 바깥 랭탱귤러 라인 그리기 두껍게
    pygame.draw.rect( surface, (0,0,255), ( top_left_x, top_left_y, play_width, play_height), 5)

    # 그리드 하얀줄 그리기
    draw_grid( surface, grid )


# 게임시작!
def main( win ):
    
    locked_positions = {}
    grid = create_grid(locked_positions)

    # change_piece 가 true이면 다음 피쓰가 내려옴.
    change_piece = False
    
    # boolean for piece movement in grid 
    run = True 

    #First Tetris Piece
    current_piece = get_shape()
    #Next Tetris Piece
    next_piece = get_shape()
    
    #게임안에서 시간.
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27

    score = 0
    last_score = max_score()

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime() #현재시간
        clock.tick()

        #reset fall_time to 0 and drop tetris piece if all_time goes passed fall_speed threshold
        # 시간이지나면 블럭 내려오는거
        if fall_time/1000 > fall_speed:
            fall_time = 0
            # 시간이 지나면 current piece를 한칸씩 떨어뜨리기
            current_piece.y += 1
        
            # 떨어진 위치가 valid한지 확인하고.
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1 # 여기에 속하면 다시 한 칸을 올려줘라!
                change_piece = True #next 피스를 보여주라!


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not( valid_space(current_piece, grid) ):
                        current_piece.x += 1
                
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not( valid_space(current_piece, grid) ):
                        current_piece.x -= 1
                
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not( valid_space(current_piece, grid) ):
                        current_piece.y -= 1

                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not( valid_space(current_piece, grid) ):
                        current_piece.rotation -= 1

                # if event.key == pygame.K_SPACE:
                    


        # 블록의 위치를 계속 확인해줘야해서 있는 코드(1차원에 current_piece 위치 저장)
        shape_pos = convert_shape_format(current_piece)

        # 색깔 한 번 더 입히기(땅에 닿자마자 보이게)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i] #블록의 위치 저장(튜플로 저장되어 있음)
            if y > -1:
                #컬러를 넣어줘라, 그리드에
                grid[y][x] = current_piece.color

        # Grid = color
        # locked_position = {(x,y) : (255,255,255)}

        # 그리드 안에서 멈추는 거. 다음거 내려! >> 여기 이해노노노노노
        if change_piece:
            # 다음 피스를 다시 정해주는 거.
            for pos in shape_pos: #shape_pos :위치 저장해놓았음. (x, y)
                # 위치 저장
                p = (pos[0], pos[1])
                # dictionary : key, value // locked_position 블록의 모양
                locked_positions[p] = current_piece.color #p(key)에 color(value) 저장 >> dictionary
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10
       
        #그리드 그리기
        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)

        #그리드 업데이트
        pygame.display.update()


        # 맨 위까지 블록이 차면 끝내기
        if check_lost(locked_positions):
            # 여기에 게임오버 팝업 넣기
            draw_text_middle("GAME OVER", 20, (255, 255, 255), win)
            run = False
            update_score(score)

def main_menu( win ):  # start game
    run = True
    while run:
        win.fill((0,0,0))  #검정색으로 배경 채우기
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #x버튼을 누르면.
                run = False
            if event.type == pygame.KEYDOWN: #아무키나 누르면 게임시작!
                main(win)

    pygame.display.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
win.fill((0,0,0))
draw_text_middle("PRESS ANY KEY TO START", 20, (255, 255, 255), win)
main_menu(win)

'''
Pygame

display.update() : 이미지 업데이트
pygame.draw.line() : 선 그리기
pygame.draw.rect() : 바깥쪽 선 그리기
pygame.keydown()
pygame.font()
pygame.surface.blit()
'''