import random
import pygame


def get_dist_from_green(col):
    tot = 0
    green = (255, 0, 0)
    for i in range(3):
        tot += abs(col[i] - green[i])
    return tot


class Player:
    def __init__(self, screen, pipe_manager, color=None):
        self.color = None
        self.x = 300
        self.y = 350
        self.flapping = False
        self.im = pygame.image.load("Flappy.gif").convert_alpha()
        self.screen = screen
        self.w = self.im.get_width()
        self.h = self.im.get_height()
        self.vel_y = -9
        self.max_vel_y = 10
        self.min_vel_y = -8
        self.acc_y = 0.8
        self.flap_vel = -10
        self.alive = True
        self.pipe_man = pipe_manager
        if color is None:
            self.assign_color()
        else:
            self.color = color

    def update(self):
        if self.vel_y < self.max_vel_y and not self.flapping:
            self.vel_y += self.acc_y
        if self.flapping:
            self.flapping = False
        self.y = self.y + min(self.vel_y, 700 * 0.95 - self.y - self.h)
        if self.check_death_by_ground():
            self.alive = False
    # if self.flapping:
    #         if self.flap_time >= self.max_flap_time:
    #             self.flap_time = 0
    #             self.flapping = False
    #         else:
    #             self.y -= 20
    #             self.flap_time += 1
    #     else:
    #         self.y += 8
        self.display()

    def display(self):
        self.screen.blit(self.im, (self.x - self.w/2, self.y - self.h/2))
        pygame.draw.rect(self.screen, self.color, (self.x - self.w / 2, self.y - self.h / 2, self.w, self.h), width=4)
        pipe_man_res = self.pipe_man.get_closest_pipe_pair_to_player(self)[3]
        pygame.draw.line(self.screen, self.color, (self.x + self.w / 2, self.y - self.h / 2), (pipe_man_res.pair_x, pipe_man_res.y_top_pipe_bottom_left))

    def flap(self):
        if self.y > 0:
            self.vel_y = self.flap_vel
            self.flapping = True
        else:
            self.alive = False

    def check_death_by_ground(self):
        if self.y > 608:
            return True
        return False

    def assign_color(self):
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        while get_dist_from_green(self.color) < 50:
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
