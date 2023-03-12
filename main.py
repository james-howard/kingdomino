import kingdomino
import pygame
import render
import sys


def main_loop():
    """
    Main entry point for the game event loop.
    """
    pygame.init()

    pygame.display.set_caption("Kingdomino")
    pygame.display.set_allow_screensaver(True)

    dim = min(pygame.display.get_desktop_sizes()[0]) - 100

    screen = pygame.display.set_mode((dim, dim), flags=pygame.RESIZABLE, vsync=1)

    game = kingdomino.Game([kingdomino.Player() for i in range(0, 4)])

    renderer = render.Renderer()

    turn_length = 100
    last_turn_ticks = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(1)

        # clear screen
        c = pygame.color.Color(0, 0, 0)
        screen.fill(c)

        # run simulation
        now = pygame.time.get_ticks()
        if now - last_turn_ticks > turn_length:
            game.step()
            last_turn_ticks = now

        # render
        renderer.draw(screen, game)
        pygame.display.flip()

        # lock to 30fps for battery life
        pygame.time.wait(34)




if __name__ == '__main__':
    main_loop()
