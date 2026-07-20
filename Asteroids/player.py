import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
from shot import Shot
from utils import resource_path

WHITE = 255,255,255

pygame.mixer.init()
pygame.display.set_caption("ASTEROIDS")

Laser_sound = pygame.mixer.Sound(resource_path("Laser.wav"))

Laser_sound.set_volume(0.75)

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.shot_cooldown_timer = 0
        self.rotation = 0
        self.vel_x = 0.0
        self.vel_y = 0.0

        self.ACCEL = 1.2
        self.FRICTION = 0.9



    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, WHITE, Player.triangle(self), LINE_WIDTH)
    def rotate(self, dt: float):
        self.rotation += (PLAYER_TURN_SPEED * dt)
    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        accel_x = 0.0
        accel_y = 0.0
        
        self.shot_cooldown_timer -= dt
        mouse_buttons = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if(self.shot_cooldown_timer <= 0):
                        self.shoot()
                        self.shot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

    def move(self, dt: float, thrust_sign: float = 1.0):
        forward = pygame.Vector2(0,1).rotate(self.rotation) * thrust_sign
        self.vel_x += forward.x * self.ACCEL
        self.vel_y += forward.y * self.ACCEL
        self.decay(dt)
        
    def decay(self, dt: float):
        self.vel_x *= self.FRICTION
        self.vel_y *= self.FRICTION
        self.position.x += self.vel_x * dt * 60
        self.position.y += self.vel_y * dt * 60

    def shoot(self):
        Laser_sound.play()
        shot = Shot(self.position.x, self.position.y)
        second_shot = Shot(self.position.x, self.position.y)
        third_shot = Shot(self.position.x, self.position.y)
        fourth_shot = Shot(self.position.x, self.position.y)
        fifth_shot = Shot(self.position.x, self.position.y)
        sixth_shot = Shot(self.position.x, self.position.y)
        seventh_shot = Shot(self.position.x, self.position.y)

        unit_vector = pygame.Vector2(0, 1)
        second_unit_vector = pygame.Vector2(0.5, 1)
        third_unit_vector = pygame.Vector2(-0.5,1)
        fourth_unit_vector = pygame.Vector2(0.25,1)
        fifth_unit_vector = pygame.Vector2(-0.25,1)
        sixth_unit_vector = pygame.Vector2(0.125,1)
        seventh_unit_vector = pygame.Vector2(-0.125,1)

        rotated_vector = unit_vector.rotate(self.rotation)
        second_rotated_vector = second_unit_vector.rotate(self.rotation)
        third_rotated_vector = third_unit_vector.rotate(self.rotation)
        fourth_rotated_vector = fourth_unit_vector.rotate(self.rotation)
        fifth_rotated_vector = fifth_unit_vector.rotate(self.rotation)
        sixth_rotated_vector = sixth_unit_vector.rotate(self.rotation)
        seventh_rotated_vector = seventh_unit_vector.rotate(self.rotation)

        rotated_with_speed_vector = rotated_vector * PLAYER_SHOOT_SPEED
        second_rotated_with_speed_vector = second_rotated_vector * 950
        third_rotated_with_speed_vector = third_rotated_vector * 950
        fourth_rotated_with_speed_vector = fourth_rotated_vector * 850
        fifth_rotated_with_speed_vector = fifth_rotated_vector * 850
        sixth_rotated_with_speed_vector = sixth_rotated_vector * 775
        seventh_rotated_with_speed_vector = seventh_rotated_vector * 775

        shot.velocity = rotated_with_speed_vector
        second_shot.velocity = second_rotated_with_speed_vector
        third_shot.velocity = third_rotated_with_speed_vector
        fourth_shot.velocity = fourth_rotated_with_speed_vector
        fifth_shot.velocity = fifth_rotated_with_speed_vector
        sixth_shot.velocity = sixth_rotated_with_speed_vector
        seventh_shot.velocity = seventh_rotated_with_speed_vector
        
        



