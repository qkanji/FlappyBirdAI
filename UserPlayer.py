import sys
import pygame
from Player import Player
from PipeManager import PipeManager

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((600, 700))
screen.fill("green")

player = Player(screen)
pipe_manager = PipeManager(screen)

while player.alive:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == ord(" "):
                player.flap()
            elif event.key == ord("q"):
                pygame.quit()
                sys.exit()
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill("green")
    player.update()
    pipe_manager.update()
    if pipe_manager.check_collided(player):
        player.alive = False
    pygame.display.flip()
    clock.tick(60)
