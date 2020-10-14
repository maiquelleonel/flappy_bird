#!/bin/python3
import pygame
import random
from pygame.locals import *

GAME_FPS = 30
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10
GROUND_WIDTH = SCREEN_WIDTH
GROUND_HEIGHT = 100
PIPE_GAP = 200
PIPE_WIDTH = 50
PIPE_HEIGHT = 500

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [
            pygame.image.load("assets/bird-upflap.png").convert_alpha(),
            pygame.image.load("assets/bird-midflap.png").convert_alpha(),
            pygame.image.load("assets/bird-downflap.png").convert_alpha(),
        ]

        self.current_image = 0
        self.speed = SPEED
        self.image = pygame.image.load("assets/bird-upflap.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 3
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED


class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("assets/base.png")
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED


class Background(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("assets/bg.png")
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos

    def update(self):
        self.rect[0] -= GAME_SPEED / 10


class Pipe(pygame.sprite.Sprite):
    def __init__(self, xpos, ysize, inverted=False):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("assets/pipe-green.png")
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = -(self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED


def is_off_screen(sprite):
    return sprite.rect[0] < -sprite.rect[2]


def get_random_pipes(xpos):
    size = random.randint(100, 400)
    pipe = Pipe(xpos, size)
    inverted_pipe = Pipe(xpos, SCREEN_HEIGHT - size - PIPE_GAP, True)
    return (pipe, inverted_pipe)


bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

bg_group = pygame.sprite.Group()
ground_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

for i in range(2):
    bg_group.add(Background(SCREEN_WIDTH * i))
    ground_group.add(Ground(SCREEN_WIDTH * i))
    pipes = get_random_pipes(SCREEN_WIDTH * i + 950)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()

while True:
    clock.tick(GAME_FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()

    if is_off_screen(bg_group.sprites()[0]):
        bg_group.remove(bg_group.sprites()[0])
        bg_group.add(Background(SCREEN_WIDTH))

    bg_group.update()
    bg_group.draw(screen)

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(SCREEN_WIDTH - 10)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])
        pipes = get_random_pipes(SCREEN_WIDTH * 3)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.update()
    pipe_group.update()
    ground_group.update()

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

    collide_ground = pygame.sprite.groupcollide(
        bird_group, ground_group, False, False, pygame.sprite.collide_mask
    )

    collide_pipe = pygame.sprite.groupcollide(
        bird_group, pipe_group, False, False, pygame.sprite.collide_mask
    )

    if collide_ground or collide_pipe:
        input()
        break
