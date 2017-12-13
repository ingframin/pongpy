import pygame_sdl2 as pg
import sys
import random
# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0, 0, 255)

class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __add__(self,vec2):
        return Vector(vec2.x + self.x, vec2.y + self.y)

    def __sub__(self,vec2):
        return Vector(self.x-vec2.x, self.y-vec2.y)

    def amplify(self,gain):
        self.x*= gain
        self.y*= gain
    def speed_up(self, k):
        if self.x <0:
            self.x -= k
        else:
            self.x += k
    
class Player:
    def __init__(self, img):
        self.score = 0
        self.image = img
        self.rect = img.get_rect()

    def move(self,speed):
        self.rect.move_ip(speed.x,speed.y)

    
class PongGame:
    def __init__(self,size = (800, 600)):
        pg.init()
        self.screen = pg.display.set_mode(size,pg.HWSURFACE|pg.DOUBLEBUF)
        self.size = size
        pg.display.set_caption("Pong.py")
        
        pg.key.set_repeat(1,10)
        
        self.up_wall_img = self.load_image("wall.png")
        self.down_wall_img = self.load_image("wall.png")
        self.up_wall_rect = self.up_wall_img.get_rect()
        self.down_wall_rect = self.down_wall_img.get_rect()
        self.net_img = self.load_image("net.png")
        self.net_rect = self.net_img.get_rect()

        self.ball_img = self.load_image("ball.gif")
        
        pg.display.set_icon(self.ball_img)
        self.ball_rect = self.ball_img.get_rect()
        self.ball_speed = Vector(0,0)
        
        self.player1 = Player(self.load_image("player1.png"))
        self.player2 = Player(self.load_image("player2.png"))
        self.p_speed_down = Vector(0,15)
        self.p_speed_up = Vector(0,-15)

        pg.font.init()
        self.font = pg.font.Font("score_font.ttf",80)

        pg.mixer.init()
        self.hit = pg.mixer.Sound("hit.wav")
        self.clock = pg.time.Clock()
        
        self.running = True
        
    def load_image(self,filename):
        return pg.image.load(filename).convert_alpha()

    def check_collisions(self):
        if self.ball_rect.left < 0:
            self.player2.score += 1
            self.level_setup()
            return
            
            
        elif self.ball_rect.right > self.size[0]:
            self.player1.score += 1
            self.level_setup()
            return
            
        elif self.ball_rect.colliderect(self.up_wall_rect) or\
           self.ball_rect.colliderect(self.down_wall_rect):
            self.hit.play()
            self.ball_speed.y = -self.ball_speed.y
            
            
            
        elif self.ball_rect.colliderect(self.player1.rect) or\
           self.ball_rect.colliderect(self.player2.rect):
            self.hit.play()
            self.ball_speed.x = -self.ball_speed.x
            self.ball_speed.speed_up(1)
            

        if self.player1.rect.colliderect(self.up_wall_rect):
            self.player1.move(self.p_speed_down)
        elif self.player1.rect.colliderect(self.down_wall_rect):
            self.player1.move(self.p_speed_up)
        if self.player2.rect.colliderect(self.up_wall_rect):
            self.player2.move(self.p_speed_down)
        elif self.player2.rect.colliderect(self.down_wall_rect):
            self.player2.move(self.p_speed_up)
            
    def handle_events(self):
        self.ball_rect.move_ip(self.ball_speed.x,self.ball_speed.y)
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.running = False

            elif event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if keys[pg.K_UP]:
                    self.player2.move(self.p_speed_up)
                elif keys[pg.K_DOWN]:
                    self.player2.move(self.p_speed_down)
                elif keys[pg.K_w]:
                    self.player1.move(self.p_speed_up)
                elif keys[pg.K_s]:
                    self.player1.move(self.p_speed_down)
                if keys[pg.K_ESCAPE]:
                    self.running = False
                
                
    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.net_img,self.net_rect)
        self.screen.blit(self.up_wall_img,self.up_wall_rect)
        self.screen.blit(self.down_wall_img,self.down_wall_rect)
        self.screen.blit(self.ball_img, self.ball_rect)
        self.screen.blit(self.player1.image,self.player1.rect)
        self.screen.blit(self.player2.image,self.player2.rect)
        self.update_score()

        pg.display.update()

    def level_setup(self):
        self.up_wall_rect.center = (self.size[0]/2,self.up_wall_rect.height/3)
        self.down_wall_rect.center = (self.size[0]/2,self.size[1]-self.down_wall_rect.height/3)
        self.net_rect.center = (self.size[0]/2,self.size[1]/2)

        ox = self.ball_rect.right/2
        oy = self.ball_rect.bottom/2
        
        self.ball_rect.center = (self.size[0]/2,self.size[1]/2)
        self.ball_speed.x = random.choice([-4,4])
        self.ball_speed.y = random.choice([-4,4])
        self.player1.rect.center = (0,self.size[1]/2)
        self.player2.rect.center = (self.size[0],self.size[1]/2)

    def update_score(self):
        scp1 = str(self.player1.score)
        scp2 = str(self.player2.score)
        scp1_surf = self.font.render(scp1,0,RED)
        scp2_surf = self.font.render(scp2,0,BLUE)
        scp1_rect = scp1_surf.get_rect()
        scp2_rect = scp2_surf.get_rect()
        scp2_rect.move_ip(self.size[0]-scp2_rect.width,0)
        self.screen.blit(scp1_surf,scp1_rect)
        self.screen.blit(scp2_surf,scp2_rect)

    def start_screen(self):
        start_surf = self.font.render("Pong.py",0,GREEN)
        pkey_surf = self.font.render("Press space to start",0,GREEN)
        start_rect = start_surf.get_rect()
        pkey_rect = pkey_surf.get_rect()
        start_rect.center = (self.size[0]/2,self.size[1]/3)
        pkey_rect.center = (self.size[0]/2,self.size[1]/3 + 100)
        
        while True:
            for event in pg.event.get(): 
                if event.type == pg.QUIT: 
                    pg.quit()
                    sys.exit(0)

                elif event.type == pg.KEYDOWN:
                    keys = pg.key.get_pressed()
                    if keys[pg.K_SPACE]:
                        return
                    if keys[pg.K_ESCAPE]:
                        self.running = False
            self.screen.fill(BLACK)
            self.screen.blit(start_surf,start_rect)
            self.screen.blit(pkey_surf,pkey_rect)
            pg.display.update()

    def end_screen(self):
        winner = ""
        if self.player1.score > self.player2.score:
            winner = "Player 1 wins!"
        elif self.player2.score > self.player1.score:
            winner = "Player 2 wins!"
        else:
            winner = "No winner, have fun :)"
        end_surf = self.font.render(winner,0,GREEN)
        end_rect = end_surf.get_rect()
        end_rect.center = (self.size[0]/2,self.size[1]/3)
        
        while True:
            self.screen.fill(BLACK)
            self.screen.blit(end_surf,end_rect)
            
            for event in pg.event.get(): 
                if event.type == pg.QUIT: 
                    return
                if event.type == pg.KEYDOWN:
                    keys = pg.key.get_pressed()
                    if keys[pg.K_ESCAPE]:
                        return
            pg.display.update()
            
    def main_loop(self):
        self.start_screen()
        self.level_setup()
        pg.key.set_repeat()
        while self.running:
            self.handle_events()
            self.check_collisions()
            self.draw()
            self.clock.tick(60)
            
        self.end_screen()
        
        pg.font.quit()
        pg.mixer.quit()
        pg.quit()
        sys.exit(0)

if __name__=="__main__":
    game = PongGame()
    game.main_loop()
