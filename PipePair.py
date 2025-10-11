import pygame.image


def rect_rect(r1x, r1y, r1w, r1h, r2x, r2y, r2w, r2h):
    if (r1x + r1w >= r2x and r1x <= r2x + r2w and r1y + r1h >= r2y and r1y <= r2y + r2h):
        return True
    return False


class PipePair:
    def __init__(self, x, y, screen):
        self.pair_x = x
        self.pair_y = y
        self.top_im = pygame.image.load("PipeTop.png")
        self.bottom_im = pygame.image.load("PipeBottom.png")
        self.w = self.bottom_im.get_width()
        self.h_of_one = self.bottom_im.get_height()
        self.gap = 170
        self.screen = screen
        self.y_bottom_pipe_top_left = self.pair_y + self.gap / 2 + self.h_of_one / 2
        self.y_top_pipe_top_left = self.pair_y - self.gap / 2 - self.h_of_one / 2
        self.y_top_pipe_bottom_left = self.y_top_pipe_top_left + self.h_of_one

    def update(self):
        self.pair_x -= 3
        self.display()

    def display(self):
        self.screen.blit(self.top_im, (self.pair_x, self.y_top_pipe_top_left))
        self.screen.blit(self.bottom_im, (self.pair_x, self.y_bottom_pipe_top_left))
        # self.screen.set_at((self.pair_x + self.w, int(self.y_top_pipe_top_left) + self.h_of_one), (255, 0, 0))
        # self.screen.set_at((self.pair_x + self.w, int(self.y_bottom_pipe_top_left) + self.h_of_one), (255, 0, 0))
        pygame.draw.rect(self.screen, (255, 0, 0), (self.pair_x, int(self.y_top_pipe_top_left), self.w, self.h_of_one),
                         width=3)
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.pair_x, int(self.y_bottom_pipe_top_left), self.w, self.h_of_one), width=3)
        pygame.draw.circle(self.screen, (0, 0, 255), (self.pair_x, int(self.y_top_pipe_bottom_left)), 2)

    def check_collision(self, player):
        if rect_rect(player.x - (player.w / 2), player.y - (player.h / 2), player.w, player.h, self.pair_x, self.y_top_pipe_top_left, self.w, self.h_of_one):
            return True
        if rect_rect(player.x - (player.w / 2), player.y - (player.h / 2), player.w, player.h, self.pair_x, self.y_bottom_pipe_top_left, self.w, self.h_of_one):
            return True
        return False
        # https://www.jeffreythompson.org/collision-detection/rect-rect.php
