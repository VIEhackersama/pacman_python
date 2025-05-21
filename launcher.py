import copy
from board import matrix
import pygame
import math

pygame.init()

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
color = 'blue'
PI = math.pi
player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))
red_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45, 45))
hong_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45, 45))
blue_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45, 45))
orange_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45, 45))
player_x = 450
player_y = 663
direction = 0
red_x = 56
red_y = 58
red_direction = 0
blue_x = 440
blue_y = 388
blue_direction = 2
hong_x = 440
hong_y = 438
hong_direction = 2
orange_x = 440
orange_y = 438
orange_direction = 2
counter = 0
flicker = False
# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
red_dead = False
blue_dead = False
orange_dead = False
hong_dead = False
red_box = False
blue_box = False
orange_box = False
hong_box = False
moving = False
ghost_speeds = [2, 2, 2, 2]
startup_counter = 0
lives = 3
game_over = False
game_won = False


class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_img, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        # R, L, U, D
        chieudai = ((HEIGHT - 50) // 32)
        chieurong = (WIDTH // 30)
        trungdiem = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if matrix[(self.center_y - trungdiem) // chieudai][self.center_x // chieurong] == 9:
                self.turns[2] = True
            if matrix[self.center_y // chieudai][(self.center_x - trungdiem) // chieurong] < 3 \
                    or (matrix[self.center_y // chieudai][(self.center_x - trungdiem) // chieurong] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if matrix[self.center_y // chieudai][(self.center_x + trungdiem) // chieurong] < 3 \
                    or (matrix[self.center_y // chieudai][(self.center_x + trungdiem) // chieurong] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if matrix[(self.center_y + trungdiem) // chieudai][self.center_x // chieurong] < 3 \
                    or (matrix[(self.center_y + trungdiem) // chieudai][self.center_x // chieurong] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if matrix[(self.center_y - trungdiem) // chieudai][self.center_x // chieurong] < 3 \
                    or (matrix[(self.center_y - trungdiem) // chieudai][self.center_x // chieurong] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % chieurong <= 18:
                    if matrix[(self.center_y + trungdiem) // chieudai][self.center_x // chieurong] < 3 \
                            or (matrix[(self.center_y + trungdiem) // chieudai][self.center_x // chieurong] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if matrix[(self.center_y - trungdiem) // chieudai][self.center_x // chieurong] < 3 \
                            or (matrix[(self.center_y - trungdiem) // chieudai][self.center_x // chieurong] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % chieudai <= 18:
                    if matrix[self.center_y // chieudai][(self.center_x - chieurong) // chieurong] < 3 \
                            or (matrix[self.center_y // chieudai][(self.center_x - chieurong) // chieurong] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if matrix[self.center_y // chieudai][(self.center_x + chieurong) // chieurong] < 3 \
                            or (matrix[self.center_y // chieudai][(self.center_x + chieurong) // chieurong] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % chieurong <= 18:
                    if matrix[(self.center_y + trungdiem) // chieudai][self.center_x // chieurong] < 3 \
                            or (matrix[(self.center_y + trungdiem) // chieudai][self.center_x // chieurong] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if matrix[(self.center_y - trungdiem) // chieudai][self.center_x // chieurong] < 3 \
                            or (matrix[(self.center_y - trungdiem) // chieudai][self.center_x // chieurong] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % chieudai <= 18:
                    if matrix[self.center_y // chieudai][(self.center_x - trungdiem) // chieurong] < 3 \
                            or (matrix[self.center_y // chieudai][(self.center_x - trungdiem) // chieurong] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if matrix[self.center_y // chieudai][(self.center_x + trungdiem) // chieurong] < 3 \
                            or (matrix[self.center_y // chieudai][(self.center_x + trungdiem) // chieurong] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_orange(self):
        # r, l, u, d
        # orange is going to turn whenever advantageous for pursuit
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_red(self):
        # r, l, u, d
        # red is going to turn whenever colliding with walls, otherwise continue straight
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_blue(self):
        # r, l, u, d
        # blue turns up or down at any point to pursue, but left and right only on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_hong(self):
        # r, l, u, d
        # blue is going to turn left or right whenever advantageous, but only up or down on collision
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction


def draw_score():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
        screen.blit(gameover_text, (100, 300))


def check_collisions(scor, power, power_count, eaten_ghosts):
    chieudai = (HEIGHT - 50) // 32
    chieurong = WIDTH // 30
    if 0 < player_x < 870:
        if matrix[center_y // chieudai][center_x // chieurong] == 1:
            matrix[center_y // chieudai][center_x // chieurong] = 0
            scor += 10
        if matrix[center_y // chieudai][center_x // chieurong] == 2:
            matrix[center_y // chieudai][center_x // chieurong] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scor, power, power_count, eaten_ghosts


def draw_matrix():
    chieudai = ((HEIGHT - 50) // 32)
    chieurong = (WIDTH // 30)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * chieurong + (0.5 * chieurong), i * chieudai + (0.5 * chieudai)), 4)
            if matrix[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * chieurong + (0.5 * chieurong), i * chieudai + (0.5 * chieudai)), 10)
            if matrix[i][j] == 3:
                pygame.draw.line(screen, color, (j * chieurong + (0.5 * chieurong), i * chieudai),
                                 (j * chieurong + (0.5 * chieurong), i * chieudai + chieudai), 3)
            if matrix[i][j] == 4:
                pygame.draw.line(screen, color, (j * chieurong, i * chieudai + (0.5 * chieudai)),
                                 (j * chieurong + chieurong, i * chieudai + (0.5 * chieudai)), 3)
            if matrix[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * chieurong - (chieurong * 0.4)) - 2, (i * chieudai + (0.5 * chieudai)), chieurong, chieudai],
                                0, PI / 2, 3)
            if matrix[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * chieurong + (chieurong * 0.5)), (i * chieudai + (0.5 * chieudai)), chieurong, chieudai], PI / 2, PI, 3)
            if matrix[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * chieurong + (chieurong * 0.5)), (i * chieudai - (0.4 * chieudai)), chieurong, chieudai], PI,
                                3 * PI / 2, 3)
            if matrix[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * chieurong - (chieurong * 0.4)) - 2, (i * chieudai - (0.4 * chieudai)), chieurong, chieudai], 3 * PI / 2,
                                2 * PI, 3)
            if matrix[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * chieurong, i * chieudai + (0.5 * chieudai)),
                                 (j * chieurong + chieurong, i * chieudai + (0.5 * chieudai)), 3)


def draw_pacman():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def check_position(centerx, centery):
    turns = [False, False, False, False]
    chieudai = (HEIGHT - 50) // 32
    chieurong = (WIDTH // 30)
    trungdiem = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if matrix[centery // chieudai][(centerx - trungdiem) // chieurong] < 3:
                turns[1] = True
        if direction == 1:
            if matrix[centery // chieudai][(centerx + trungdiem) // chieurong] < 3:
                turns[0] = True
        if direction == 2:
            if matrix[(centery + trungdiem) // chieudai][centerx // chieurong] < 3:
                turns[3] = True
        if direction == 3:
            if matrix[(centery - trungdiem) // chieudai][centerx // chieurong] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % chieurong <= 18:
                if matrix[(centery + trungdiem) // chieudai][centerx // chieurong] < 3:
                    turns[3] = True
                if matrix[(centery - trungdiem) // chieudai][centerx // chieurong] < 3:
                    turns[2] = True
            if 12 <= centery % chieudai <= 18:
                if matrix[centery // chieudai][(centerx - chieurong) // chieurong] < 3:
                    turns[1] = True
                if matrix[centery // chieudai][(centerx + chieurong) // chieurong] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % chieurong <= 18:
                if matrix[(centery + chieudai) // chieudai][centerx // chieurong] < 3:
                    turns[3] = True
                if matrix[(centery - chieudai) // chieudai][centerx // chieurong] < 3:
                    turns[2] = True
            if 12 <= centery % chieudai <= 18:
                if matrix[centery // chieudai][(centerx - trungdiem) // chieurong] < 3:
                    turns[1] = True
                if matrix[centery // chieudai][(centerx + trungdiem) // chieurong] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(play_x, play_y):
    # r, l, u, d
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y


def get_targets(reddy_x, reddy_y, bluy_x, bluy_y, hong_x, hong_y, orangy_x, orangy_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not red.dead and not eaten_ghost[0]:
            reddy_target = (runaway_x, runaway_y)
        elif not red.dead and eaten_ghost[0]:
            if 340 < reddy_x < 560 and 340 < reddy_y < 500:
                reddy_target = (400, 100)
            else:
                reddy_target = (player_x, player_y)
        else:
            reddy_target = return_target
        if not blue.dead and not eaten_ghost[1]:
            bluy_target = (runaway_x, player_y)
        elif not blue.dead and eaten_ghost[1]:
            if 340 < bluy_x < 560 and 340 < bluy_y < 500:
                bluy_target = (400, 100)
            else:
                bluy_target = (player_x, player_y)
        else:
            bluy_target = return_target
        if not hong.dead:
            hong_target = (player_x, runaway_y)
        elif not hong.dead and eaten_ghost[2]:
            if 340 < hong_x < 560 and 340 < hong_y < 500:
                hong_target = (400, 100)
            else:
                hong_target = (player_x, player_y)
        else:
            hong_target = return_target
        if not orange.dead and not eaten_ghost[3]:
            orangy_target = (450, 450)
        elif not orange.dead and eaten_ghost[3]:
            if 340 < orangy_x < 560 and 340 < orangy_y < 500:
                orangy_target = (400, 100)
            else:
                orangy_target = (player_x, player_y)
        else:
            orangy_target = return_target
    else:
        if not red.dead:
            if 340 < reddy_x < 560 and 340 < reddy_y < 500:
                reddy_target = (400, 100)
            else:
                reddy_target = (player_x, player_y)
        else:
            reddy_target = return_target
        if not blue.dead:
            if 340 < bluy_x < 560 and 340 < bluy_y < 500:
                bluy_target = (400, 100)
            else:
                bluy_target = (player_x, player_y)
        else:
            bluy_target = return_target
        if not hong.dead:
            if 340 < hong_x < 560 and 340 < hong_y < 500:
                hong_target = (400, 100)
            else:
                hong_target = (player_x, player_y)
        else:
            hong_target = return_target
        if not orange.dead:
            if 340 < orangy_x < 560 and 340 < orangy_y < 500:
                orangy_target = (400, 100)
            else:
                orangy_target = (player_x, player_y)
        else:
            orangy_target = return_target
    return [reddy_target, bluy_target, hong_target, orangy_target]


run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        power_counter = 0
        powerup = False
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180 and not game_over and not game_won:
        moving = False
        startup_counter += 1
    else:
        moving = True

    screen.fill('black')
    draw_matrix()
    center_x = player_x + 23
    center_y = player_y + 24
    if powerup:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 2, 2, 2]
    if eaten_ghost[0]:
        ghost_speeds[0] = 2
    if eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3]:
        ghost_speeds[3] = 2
    if red_dead:
        ghost_speeds[0] = 4
    if blue_dead:
        ghost_speeds[1] = 4
    if hong_dead:
        ghost_speeds[2] = 4
    if orange_dead:
        ghost_speeds[3] = 4

    game_won = True
    for i in range(len(matrix)):
        if 1 in matrix[i] or 2 in matrix[i]:
            game_won = False

    player_circle = pygame.draw.circle(screen, 'black', (center_x, center_y), 20, 2)
    draw_pacman()
    red = Ghost(red_x, red_y, targets[0], ghost_speeds[0], red_img, red_direction, red_dead,
                   red_box, 0)
    blue = Ghost(blue_x, blue_y, targets[1], ghost_speeds[1], blue_img, blue_direction, blue_dead,
                 blue_box, 1)
    hong = Ghost(hong_x, hong_y, targets[2], ghost_speeds[2], hong_img, hong_direction, hong_dead,
                  hong_box, 2)
    orange = Ghost(orange_x, orange_y, targets[3], ghost_speeds[3], orange_img, orange_direction, orange_dead,
                  orange_box, 3)
    draw_score()
    targets = get_targets(red_x, red_y, blue_x, blue_y, hong_x, hong_y, orange_x, orange_y)

    turns_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not red_dead and not red.in_box:
            red_x, red_y, red_direction = red.move_red()
        else:
            red_x, red_y, red_direction = red.move_orange()
        if not hong_dead and not hong.in_box:
            hong_x, hong_y, hong_direction = hong.move_hong()
        else:
            hong_x, hong_y, hong_direction = hong.move_orange()
        if not blue_dead and not blue.in_box:
            blue_x, blue_y, blue_direction = blue.move_blue()
        else:
            blue_x, blue_y, blue_direction = blue.move_orange()
        orange_x, orange_y, orange_direction = orange.move_orange()
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)
    # add to if not powerup to check if eaten ghosts
    if not powerup:
        if (player_circle.colliderect(red.rect) and not red.dead) or \
                (player_circle.colliderect(blue.rect) and not blue.dead) or \
                (player_circle.colliderect(hong.rect) and not hong.dead) or \
                (player_circle.colliderect(orange.rect) and not orange.dead):
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                red_x = 56
                red_y = 58
                red_direction = 0
                blue_x = 440
                blue_y = 388
                blue_direction = 2
                hong_x = 440
                hong_y = 438
                hong_direction = 2
                orange_x = 440
                orange_y = 438
                orange_direction = 2
                eaten_ghost = [False, False, False, False]
                red_dead = False
                blue_dead = False
                orange_dead = False
                hong_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
    if powerup and player_circle.colliderect(red.rect) and eaten_ghost[0] and not red.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            red_x = 56
            red_y = 58
            red_direction = 0
            blue_x = 440
            blue_y = 388
            blue_direction = 2
            hong_x = 440
            hong_y = 438
            hong_direction = 2
            orange_x = 440
            orange_y = 438
            orange_direction = 2
            eaten_ghost = [False, False, False, False]
            red_dead = False
            blue_dead = False
            orange_dead = False
            hong_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(blue.rect) and eaten_ghost[1] and not blue.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            red_x = 56
            red_y = 58
            red_direction = 0
            blue_x = 440
            blue_y = 388
            blue_direction = 2
            hong_x = 440
            hong_y = 438
            hong_direction = 2
            orange_x = 440
            orange_y = 438
            orange_direction = 2
            eaten_ghost = [False, False, False, False]
            red_dead = False
            blue_dead = False
            orange_dead = False
            hong_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(hong.rect) and eaten_ghost[2] and not hong.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            red_x = 56
            red_y = 58
            red_direction = 0
            blue_x = 440
            blue_y = 388
            blue_direction = 2
            hong_x = 440
            hong_y = 438
            hong_direction = 2
            orange_x = 440
            orange_y = 438
            orange_direction = 2
            eaten_ghost = [False, False, False, False]
            red_dead = False
            blue_dead = False
            orange_dead = False
            hong_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(orange.rect) and eaten_ghost[3] and not orange.dead:
        if lives > 0:
            powerup = False
            power_counter = 0
            lives -= 1
            startup_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            direction_command = 0
            red_x = 56
            red_y = 58
            red_direction = 0
            blue_x = 440
            blue_y = 388
            blue_direction = 2
            hong_x = 440
            hong_y = 438
            hong_direction = 2
            orange_x = 440
            orange_y = 438
            orange_direction = 2
            eaten_ghost = [False, False, False, False]
            red_dead = False
            blue_dead = False
            orange_dead = False
            hong_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(red.rect) and not red.dead and not eaten_ghost[0]:
        red_dead = True
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(blue.rect) and not blue.dead and not eaten_ghost[1]:
        blue_dead = True
        eaten_ghost[1] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(hong.rect) and not hong.dead and not eaten_ghost[2]:
        hong_dead = True
        eaten_ghost[2] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(orange.rect) and not orange.dead and not eaten_ghost[3]:
        orange_dead = True
        eaten_ghost[3] = True
        score += (2 ** eaten_ghost.count(True)) * 100

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                red_x = 56
                red_y = 58
                red_direction = 0
                blue_x = 440
                blue_y = 388
                blue_direction = 2
                hong_x = 440
                hong_y = 438
                hong_direction = 2
                orange_x = 440
                orange_y = 438
                orange_direction = 2
                eaten_ghost = [False, False, False, False]
                red_dead = False
                blue_dead = False
                orange_dead = False
                hong_dead = False
                score = 0
                lives = 3
                matrix = copy.deepcopy(matrix)
                game_over = False
                game_won = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction

    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_x > 900:
        player_x = -47
    elif player_x < -50:
        player_x = 897

    if red.in_box and red_dead:
        red_dead = False
    if blue.in_box and blue_dead:
        blue_dead = False
    if hong.in_box and hong_dead:
        hong_dead = False
    if orange.in_box and orange_dead:
        orange_dead = False

    pygame.display.flip()
pygame.quit()


# sound effects, restart and winning messages
