import pygame
import sys

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED
from player import Player
from asteroid import Asteroid
from logger import log_state
from asteroidfield import AsteroidField
from logger import log_event
from circleshape import CircleShape
from shot import Shot
from utils import resource_path

BLACK = (0,0,0)


def main():
    pygame.init()
    print("Starting Asteroids")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.display.set_caption("Score")
    my_font = pygame.font.SysFont("Arial", 50)
    pygame.mixer.init()
    pygame.display.set_caption("ASTEROIDS")

    Explosion_sound = pygame.mixer.Sound(resource_path("Explosion.wav"))


    Explosion_sound.set_volume(0.5)


    clock = pygame.time.Clock()
    dt = 0.0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    asteroids = pygame.sprite.Group()

    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)

    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

    asteroid_field = AsteroidField()

    amount_of_asteroids_killed = 0
    health_of_player = 5

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        
        
        screen.fill(BLACK, rect=None, special_flags=0)

        dt = clock.tick(60) / 1000

        player.draw(screen)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(dt, 1.0)
        elif keys[pygame.K_s]:
            player.move(dt, -1.0)
        else:
            player.decay(dt)


        for drawables in drawable:
           drawables.draw(screen)
        updatable.update(dt)
        for asteroid in asteroids:
            if(CircleShape.collides_with(player, asteroid)):
                log_event("player_hit")
                health_of_player -= 1
                if health_of_player <= 0:
                    print("Game Over!")
                    sys.exit()

            for shot in shots:
                if(CircleShape.collides_with(shot, asteroid)):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
                    Explosion_sound.play()
                    amount_of_asteroids_killed += 1

            text_surface = my_font.render(f"ASTEROIDS KILLED: {amount_of_asteroids_killed}", True, (255,255,255))
            screen.blit(text_surface, (100, 100))

        pygame.display.flip()




if __name__ == "__main__":
    main()
