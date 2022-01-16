import pygame
from pygame.locals import *

pygame.init()


clock = pygame.time.Clock()
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


player_left = pygame.transform.flip(player_img,True,False)
player_right = pygame.transform.flip(player_img,False,False)
def draw_grid():

    for line in range(20):
        pygame.draw.line(screen,white,(0,line*tile_size),(screen_width,line*tile_size))
        pygame.draw.line(screen,white,(line*tile_size,0),(line*tile_size,screen_width))


class World():
    def __init__(self,data):
        self.tile_list = []
      
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img,(tile_size, tile_size-1))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img,img_rect,1)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(apple_img,(tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img,img_rect,2)
                    self.tile_list.append(tile)
                    
                col_count += 1
            row_count += 1
                    

    def draw(self):
        for tile in self.tile_list:
           
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen,black,tile[1],1)

class Player():
    def __init__(self,x,y,flip):
        self.image_right = player_right_list
        self.image_left = player_left_list
        self.index = 0
        self.counter = 0

        self.image = self.image_right[self.index]
       
        
        self.rect = self.image.get_rect()
        self.rect.x= x
        self.rect.y= y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.dx = 0
        self.dy = 0
        self.jumped = False
        self.flip = True
        self.vel_y=0
        self.score =0
        
    def update(self):
        global dx
        
        walk_cooldown = 5
        dx = 0
        dy = 0
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        
        # check for collision
        
        for tile in world.tile_list:
            #print(tile[1])
             # check for collision in x direction
            if tile[1].colliderect(self.rect.x + self.dx, self.rect.y,self.width,self.height):
                self.dx = 0
                #print('hi')
                if tile[2] == 2:
                    
                    world.tile_list.remove(tile)
                    self.score += 1
            # check for collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy,self.width,self.height):
                #print('collision')
                # check if below the ground i.e. jumping
                if self.vel_y<0:
                    dy = tile[1].bottom - self.rect.top
                    #print('hello')
                else:
                    dy = tile[1].top - self.rect.bottom
                if tile[2] == 2:
                    if tile in world.tile_list:
                        world.tile_list.remove(tile)
                        self.score += 1
        # update player coordinates
        
        self.rect.x += self.dx
        self.rect.y += dy

       

        #print(self.vel_y,dy)

        
        if self.counter > walk_cooldown:
            self.counter = 0
            

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.vel_y=0
        if self.dx==0:
            self.index = 0
        else:
            self.index += 1
        #print(self.index)
        if self.index >= len(self.image_right):
            self.index = 0
            
        
    
        # get keypress
        if self.flip:
            self.image = self.image_right[self.index]
        else:
            self.image = self.image_left[self.index]
        screen.blit(self.image,self.rect)
        pygame.draw.rect(screen,white, self.rect, 1)
        
        
    
        
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
    

flip = False
player = Player(50,screen_height -90, flip)
world = World(world_data)
run = True
dx = 0
dy = 0

while run:
    pygame.time.delay(100)
    #screen.blit(bg_img,(0,0))
    #screen.blit(sun_img,(100,100))
    world.draw()
    player.update()
    #draw_grid()
    #print(dx)
##    player.rect.x += dx
##    player.rect.y += dy
    #print(world.tile_list)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:

            if event.key == K_SPACE and player.jumped == False:
                player.vel_y = -15
                player.jumped = True
            if event.key == K_SPACE:
                player.jumped = False
                
            if event.key == K_LEFT:
                player.dx -= 5
               
                player.counter +=1
                player.flip = False
                
            if event.key == K_RIGHT:
                player.dx += 5
               
                player.counter +=1
                player.flip = True

            if not (event.key == K_LEFT or event.key == K_RIGHT):
                player.counter = 0
                player.index = 0
                player.image = player.image_right[player.index]
        if event.type == pygame.KEYUP:
            
            if event.key == K_LEFT :
           
                player.counter = 0
                player.index = 0
                player.image = player.image_right[player.index]
                
            if event.key == K_RIGHT:
                player.counter = 0
                player.index = 0
                player.image = player.image_right[player.index]
                
               
                
            
                
                
                

    pygame.display.update()
    screen.fill(black)
            
