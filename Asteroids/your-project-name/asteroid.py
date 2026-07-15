import pygame
import random

from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event


class Asteroid(CircleShape):


    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
    def draw(self, screen: pygame.Surface) -> None:
        WHITE = 255,255,255

        pygame.draw.circle(screen, WHITE, self.position, self.radius, LINE_WIDTH)
    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)
    def split(self):
        self.kill()

        old_radius = self.radius

        if(self.radius <= ASTEROID_MIN_RADIUS):
            return
        
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        first_asteroid_vector = self.velocity.rotate(angle)
        second_asteroid_vector = self.velocity.rotate(-angle)
        new_radius = old_radius - ASTEROID_MIN_RADIUS

        first_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        second_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        
        first_asteroid.velocity = first_asteroid_vector * 1.2
        second_asteroid.velocity = second_asteroid_vector * 1.2