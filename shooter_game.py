#Create your own shooter

from pygame import *
from random import randint
window = display.set_mode((700, 500))
display.set_caption('Shooters')
bg = transform.scale(image.load('galaxy.jpg'),(700, 500))


class Game(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

bullets = sprite.Group()
sum_bullet = 0
class Player(Game):
    def update(self):
        keys = key.get_pressed()

        if keys[K_a] and self.rect.x > 50:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 600:
            self.rect.x += self.speed
        if keys[K_RSHIFT]:
            self.Fire()

    def Fire(self):
        fire_sound.play()
        global sum_bullet
        if sum_bullet < 30:
            bullet = Bullets('bullet.png',self.rect.centerx, self.rect.top, 15, 20, -15)
            bullets.add(bullet)
        
        else:
            window.blit(text_reload, (300, 450))
        
        if sum_bullet > 50:
            sum_bullet = 0
        sum_bullet += 1


lose = 0
class Enemy(Game):
    def update(self):
        self.rect.y += self.speed
        global lose
        if self.rect.y > 500 :
            self.rect.y = -40
            self.rect.x  = randint(10, 650)
            self.speed = randint(1, 5)
            lose += 1

class Asteroid(Game):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500 :
            self.rect.y = -40
            self.rect.x  = randint(10, 650)
            self.speed = randint(1, 5)
            

class Bullets(Game):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        

monsters = sprite.Group()
sum_enemy = 8
for i in range(sum_enemy):
    monster = Enemy('ufo.png', randint(10, 650), -40,100,50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1):
    asteroid = Asteroid('asteroid.png', randint(10, 650), -40,100,50, randint(1, 5)) 
    asteroids.add(asteroid)
#Music
mixer.init()
mixer_music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.play()
#===================
font.init()
font1 = font.SysFont(None, 36)



run = True
game = True
clock = time.Clock()
Hero = Player('rocket.png',400,400,65,90,10)

font.init()
font2 = font.SysFont(None, 60)
text_win = font2.render('GREAT',True, (0,255,255))
text_fail = font2.render(' TRY AGAIN', True, (255,255,255))

font3 = font.SysFont(None, 30)
text_reload = font3.render('--🔄Reload🔄--',True, (0,255,255))
while run :
    for e in event.get():
        if e.type == QUIT:
            run = False
    
    window.blit(bg,(0,0))
    if sprite.collide_rect(Hero, monster): 
        window.blit(text_fail, (250, 250))
        game = False
    if lose >=5 : 
        window.blit(text_fail, (250, 250))
        game = False
    if sprite.collide_rect(Hero,asteroid):
        window.blit(text_fail, (250, 250))
        game = False
    collides = sprite.groupcollide (bullets,monsters,True, True)
    sprite.groupcollide (bullets,asteroids,True, False)


    if len (monsters)== 0:
        window.blit(text_win, (255,255))

    text_lose = font1.render('Missed : ' + str(lose), 1, (255, 255, 255))
    window.blit(text_lose, (10, 10))

    if game:
        asteroids.draw(window)
        asteroids.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        Hero.reset()
        Hero.update()
    display.update()
    clock.tick(40)
    
    
    
