import pygame
from pygame.locals import *

pygame.init()

screen_width = 950
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

white= (255,255,255)
black = (0,0,0)
tile_size = 50

# load images

sun_img = pygame.image.load('C:/Users/richardlin/Downloads/sun1.png')
sky_img = pygame.image.load('C:/Users/richardlin/Downloads/sky.png')
bg_img = pygame.transform.scale(sky_img,(1000,600))
dirt_img = pygame.image.load('C:/Users/richardlin/Downloads/dirt.jpg')
grass_img = pygame.image.load('C:/Users/richardlin/Downloads/grass1.png')
apple_img = pygame.image.load('C:/Users/richardlin/Downloads/apple2.png')

player_img =  pygame.image.load('C:/Users/richardlin/Downloads/player1.png')

player_left = pygame.transform.flip(player_img,True,False)
player_right = pygame.transform.flip(player_img,False,False)

player_right_list = []
player_left_list = []
for i in range(1,7):
    img = pygame.image.load('C:/Users/richardlin/Downloads/player'+str(i)+'.png')
    img = pygame.transform.flip(img,True,False)
    img = pygame.transform.scale(img,(40,40))
    player_right_list.append(img)

    
for i in range(1,7):
    img = pygame.image.load(f'C:/Users/richardlin/Downloads/player{i}.png')
    #img = pygame.transform.flip(img,True,False)
    img = pygame.transform.scale(img,(40,40))
    player_left_list.append(img)
def draw_grid():

    for line in range(20):
        pygame.draw.line(screen,white,(0,line*tile_size),(screen_width,line*tile_size))
        pygame.draw.line(screen,white,(line*tile_size,0),(line*tile_size,screen_width))



world_data = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1],
    [1,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,1],
    [1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,1],
    [1,2,0,0,0,2,0,0,0,2,0,0,0,2,0,0,0,2,1],
    [1,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1],
    [1,2,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

def tile_data():
    global tile_list
    tile_list = []
    row_count = 0
    for row in world_data:
        col_count = 0
        for tile in row:
            if tile == 1:
                img = pygame.transform.scale(dirt_img,(tile_size-1, tile_size-1))
                img_rect = img.get_rect()
                img_rect.x = col_count * tile_size
                img_rect.y = row_count * tile_size
                tile = (img,img_rect,1)
                tile_list.append(tile)
            if tile == 2:
                img = pygame.transform.scale(apple_img,(tile_size, tile_size))
                img_rect = img.get_rect()
                img_rect.x = col_count * tile_size
                img_rect.y = row_count * tile_size
                tile = [img,img_rect,2]
                tile_list.append(tile)
                
            col_count += 1
        row_count += 1
            
def draw_tile():
    global tile_list

    for tile in tile_list:
        screen.blit(tile[0], tile[1])

x = 50
y = 399





vel_y =0
index = 0
img = pygame.transform.scale(player_left,(40,40))

img = pygame.transform.scale(player_left_list[index],(40,40))
rect = img.get_rect()


counter = 0
tile_width=img.get_width()
tile_height = img.get_height()

walk_cooldown=5
rect.x = 50
rect.y=410
def update(flip):
    global vel_y,dx,dytile_list, counter, index, walk_cooldown
    dy = 0  
    vel_y += 1
    if vel_y > 10:
        vel_y = 10

    dy += vel_y
   
    for tile in tile_list:
        if  tile[1].colliderect(rect.x + dx , rect.y, tile_width, tile_height):
            dx = 0
            if tile[2] == 2:
                print('heelo')
                tile_list.remove(tile)      
        if tile[1].colliderect(rect.x , rect.y + dy, tile_width, tile_height):
            
            if vel_y<0:
                dy = tile[1].bottom - rect.top
            else:
                dy = tile[1].top - rect.bottom
            if tile[2] == 2:
                print('hi')
                if tile in tile_list:
                    #print('hello')
                    #tile[2] = 0
                    
                    tile_list.remove(tile) 
                    
    rect.x += dx
    rect.y += dy     

    if counter > walk_cooldown:
        counter = 0
    if rect.bottom > screen_height-50:
        rect.bottom = screen_height -50
        vel_y = 0
        dy = 0
    if dx ==0:
        index =0
    else:
        index += 1

    if index >= len(player_left_list):
        index = 0
    
    if flip:
            image = pygame.transform.scale(player_right_list[index],(40,40))
    else:
            image = pygame.transform.scale(player_left_list[index],(40,40))
    screen.blit(image,rect)

    

flip = False
jumped= False
##player = Player(50,screen_height -90, flip)
#world = World(world_data)
run = True
dx = 0
dy = 0

tile_data()



while run:
    draw_tile()
    update(flip)
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE and jumped == False:
                vel_y = -15
                jumped = True
            if event.key == K_SPACE:
                jumped = False
            if event.key == K_LEFT:
                dx = -3
                flip = False  
            if event.key == K_RIGHT:
                dx = 3
                flip = True
        if event.type == pygame.KEYUP:
            if event.key == K_SPACE:
                  dy = 1
            if event.key == K_LEFT:
                dx = 0
                flip = False
                
            if event.key == K_RIGHT:
                dx = 0
                flip = True               
       
                
                

    pygame.display.update()
    screen.fill(black)
            
