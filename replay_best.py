import pickle
import sys
import time
import pygame
from Player import Player
from PipeManager import PipeManager
import neat

# Three inputs:
# 1. Horizontal distance to pipe (x-diff)
# 2. Vertical distance to the top pipe's bottom edge
# 3. Vertical distance to the bottom pipe's top edge

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)
game_speed = 1

screen = pygame.display.set_mode((600, 700))
screen.fill("green")
pygame.display.set_caption("Flappy Bird - NEAT Final Demo")
best_genome = None


def eval_genomes(genomes, config):
    global game_speed
    birds = []
    genos = []
    nets = []

    pipe_manager = PipeManager(screen)

    for genome_id, genome in genomes:
        birds.append(Player(screen, pipe_manager, (225, 110, 150)))
        genos.append(genome)
        nets.append(neat.nn.FeedForwardNetwork.create(genome, config))
        genome.fitness = 0

    start = time.time()

    while len(birds) != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == ord("b"):
                    print(genos)
                    breakpoint()
                elif event.key == ord("q"):
                    pygame.quit()
                    sys.exit()
                elif event.key == ord("f"):
                    game_speed += 1
                elif event.key == ord("s"):
                    game_speed -= 1
        pic = font.render(f"Speed: {game_speed}", True, (0, 0, 0))
        pic2 = font.render(f"Score: {round(time.time() - start)}", True, (0, 0, 0))
        screen.fill("green")
        for i, bird in enumerate(birds):
            output = nets[i].activate(pipe_manager.get_closest_pipe_pair_to_player(bird)[0:3])
            if output[0] > 0.5 and not bird.flapping:
                bird.flap()
            bird.update()
            if pipe_manager.check_collided(bird):
                bird.alive = False
            if not bird.alive:
                i = birds.index(bird)
                genos[i].fitness = (time.time() - start) * game_speed
                genos.pop(i)
                birds.pop(i)
                nets.pop(i)
        pipe_manager.update()
        screen.blit(pic, (20, 600))
        screen.blit(pic2, (20, 650))
        pygame.display.flip()
        clock.tick(60 * game_speed)


def run_ai(config_path):
    global best_genome
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    with open("winner.pkl", "rb") as f:
        best_genome = pickle.load(f)
    eval_genomes([(1, best_genome)], config)
    breakpoint()


if __name__ == "__main__":
    run_ai("C:/Users/qayim/PycharmProjects/FlappyBird_AI/config.txt")
