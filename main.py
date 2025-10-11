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
game_speed = 4

screen = pygame.display.set_mode((600, 700))
screen.fill("green")
pygame.display.set_caption("Flappy Bird - NEAT Training")
gens = 0
best_genome = None
best_fitness = 0
gen_to_highest_fitness = [0]


def eval_genomes(genomes, config):
    global gens, best_fitness, game_speed
    birds = []
    genos = []
    nets = []
    gens += 1
    pic2 = font.render(f"Gen: {gens}", True, (0, 0, 0))

    pipe_manager = PipeManager(screen)

    for genome_id, genome in genomes:
        birds.append(Player(screen, pipe_manager))
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
                    print(gen_to_highest_fitness)
                    print(genos)
                    breakpoint()
                elif event.key == ord("q"):
                    pygame.quit()
                    sys.exit()
                elif event.key == ord("p"):  # P for Preserve
                    with open("winner.pkl", "wb") as f:
                        pickle.dump(genos[0], f)
                # elif event.key == ord("f"):
                #     game_speed *= 1.5
                # elif event.key == ord("s"):
                #     game_speed /= 1.5
        pic = font.render(f"Best Fitness: {best_fitness}", True, (0, 0, 0))
        pic3 = font.render(f"Score: {round(time.time() - start)}", True, (0, 0, 0))
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
                if genos[i].fitness > best_fitness:
                    best_fitness = round(genos[i].fitness, 2)
                genos.pop(i)
                birds.pop(i)
                nets.pop(i)
        pipe_manager.update()
        screen.blit(pic, (20, 600))
        screen.blit(pic2, (20, 650))
        screen.blit(pic3, (50, 0))
        pygame.display.flip()
        clock.tick(60 * game_speed)
    gen_to_highest_fitness.append(best_fitness)


def run_ai(config_path):
    global best_genome
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    pop = neat.Population(config)
    best_genome = pop.run(eval_genomes, None)
    breakpoint()


if __name__ == "__main__":
    run_ai("config.txt")
