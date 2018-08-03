import pygame

pygame.init()

# Tworzenie okna
SCREEN_WIDTH = 852
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Obrazki animacji

# Ruch w prawo
walkRight = [pygame.image.load('character1_animation/R1.png'), pygame.image.load('character1_animation/R2.png'),
             pygame.image.load('character1_animation/R3.png'), pygame.image.load('character1_animation/R4.png'),
             pygame.image.load('character1_animation/R5.png'), pygame.image.load('character1_animation/R6.png'),
             pygame.image.load('character1_animation/R7.png'), pygame.image.load('character1_animation/R8.png'),
             pygame.image.load('character1_animation/R9.png')]
# Ruch w lewo
walkLeft = [pygame.image.load('character1_animation/L1.png'), pygame.image.load('character1_animation/L2.png'),
            pygame.image.load('character1_animation/L3.png'), pygame.image.load('character1_animation/L4.png'),
            pygame.image.load('character1_animation/L5.png'), pygame.image.load('character1_animation/L6.png'),
            pygame.image.load('character1_animation/L7.png'), pygame.image.load('character1_animation/L8.png'),
            pygame.image.load('character1_animation/L9.png')]
# Tło
bg = pygame.image.load('character1_animation/bg.jpg')
# Animacja stania
char = pygame.image.load('character1_animation/standing.png')

#Sounds
bulletSound = pygame.mixer.Sound('Sounds/bullet.wav')
hitSound = pygame.mixer.Sound('Sounds/hit.wav')

music = pygame.mixer.music.load('Sounds/music.mp3')

#Ciągłe odtwarzanie muzyki
pygame.mixer.music.play(-1)

#Zegar
clock = pygame.time.Clock()

score = 0 # punktacja

class player(object):
    def __init__(self, x, y, width, height):

        #Parametry obiektu na ekranie
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        #Parametry fizyczne postaci
        self.vel = 5

        #Ustawienia hitboxów
        self.hitbox = (self.x + 17, self.y + 11, 29, 50)

        #Obsługa skoku
        self.isJump = False
        self.JumpCount = 10

        #Zmienne ruchu
        self.left = False #wykorzystana do wyświelenia 'lewej" animacji
        self.right = False #wykorzystana do wyświelenia 'prawej" aniacji
        self.WalkCOunt = 0 # licznik zmiany animacji ruchu
        self.standing = False

    def draw(self, screen):

        # Rysowanie
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):

            if self.left:
                screen.blit(walkLeft[self.walkCount // 3],(self.x, self.y))  # 9 obrazków animacja, zmiana animacji co 3 odtworzenia pętli 3*9 = 27
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x,self.y))
            else:
                screen.blit(walkLeft[0], (self.x,self.y))

        self.hitbox = (self.x + 17, self.y + 11, 29, 50)
        #pygame.draw.rect(screen, (255,0,0), self.hitbox,2)

    def hit(self):
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5',1,(255,0,0))
        screen.blit(text, ((SCREEN_WIDTH/2)-(text.get_width())/2,200))
        pygame.display.update()
        self.x = 300
        
        #Opóźnienie pozwalające zostawić napis dłużej na ekranie
        i=0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i=301
                    pygame.quit()


class projectile(object):
    def __init__(self, x,y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing # 1 lub - 1 , w zależności od strony strzału
        self.vel = 8 * facing

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)

class enemy(object):
    walkRight = [pygame.image.load('character2_animation/R1E.png'), pygame.image.load('character2_animation/R2E.png'), pygame.image.load('character2_animation/R3E.png'),
                 pygame.image.load('character2_animation/R4E.png'), pygame.image.load('character2_animation/R5E.png'), pygame.image.load('character2_animation/R6E.png'),
                 pygame.image.load('character2_animation/R7E.png'), pygame.image.load('character2_animation/R8E.png'), pygame.image.load('character2_animation/R9E.png'),
                 pygame.image.load('character2_animation/R10E.png'), pygame.image.load('character2_animation/R11E.png')]
    walkLeft = [pygame.image.load('character2_animation/L1E.png'), pygame.image.load('character2_animation/L2E.png'), pygame.image.load('character2_animation/L3E.png'),
                pygame.image.load('character2_animation/L4E.png'), pygame.image.load('character2_animation/L5E.png'), pygame.image.load('character2_animation/L6E.png'),
                pygame.image.load('character2_animation/L7E.png'), pygame.image.load('character2_animation/L8E.png'), pygame.image.load('character2_animation/L9E.png'),
                pygame.image.load('character2_animation/L10E.png'), pygame.image.load('character2_animation/L11E.png')]


    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end] #zakres ruchu postaci od początku do końca
        self.walkCount = 0
        self.vel = 3
        self.health = 10
        self.visible = True

        self.hitbox = (self.x + 17, self.y + 2 , 31, 57)

    def draw(self, screen):
        if self.visible:
            self.move() # przemieszczenie postaci przed narysowaniem

            if self.walkCount + 1 >=33: # 11 obrazków , 11 * 3 = 33
                self.walkCount = 0

            #Wybór zestawu obrazków w zależności od kierunku ruchu
            if self.vel > 0:
                screen.blit(enemy.walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                screen.blit(enemy.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1

            #Paski życia
            pygame.draw.rect(screen, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50 , 10))
            pygame.draw.rect(screen, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 * (1-(10-self.health)/10), 10)) #Redukcja paska zielonego z każdym uderzeniem

            self.hitbox = (self.x + 17, self.y + 2 , 31, 57)
            #pygame.draw.rect(screen, (255,0,0), self.hitbox,2)



    def move(self):

            # Ruch w prawo aż do osiągnięcia wartości "end"
            if self.vel >0:
                if self.x + self.vel <self.path[1] :
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0
            # Zmiana kierunku ruchu
            else:
                if self.x - self.vel  > self.path[0]:
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                    self.walkCount = 0

    def hit(self):
        #Obniżanie życia przy uderzeniu
        if self.health > 0:
            self.health -=1
        else:
            self.visible = False
        hitSound.play()


def redrawGameWindow():

    # Resetowanie okna
    screen.blit(bg, (0, 0))  # Ustawienie obrazka tła

    text = font.render('Score:' + str(score),1,(0,0,0)) #Wyrenderowanie napisu na podstawie zmiennej font
    screen.blit(text, (390,10))

    man.draw(screen)
    goblin.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.update()


# Główna pętla gry
font = pygame.font.SysFont('comicsans', 30, True, True)
man = player(300,410, 64,64) # instancja klasy player
goblin = enemy(100, 410, 64, 64, 450)
bullets = [] #lista przechowująca wszystkie wystrzelone aktualnie kule
run = True

#Obsługa strzałów
shootCount = 0

while run:
    clock.tick(27)  # ilość klatek na sekundę, FPS


    # Obsługa wydarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Sprawdzanie kolizji man i goblin

    if man.hitbox[1]  < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:  # sprawdzenie współrzędnej y
        if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0]  < goblin.hitbox[0] + goblin.hitbox[2]:  # sprawdzenie współrzędnej x
            man.hit()
            score -= 5  # zmniejszenie punktacji w momencie kolizji


    for bullet in bullets:

        #Sprawdzenie kolizji bullet i goblin
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]: # sprawdzenie współrzędnej y
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]: # sprawdzenie współrzędnej x
                goblin.hit()
                score += 1 # zwiększenie punktacji w momencie trafienia goblina
                bullets.pop(bullets.index(bullet)) # usunięcie kuli

        if bullet.x < SCREEN_WIDTH and bullet.x > 0: # sprawdzenie czy kula znajduje się w obrębie ekranu
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet)) # usunięcie kuli

    # Obsługa sterowania
    keys = pygame.key.get_pressed()

    #Obsłucha ilości wystrzelonych kul

    if shootCount > 0:
        shootCount += 1
    if shootCount >3:
        shootCount = 0

    #Strzał
    if keys[pygame.K_SPACE] and shootCount == 0:
        if man.left: # określenie w którą stronę patrzy postać
            facing = -1
        else:
            facing = 1

        if len(bullets) < 5: # ograniczenie ilości kul na ekranie
            bullets.append(projectile(round(man.x + man.width//2), round(man.y + man.height//2), 6,(0,0,0), facing))
            bulletSound.play()

        shootCount = 1

    # Porusznia lewa, prawa
    if keys[pygame.K_LEFT] and man.x > 0:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < (SCREEN_WIDTH - man.width):
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    # Moduł skoku
    if man.isJump:

        if man.JumpCount >= -10:

            if man.JumpCount < 0:
                neg = -1
            else:
                neg = 1
            man.y -= neg * (man.JumpCount ** 2) * 0.5
            man.JumpCount -= 1
        else:
            man.isJump = False
            man.JumpCount = 10

    else:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0

    redrawGameWindow()
pygame.quit()
