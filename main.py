import pygame
import random

pygame.init()
screen = pygame.display.set_mode((640, 480))
GAME_FONT = pygame.font.Font("Pixeled.ttf", 24)
done = False

class Car:
    image = pygame.image.load("car.png").convert_alpha()
    rect = image.get_rect()
    pos = [0, 0]
    movementRate = 0

    def __init__(self, pos, movementRate):
        self.pos = pos
        self.movementRate = movementRate

    def render(self, screen):
        screen.blit(self.image, self.pos)
    
    def update(self, player):
        self.pos[0] -= self.movementRate
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())
        if self.rect.colliderect(player.rect):
            player.alive = False
            player.deathSound.play()

class Player:
    image = pygame.image.load("player.png").convert_alpha()
    rect = image.get_rect()
    pos = [10, 10]
    alive = True
    scoreSound = pygame.mixer.Sound('beep.wav')
    deathSound = pygame.mixer.Sound('death.wav')

    def render(self, screen):
        screen.blit(self.image, self.pos)

    def update(self, event):
        keys_pressed = pygame.key.get_pressed()
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.image.get_width(), self.image.get_height())

        if keys_pressed[pygame.K_DOWN]:
            self.pos[1] += 3
        elif keys_pressed[pygame.K_UP]:
            self.pos[1] -= 3
        if keys_pressed[pygame.K_LEFT]:
            self.pos[0] -= 3
        elif keys_pressed[pygame.K_RIGHT]:
            self.pos[0] += 3


player = Player()

clock = pygame.time.Clock()

cars = []

carTimer = 50

score = 0

pygame.mixer.music.load('song.mp3')
pygame.mixer.music.play(-1)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill((0, 0, 0))
    # Update
    if player.alive:
        if carTimer <= 0:
            carTimer = 75
            carPos = [640, random.randint(0, 480)]
            carMovementRate = random.randint(4, 7)
            cars.append(Car(carPos, carMovementRate))
        else:
            carTimer -= 1
        for i in cars:
            i.update(player)
            if i.pos[0] <= -300:
                score += 1
                player.scoreSound.play()
                cars.remove(i)

        player.update(event)

    else:
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_r]:
            cars = []
            player.pos = [0, 240]
            score = 0
            player.alive = True
    
    # Render
    player.render(screen)
    for i in cars:
        i.render(screen)

    text_surface = GAME_FONT.render(str(score), False, (0, 255, 50))
    screen.blit(text_surface, (10,-20))

    if not player.alive:
        death_text_surface = GAME_FONT.render('You lost! Press "R" to restart!', False, (255, 50, 50))
        score_text_surface = GAME_FONT.render('Score: ' + str(score), False, (255, 255, 255))
        screen.blit(death_text_surface, (10, 240))
        screen.blit(score_text_surface, (260, 280))

    pygame.display.flip()
    clock.tick(60)
