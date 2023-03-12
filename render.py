"""
Board and game state rendering
"""

import pygame
import pygame.draw
import kingdomino

# all of the values below are in the native coordinate system of the renderer.
# a matrix transforms them to window coordinates.

CELL_SIZE = 32
SPACING = CELL_SIZE

# max width / height of a single player's board
BOARD_MAX_TILES = 9

# size of each player's board (grid) for placing tiles
BOARD_SIZE = CELL_SIZE * BOARD_MAX_TILES

# how wide our game scene is. 4 boards, each 10 cells wide, plus spacing
SCENE_WIDTH = BOARD_SIZE * 4 + \
              SPACING * 5

# how tall our game scene is. 1 board high, plus 4 tiles with spacing for the dealt tiles.
SCENE_HEIGHT = SPACING + \
               CELL_SIZE * 4 + SPACING * 3 + \
               SPACING + \
               BOARD_SIZE + \
               SPACING

# If true, draw a second view of each board from the tile placement history.
DRAW_TILE_HISTORY = False

if DRAW_TILE_HISTORY:
    SCENE_HEIGHT += \
        BOARD_SIZE + \
        SPACING

class Renderer (object):
    def __init__(self):
        # self.crown = pygame.image.load("resources/crown.png")
        self.ticks = pygame.time.get_ticks()
        self.dt = 16
        res = (SCENE_WIDTH, SCENE_HEIGHT)
        self.surface = pygame.Surface((SCENE_WIDTH, SCENE_HEIGHT))
        self.scratch = pygame.Surface((1, 1))

        print(f'Internal game board resolution {res}')

    def update_time(self):
        """
        Updates elapsed time and frame time for animations.
        """
        now = pygame.time.get_ticks()
        self.dt = now - self.ticks
        self.ticks = now

    def blit(self, screen: pygame.Surface):
        """
        Blit internal game surface to the screen.
        """
        (screen_w, screen_h) = screen.get_size()
        # figure out whether to letterbox or pillarbox the game based on the relative aspect ratios of screen and game.
        screen_aspect = float(screen_w) / float(screen_h)
        game_aspect = float(SCENE_WIDTH) / float(SCENE_HEIGHT)
        if screen_aspect > game_aspect:
            # screen is wider than game, will pillarbox
            height = float(screen_h)
            width = SCENE_WIDTH * (height / SCENE_HEIGHT)
        else:
            # screen is narrower than game, will letterbox
            width = float(screen_w)
            height = SCENE_HEIGHT * (width / SCENE_WIDTH)

        x = round((screen_w - width) / 2.0)
        y = round((screen_h - height) / 2.0)

        width = round(width)
        height = round(height)

        if self.scratch is None or self.scratch.get_size()[0] != width or self.scratch.get_size()[1] != height:
            # reallocate scaling buffer because window size changed
            self.scratch = pygame.Surface((width, height))

        # scale game buffer to scratch buffer
        # smoothscale will do a bilinear filter, scale is nearest.
        # i kinda think nearest looks best for the blocky aesthetic
        #pygame.transform.smoothscale(self.surface, (width, height), dest_surface=self.scratch)
        pygame.transform.scale(self.surface, (width, height), dest_surface=self.scratch)

        # blit scratch buffer to the screen
        screen.blit(self.scratch, (x, y))

    def clear(self):
        """
        Clear internal game surface
        """
        clear_color = pygame.color.Color(60, 127, 60)
        self.surface.fill(clear_color)

    def draw_cell(self, cell, x, y):
        from kingdomino import Environment
        colors = {
            Environment.EMPTY: (16, 16, 16),
            Environment.WHEAT: (240, 240, 10),
            Environment.OCEAN: (32, 48, 255),
            Environment.FOREST: (0, 143, 0),
            Environment.BASE: (127, 127, 127),
            Environment.SWAMP: (146, 144, 0),
            Environment.MINE: (255, 212, 121),
            Environment.PASTURE: (115, 250, 121)
        }
        c = colors[cell.environment]
        r = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        self.surface.fill(c, r)
        # c = (32, 32, 32)
        # pygame.draw.rect(self.surface, c, r, width=1)


    def draw_board(self, player: kingdomino.Player):
        i = (player.number - 1)
        ox = SPACING + (SPACING * i) + BOARD_SIZE * i
        oy = SPACING * 5 + CELL_SIZE * 4
        for y in range(0, BOARD_MAX_TILES):
            for x in range(0, BOARD_MAX_TILES):
                cell = player.at((x-4, y-4))
                self.draw_cell(cell, ox + (x * CELL_SIZE), oy + (y * CELL_SIZE))
        if DRAW_TILE_HISTORY:
            self.draw_history(player)

    def draw_history(self, player: kingdomino.Player):
        i = (player.number - 1)
        ox = SPACING + (SPACING * i) + BOARD_SIZE * i
        oy = SPACING * 6 + CELL_SIZE * 4 + BOARD_SIZE
        r = pygame.Rect(ox, oy, BOARD_SIZE, BOARD_SIZE)
        self.surface.fill((0, 0, 0), r)

        for tile, placing in player.placement_history:
            x0 = (placing[0][0] + 4) * CELL_SIZE
            y0 = (placing[0][1] + 4) * CELL_SIZE
            self.draw_cell(tile.cells[0], ox + x0, oy + y0)
            x1 = (placing[1][0] + 4) * CELL_SIZE
            y1 = (placing[1][1] + 4) * CELL_SIZE
            self.draw_cell(tile.cells[1], ox + x1, oy + y1)
            x_min = min(x0, x1)
            y_min = min(y0, y1)
            x_max = max(x0, x1) + CELL_SIZE
            y_max = max(y0, y1) + CELL_SIZE
            assert((x_max - x_min) * (y_max - y_min) == CELL_SIZE * CELL_SIZE * 2)
            r = pygame.Rect(ox + x_min, oy + y_min, x_max - x_min, y_max - y_min)
            pygame.draw.rect(self.surface, (255, 255, 255), r, width=2)


    def draw(self, screen: pygame.Surface, game: kingdomino.Game):
        self.update_time()
        self.clear()
        for player in game.players:
            self.draw_board(player)
        self.blit(screen)





