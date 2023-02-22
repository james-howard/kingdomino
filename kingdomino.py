"""
Kingdomino game state and logic.
"""

from enum import Enum

class Environment (Enum):
    """
    The types of Kingdomino tile environments
    """
    EMPTY = 0
    OCEAN = 1
    FOREST = 2
    PASTURE = 3
    SWAMP = 4
    OIL = 5
    BASE = 100


class Cell (object):
    """
    Represents a single cell in a tile or game grid
    """
    def __init__(self, environment=Environment.EMPTY, crowns=0):
        self.environment = environment
        self.crowns = crowns

    def __repr__(self):
        return f'{self.environment.name}{"👑"*self.crowns}'


class Tile (object):
    """
    A Kingdomino tile has two cells, each with its own environment, as well as a number of crowns per cell.
    On the back is the tile number.
    """
    def __init__(self, number, cells):
        self.number = number
        self.cells = cells

    def __repr__(self):
        return f'{self.number} {"|".join([repr(c) for c in self.cells])}'


class Player (object):
    """
    Base class for all Kingdomino players.
    """

    def __init__(self):
        self.game = None  # attached game set during game init
        self.grid = [[Cell() for i in range(0, 10)] for j in range(0, 10)]
        self.at(0, 0).environment = Environment.BASE

    def at(self, x, y=None) -> Cell:
        """
        The player's game grid is a cartesian plane with the base at the origin of 0,0.
        The bottom leftmost possible cell is at -4,-4
        The upper rightmost possible cell is at 4,4
        """

        # unpack coord tuple if necessary
        if y is None:
            x, y = x

        # Assert that x and y are in range of the grid
        assert(x > -5)
        assert(x < 5)
        assert(y > -5)
        assert(y < 5)

        return self.grid[x+5][y+5]

    @staticmethod
    def adj(coord):
        """
        Yield immediately adjacent (up,down,left,right)
        coords on game grid to coord
        """
        # lower
        if coord[1] > -4:
            yield coord[0], coord[1] - 1
        # left
        if coord[0] > -4:
            yield coord[0] - 1, coord[1]
        # right
        if coord[0] < 4:
            yield coord[0] + 1, coord[1]
        # upper
        if coord[1] < 4:
            yield coord[0], coord[1] + 1

    def search(self):
        """
        Visit all the non-empty cells in the player's game grid and yield their coordinates.
        The search pattern groups cells by their environments, meaning it will visit all
        contiguous cells of a certain type before visiting the next type and so forth.
        """
        q = [(0, 0)]
        hist = set(q[0])

        while q:
            loc = q.pop(0)
            yield loc
            for c in self.adj(loc):
                if c in hist or self.at(c).environment == Environment.EMPTY:
                    continue  # ignore already visited or empty cells
                hist.add(c)
                i = 0
                if self.at(c).environment == self.at(loc).environment:
                    loc.insert(0, c)
                else:
                    loc.append(c)

    def score(self):
        """
        :return: the current score of the player's game grid
        """
        env = Environment.EMPTY
        crowns = 0
        contiguous = 0
        score = 0
        for loc in self.search():
            c = self.at(loc)
            if c.environment != env:
                score += crowns * contiguous
                crowns = 0
                contiguous = 0
                env = c.environment
            crowns += c.crowns
            contiguous += 1
        score += crowns * contiguous
        return score

    @staticmethod
    def tile_adj(loc):
        """
        Yield all possible placings of a tile adjacent to loc as tuples of grid coordinates
        This is a static method therefore it does not consider the player's grid state, but just
        yields the places where the tile could be on an empty grid.
        """
        x, y = loc

        for dy in (-1, 1):
            # vertical
            yield (x, y+dy), (x, y+2*dy)
            # vertical, flip
            yield (x, y+2*dy), (x, y+dy)
            # left
            yield (x-1, y+dy), (x, y+dy)
            # left, flip
            yield (x, y+dy), (x-1, y+dy)
            # right
            yield (x, y+dy), (x+1, y+dy)
            # right, flip
            yield (x+1, y+dy), (x, y+dy)

        for dx in (-1, 1):
            # horizontal
            yield (x+dx, y), (x+2*dx, y)
            # horizontal, flip
            yield (x+2*dx, y), (x+dx, y)
            # up
            yield (x+dx, y), (x+dx, y+1)
            # up, flip
            yield (x+dx, y+1), (x+dx, y)
            # down
            yield (x+dx, y), (x+dx, y-1)
            # down, flip
            yield (x+dx, y-1), (x+dx, y)

    def valid_placings(self, tile):
        """
        Yield the set of valid placings for the given tile.
        A placing is represented as a tuple of grid coordinates.
        For example a tile placed longitudinally directly to the right
        of the base (origin) cell would yield ((1, 0), (2, 0)) as well
        as a second yield for its flipped orientation ((2, 0), (1, 0))
        """

        # Find the min and max x and y of any non-empty tiles
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        for y in range(-4, 5):
            for x in range(-4, 5):
                if self.at(x, y).environment != Environment.EMPTY:
                    min_x = min(x, min_x)
                    max_x = max(x, max_x)
                    min_y = min(y, min_y)
                    max_y = max(y, max_y)

        hist = set()

        for loc in self.search():
            for placing in self.tile_adj(loc):
                # ignore any placing we've already considered
                if placing in hist:
                    continue
                hist.add(placing)
                # ignore any placing that breaks the 5x5 rule
                x_lo = min(min_x, placing[0][0], placing[1][0])
                x_hi = max(max_x, placing[0][0], placing[1][0])
                y_lo = min(min_y, placing[0][1], placing[1][1])
                y_hi = max(max_y, placing[0][1], placing[1][1])
                if x_hi - x_lo > 5 or y_hi - y_lo > 5:
                    continue
                # ignore any placing that collides with an existing cell
                if any(c for c in placing if self.at(c).environment != Environment.EMPTY):
                    continue
                # ignore any placing that doesn't have at least one environmentally matching adjacent cell
                has_match = False
                for i, c in enumerate(placing):
                    for adj in self.adj(c):
                        adj_env = self.at(adj).environment
                        if adj_env == Environment.BASE or adj_env == tile.cells[i].environment:
                            has_match = True
                            break
                if has_match:
                    yield placing

if __name__ == '__main__':
    c1 = Cell(Environment.OCEAN, 1)
    c2 = Cell(Environment.FOREST, 0)
    t = Tile(1, (c1, c2))
    print(t)

    p = Player()
    for p in p.valid_placings(t):
        print(p)