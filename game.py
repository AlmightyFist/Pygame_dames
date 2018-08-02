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

#Zegar
clock = pygame.time.Clock()

# Parametry obiektu Rectangle
x = 50
y = 416
width = 64
height = 64

# Parametry fizyczne
vel = 5  # prędkość

# Obsługa skoku

isJump = False
JumpCount = 10

# Zmienne ruchu
left = False #wykorzystana do wyświelenia 'lewej" animcaji
right = False ##wykorzystana do wyświelenia 'prawej" animcaji
walkCount = 0


def redrawGameWindow():
    global walkCount  # praca na zmiennej globalnej
    # Resetowanie okna
    screen.blit(bg, (0, 0))  # Ustawienie obrazka tła

    # Rysowanie
    if walkCount + 1 >= 27:
        walkCount = 0

    if left:
        screen.blit(walkLeft[walkCount//3], (x,y)) #9 obrazków animacja, zmiana animacji co 3 odtworzenia pętli 3*9 = 27
        walkCount +=1
    elif right:
        screen.blit(walkRight[walkCount//3], (x,y))
        walkCount +=1
    else:
        screen.blit(char, (x,y))
    pygame.display.update()


# Główna pętla gry
run = True

while run:
    clock.tick(27)  # ilość klatek na sekundę, FPS

    # Obsługa wydarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Obsługa sterowania
    keys = pygame.key.get_pressed()

    # Porusznia lewa, prawa
    if keys[pygame.K_LEFT] and x > 0:
        x -= vel
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < (SCREEN_WIDTH - width):
        x += vel
        right = True
        left = False
    else:
        right = False
        left = False
        walkCount = 0

    # Moduł skoku
    if isJump:

        if JumpCount >= -10:

            if JumpCount < 0:
                neg = -1
            else:
                neg = 1
            y -= neg * (JumpCount ** 2) * 0.5
            JumpCount -= 1
        else:
            isJump = False
            JumpCount = 10

    else:
        if keys[pygame.K_SPACE]:
            isJump = True
            right = False
            left = False
            walkCount = 0

    redrawGameWindow()
pygame.quit()
