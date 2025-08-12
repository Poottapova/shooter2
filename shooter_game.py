#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as timer
font.init()
font2 = font.Font(None, 36)
win = font2.render("You win", True,(66, 245, 209))
lose = font2.render("Твой дом мы продаём за долги!!", True, (180, 0 , 0))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()


fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.3)

window_width = 700
window_height = 500
window = display.set_mode((window_width, window_height))
display.set_caption("Space Shooter🛸🛰")
img_back = 'galaxy.jpg'
backgroup = transform.scale(image.load(img_back), (window_width, window_height))
run = True
finish = False

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def draw(self):
        window.blit(self.image, (self.rect.x , self.rect.y))

class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 3:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < window_width - 80:
            self.rect.x += self.speed
    
    def fire(self):
        bullet  = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

skore = 0
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        global lost
        if self.rect.y > window_height:
            self.rect.y = 0
            self.rect.x = randint(1,window_width-80)
            lost += 1

class EnemyAsteroid(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        if self.rect.y > window_height:
            self.rect.y = 0
            self.rect.x = randint(1,window_width-80)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

        
bullets = sprite.Group()

monsters = sprite.Group()
for i in range(1,10):
    monster = Enemy("ufo.png",randint(1, window_width-80), -40, 80, 50,randint(1,5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(2):
    asteroid = EnemyAsteroid("asteroid.png",randint(1, window_width-80), -40, 80, 50,randint(1,5))
    asteroids.add(asteroid)

ship = Player("rocket.png", 5, window_height - 100, 80, 100, 10)


lives = 5
color_lives = [
    (107, 0,0),
    (187, 0 ,0),
    (173, 86, 9),
    (250, 217, 0),
    (157, 181, 2),
    (0, 199, 43)
]

rel_time = False
num_fire = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time ==False:
                    num_fire = num_fire + 1
                    ship.fire()
                    fire_sound.play()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:

        window.blit(backgroup, (0,0))
        ship.move()

        monsters.update()
        bullets.update()
        asteroids.update()


        if rel_time == True:
            now_time  = timer()

            if now_time - last_time < 3:
                reload = font2.render('Подождите, идёт reload', 1,(150, 0 , 0))
                window.blit(reload,(260, 460))

            else :
                num_fire = 0
                rel_time = False

        ship.draw()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        text_win = font2.render('Счёт: '+str(skore), 1, (255, 255, 255))
        window.blit(text_win, (10, 20))

        text = font2.render('Пропущено: '+str(lost),1,(255,255,255))
        window.blit(text, (10, 50))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            skore += 1
            monster = Enemy("ufo.png",randint(1, window_width-80), -40, 80, 50,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, True):
            lives-= 1
            monster = Enemy("ufo.png",randint(1, window_width-80), -40, 80, 50,randint(1,5))
            monsters.add(monster)


        collides = sprite.groupcollide(asteroids, bullets, True, True)
        for i in collides:
            asteroid = EnemyAsteroid("asteroid.png",randint(1, window_width-80), -40, 80, 50,randint(2,25))
            asteroids.add(asteroid)
        if sprite.spritecollide(ship, asteroids, True):
            lives -= 1
            asteroid = EnemyAsteroid("asteroid.png",randint(1, window_width-80), -40, 80, 50,randint(1,30))
            asteroids.add(asteroid)

        if skore >= 10:
            finish = True
            window.blit(win, (150, 150))
        if lost >=10 or lives <= 0:
            finish = True
            window.blit(lose, (150, 150))
        
        text_lives = font2.render(str(lives), 1, color_lives[lives])
        window.blit(text_lives,(650, 20))



    display.update()
    time.delay(50)


'''from pygame import *
from random import randint
from time import time as timer
#текст
font.init()
font2 = font.Font(None,36)


#границы и т.д
win_weight = 700
win_height = 500
clock = time.Clock()
fps = 60
score = 0


#ещё что-то
window = display.set_mode((win_weight,win_height))
display.set_caption('Чюпеп')
back = transform.scale(image.load('galaxy.jpg'),(win_weight,win_height))


#музуыка какая-то
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)





#звук выстрела
fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.1)


#классы
class GameSprite(sprite.Sprite):
   def __init__(self,player_image,player_x,player_y,player_speed):
       super().__init__()
       self.image = transform.scale(image.load(player_image),(65,65))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def draw(self):
       window.blit(self.image,(self.rect.x,self.rect.y))
  


class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_w] and self.rect.y > 5:
           self.rect.y -= self.speed
       if keys[K_s] and self.rect.y < win_height - 80:
           self.rect.y += self.speed
       if keys[K_a] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_d] and self.rect.x < win_weight - 80:
           self.rect.x += self.speed
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_weight - 80:
           self.rect.x += self.speed
      
   def fire(self):
       bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,-15)
       bullets.add(bullet)
      
      


lost = 0


class Enemy(GameSprite):
   def update(self):
      
       self.rect.y += self.speed
       global lost
       if self.rect.y > win_height:
           self.rect.y = 0
           self.rect.x = randint(80, win_weight -80)
           lost += 1
monsters = sprite.Group()
for i in range(1, 4):
   monster = Enemy("ufo.png", randint(80, win_weight -80),-40,randint(1,3))
   monsters.add(monster)


class EnemyAsteroids(GameSprite):
   def update(self):
       self.rect.y += self.speed
       if self.rect.y > win_height:
           self.rect.y = 0
           self.rect.x = randint(80, win_weight -80)


#астеройды (я не знаю, что они тут делают)
asteroids = sprite.Group()
for _ in range(1,4):
   asteroid = EnemyAsteroids('asteroid.png',randint(80, win_weight -80),-40,randint(1,5))
   asteroids.add(asteroid)




#ещё класс (я не знаю что он тут делает)
class Bullet(GameSprite):
   def update(self):
       self.rect.y += self.speed
       if self.rect.y < 0:
           self.kill()
#что-то 
bullets = sprite.Group()






ship = Player('rocket.png',50,420,4)


#помощь к циклу
lives = 3
rel_time = False
num_fire = 0
game = True
finish = False


#цикл
while game:
  
   for i in event.get():
       if i.type == QUIT:
           game = False
           #перезарядка
       elif i.type == KEYDOWN:
           if i.key == K_SPACE:
               if num_fire < 5 and rel_time == False:
                   num_fire = num_fire + 1
                   ship.fire()
                   fire_sound.play()


           if num_fire >= 5 and rel_time == False:
               last_time = timer()
               rel_time = True


   if finish != True:
       window.blit(back,(0,0))


       if rel_time == True:
           now_time = timer()


           if now_time - last_time < 3:
               reload = font2.render('Reload...',1,(150,0,0))
               window.blit(reload,(260,460))
               #звук перезарядки (не обращайте внимания)
               #reload_sound.play()
           else:
               num_fire = 0
               rel_time = False


              
       #отрисовка
       ship.update()
       ship.draw()
       monsters.update()
       monsters.draw(window)
       bullets.update()
       bullets.draw(window)
       asteroids.update()
       asteroids.draw(window)
      
       #Счёт и т.п
       score_text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
       window.blit(score_text, (10, 10))
      
      
       text = font2.render('Пропущено: '+str(lost),1,(255,255,255))
       window.blit(text,(10,30))
       if lost >= 10:
           lost = 10
           finish = True
           text2 = font2.render('йцуйцуйцкйцейце',1,(255,255,255))
           window.blit(text2,(300,250))


       collides = sprite.groupcollide(monsters,bullets,True,True)
       for _ in collides:
           score += 1
           monster = Enemy('ufo.png',randint(80, win_weight - 80),-40,randint(1,3))
           monsters.add(monster)


       boom = sprite.spritecollide(ship,asteroids,True)
       boom2 = sprite.spritecollide(ship,monsters,True)
       if boom:
           lives -= 1
          
       if boom2:
           lives -= 1


      
       lives_text = font2.render('Жизни:'+str(lives),1,(173, 255, 47))
       window.blit(lives_text,(500,50))
       if lives == 2:
           lives_text = font2.render('Жизни:'+str(lives),1,(255, 255, 0))
           window.blit(lives_text,(500,50))
       if lives == 1:
           lives_text = font2.render('Жизни:'+str(lives),1,(255, 0, 0))
           window.blit(lives_text,(500,50))


       if lives <= 0:
           fail_text = font2.render('Ракета уничтожена',1,(255,0,0))
           window.blit(fail_text,(300,250))
           finish = True


       if score == 10:
           win_text = font2.render('Победа',1,(173, 255, 47))
           window.blit(win_text,(300,250))
           finish = True
          
   #конец
   display.update()
   clock.tick(fps)'''
