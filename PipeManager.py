import math
import random
from PipePair import PipePair


def dist(x1, x2, y1, y2):
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))


class PipeManager:
    def __init__(self, screen):
        self.screen = screen
        self.pipes = [PipePair(500, 0, self.screen), PipePair(803, 200, self.screen)]
        self.pipe_cooldown = -100
        self.new_pipe_time = 100

    def check_add_new_pipe_pair(self):
        if self.pipe_cooldown >= self.new_pipe_time:
            self.pipe_cooldown = 0
            self.pipes.append(PipePair(700, random.randrange(-150, 250), self.screen))
        else:
            self.pipe_cooldown += 1

    def check_del_a_pair(self):
        if len(self.pipes) == 0:
            return
        if self.pipes[0].pair_x < -100:
            self.pipes.pop(0)

    def update(self):
        self.check_add_new_pipe_pair()
        self.check_del_a_pair()
        for pair in self.pipes:
            pair.update()
        self.display()

    def display(self):
        for pair in self.pipes:
            pair.display()

    def check_collided(self, player):
        for pair in self.pipes:
            if pair.check_collision(player):
                return True
        return False

    def destroy(self):
        self.pipes = []

    def get_closest_pipe_pair_to_player(self, player):
        min_dist = 1000000
        min_pipe = None
        for pipe in self.pipes:
            dista = abs(player.x - pipe.pair_x)
            if (dista < min_dist) and ((pipe.pair_x + pipe.w) > (player.x - player.w / 2)):
                min_pipe = pipe
                min_dist = dista

        return min_pipe.pair_x - player.x + player.w / 2,\
            min_pipe.y_top_pipe_bottom_left - player.y - player.h / 2,\
            min_pipe.y_top_pipe_top_left - player.y + player.h / 2, min_pipe
