import math
import pygame


def main_loop():
    """
    Main entry point for the game event loop.
    """
    pygame.init()

    pygame.display.set_caption("Kingdomino")
    pygame.display.set_allow_screensaver(True)

    dim = min(pygame.display.get_desktop_sizes()[0]) - 100

    screen = pygame.display.set_mode((dim, dim), flags=pygame.SCALED, vsync=1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        v = (math.cos(pygame.time.get_ticks() / 100.0) + 1.0) * 127.5
        c = pygame.color.Color(5, int(v), 5)
        screen.fill(c)
        pygame.display.flip()


if __name__ == '__main__':
    main_loop()
