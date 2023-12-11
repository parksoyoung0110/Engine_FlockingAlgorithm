import pygame
from sys import exit
from random import randint, uniform, choice

WIDTH = 800
HEIGHT = 600
fps = 30

black = (0, 0, 0)
white = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flocking Algorithm")
clock = pygame.time.Clock()

MAX_SPEED = 3
BOID_SIZE = 6

FLEE_RADIUS = 43
MAX_FLEE_FORCE = 22

ALIGN_RADIUS = 120

COHESION_RADIUS = 400

vec = pygame.math.Vector2

class Boid(pygame.sprite.Sprite):
    def __init__(self, species_color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BOID_SIZE, BOID_SIZE))
        self.image.fill(species_color)
        self.rect = self.image.get_rect()
        self.pos = vec(randint(0, WIDTH), randint(0, HEIGHT))
        self.vel = vec(choice([-MAX_SPEED, MAX_SPEED]), choice([-MAX_SPEED, MAX_SPEED])).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.species_color = species_color

    def update(self):
        self.acc = vec(0, 0)
        for i in boids:
            if i != self and i.species_color == self.species_color:
                self.acc += self.separation(i.rect.center)
        self.acc += self.alignment()
        self.acc += self.cohesion()

        self.vel += (self.acc * DELTA_TIME)

        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.pos += self.vel

        # Screen boundaries check and adjustment
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
            self.vel.x *= -1
        elif self.pos.x < 0:
            self.pos.x = 0
            self.vel.x *= -1
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT
            self.vel.y *= -1
        elif self.pos.y < 0:
            self.pos.y = 0
            self.vel.y *= -1

        self.rect.center = self.pos

    def separation(self, target):
        steer = vec(0, 0)
        dist = self.pos - target
        desired = vec(0, 0)
        
        if dist.x != 0 and dist.y != 0:
            if dist.length() < FLEE_RADIUS:
                desired = dist.normalize() * MAX_SPEED
            else:
                desired = self.vel.normalize() * MAX_SPEED
        steer = desired - self.vel
        if steer.length() > MAX_FLEE_FORCE:
            steer.scale_to_length(MAX_FLEE_FORCE)
        return steer

    def alignment(self):
        align = vec(0, 0)
        desired = vec(0, 0)
        for i in boids:
            if i != self and i.species_color == self.species_color:
                if i.vel.x != 0 and i.vel.y != 0:
                    if (self.pos - i.pos).length() < ALIGN_RADIUS:
                        desired += i.vel.normalize() * MAX_SPEED

        align = desired - self.vel
        if len([b for b in boids if b.species_color == self.species_color]) > 0:
            align /= len([b for b in boids if b.species_color == self.species_color])
            
        if align.length() > MAX_SPEED:
            align.scale_to_length(MAX_SPEED)

        return align

    def cohesion(self):
        cohes = vec(0, 0)
        average_location = vec(0, 0)
        for i in boids:
            if i != self and i.species_color == self.species_color:
                dist = self.pos - i.pos
                if dist.length() < COHESION_RADIUS:
                    average_location += i.pos

        if len([b for b in boids if b.species_color == self.species_color]) > 1:
            average_location /= (len([b for b in boids if b.species_color == self.species_color]) - 1)

        cohes = average_location - self.pos
        if cohes.length() > MAX_SPEED:
            cohes.scale_to_length(MAX_SPEED)
        return cohes

def create_boids(number):
    global all_sprite, boids
    all_sprite = pygame.sprite.Group()
    species_colors = [(255, 255, 56), (255, 10, 10), (0, 255, 0)]  # Add more colors as needed
    boids = [Boid(choice(species_colors)) for _ in range(number)]
    all_sprite.add(boids)

create_boids(60)

DELTA_TIME = 0

run = True
last_click = pygame.time.get_ticks()
while run:
    DELTA_TIME = clock.tick(fps) / 1000


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    all_sprite.update()

    screen.fill(black)
    all_sprite.draw(screen)

    pygame.display.flip()

pygame.quit()
exit()
