"""
Kingdomino game state and logic.
"""

from enum import Enum
import random

class Environment (Enum):
    """
    The types of Kingdomino tile environments
    """
    BASE = -1
    EMPTY = 0
    WHEAT = 1
    FOREST = 2
    OCEAN = 3
    PASTURE = 4
    SWAMP = 5
    MINE = 6


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
    def __init__(self, number, env1, crowns1, env2, crowns2):
        self.number = number
        self.cells = [Cell(env1, crowns1), Cell(env2, crowns2)]

    def __repr__(self):
        return f'{self.number} {"|".join([repr(c) for c in self.cells])}'


# All the king's domino tiles.
ALL_TILES = [
    Tile(1, Environment.WHEAT, 0, Environment.WHEAT, 0),
    Tile(2, Environment.WHEAT, 0, Environment.WHEAT, 0),
    Tile(3, Environment.FOREST, 0, Environment.FOREST, 0),
    Tile(4, Environment.FOREST, 0, Environment.FOREST, 0),
    Tile(5, Environment.FOREST, 0, Environment.FOREST, 0),
    Tile(6, Environment.FOREST, 0, Environment.FOREST, 0),
    Tile(7, Environment.OCEAN, 0, Environment.OCEAN, 0),
    Tile(8, Environment.OCEAN, 0, Environment.OCEAN, 0),
    Tile(9, Environment.OCEAN, 0, Environment.OCEAN, 0),
    Tile(10, Environment.PASTURE, 0, Environment.PASTURE, 0),
    Tile(11, Environment.PASTURE, 0, Environment.PASTURE, 0),
    Tile(12, Environment.SWAMP, 0, Environment.SWAMP, 0),
    Tile(13, Environment.WHEAT, 0, Environment.FOREST, 0),
    Tile(14, Environment.WHEAT, 0, Environment.OCEAN, 0),
    Tile(15, Environment.WHEAT, 0, Environment.PASTURE, 0),
    Tile(16, Environment.WHEAT, 0, Environment.SWAMP, 0),
    Tile(17, Environment.FOREST, 0, Environment.OCEAN, 0),
    Tile(18, Environment.FOREST, 0, Environment.PASTURE, 0),
    Tile(19, Environment.WHEAT, 1, Environment.FOREST, 0),
    Tile(20, Environment.WHEAT, 1, Environment.OCEAN, 0),
    Tile(21, Environment.WHEAT, 1, Environment.PASTURE, 0),
    Tile(22, Environment.WHEAT, 1, Environment.SWAMP, 0),
    Tile(23, Environment.WHEAT, 1, Environment.MINE, 0),
    Tile(24, Environment.FOREST, 1, Environment.WHEAT, 0),
    Tile(25, Environment.FOREST, 1, Environment.WHEAT, 0),
    Tile(26, Environment.FOREST, 1, Environment.WHEAT, 0),
    Tile(27, Environment.FOREST, 1, Environment.WHEAT, 0),
    Tile(28, Environment.FOREST, 1, Environment.OCEAN, 0),
    Tile(29, Environment.FOREST, 1, Environment.PASTURE, 0),
    Tile(30, Environment.OCEAN, 1, Environment.WHEAT, 0),
    Tile(31, Environment.OCEAN, 1, Environment.WHEAT, 0),
    Tile(32, Environment.OCEAN, 1, Environment.FOREST, 0),
    Tile(33, Environment.OCEAN, 1, Environment.FOREST, 0),
    Tile(34, Environment.OCEAN, 1, Environment.FOREST, 0),
    Tile(35, Environment.OCEAN, 1, Environment.FOREST, 0),
    Tile(36, Environment.WHEAT, 0, Environment.PASTURE, 1),
    Tile(37, Environment.OCEAN, 0, Environment.PASTURE, 1),
    Tile(38, Environment.WHEAT, 0, Environment.SWAMP, 1),
    Tile(39, Environment.PASTURE, 0, Environment.SWAMP, 1),
    Tile(40, Environment.MINE, 1, Environment.WHEAT, 0),
    Tile(41, Environment.WHEAT, 0, Environment.PASTURE, 2),
    Tile(42, Environment.OCEAN, 0, Environment.PASTURE, 2),
    Tile(43, Environment.WHEAT, 0, Environment.SWAMP, 2),
    Tile(44, Environment.PASTURE, 0, Environment.SWAMP, 2),
    Tile(45, Environment.MINE, 2, Environment.WHEAT, 0),
    Tile(46, Environment.SWAMP, 0, Environment.MINE, 2),
    Tile(47, Environment.SWAMP, 0, Environment.MINE, 2),
    Tile(48, Environment.WHEAT, 0, Environment.MINE, 3)
]


class Player (object):
    """
    Base class for all Kingdomino players.
    """

    def __init__(self):
        self.game = None  # attached game set during game init
        self.number = 0  # assigned by game, in range 1-4 according to initial random order.
        self.grid = [[Cell() for i in range(0, 10)] for j in range(0, 10)]
        self.at(0, 0).environment = Environment.BASE
        self.name = "Player"

    def __repr__(self):
        return f'{self.name} {self.number}'

    def choose_tile(self, choices):
        """
        Choose a tile out of the list of choices. The player will receive that tile on their next turn.
        Choices is a list of tiles between 1 and 4 items long, sorted in ascending order of tile number.
        Tiles already chosen by other players are removed from the list, so every choice is valid.
        Players that want to know what tiles are chosen by others during this phase can ask self.game.
        :return: the tile chosen or None if the player needs more time to choose (for human players).
        """
        # Default implementation is hapless and just chooses the lowest numbered tile available.
        return choices[0]

    def place_tile(self, tile, valid_placings):
        """
        Choose a placing for tile out of the set of valid_placings (which has at least 1 entry in it).
        Return a placing from valid_placings or None if the player needs more time to choose (for human players).
        """
        # Default implementation is hapless and just chooses an arbitrary placing
        for placing in valid_placings:
            return placing

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

    def set_cell(self, coord, cell):
        x, y = coord
        self.grid[x+5][y+5] = cell

    def set_tile(self, placement, tile):
        self.set_cell(placement[0], tile.cells[0])
        self.set_cell(placement[1], tile.cells[1])

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

    def search(self, origin=(0, 0)):
        """
        Visit all the non-empty cells in the player's game grid and yield their coordinates.
        The search pattern groups cells by their environments, meaning it will visit all
        contiguous cells of a certain type before visiting the next type and so forth.
        """
        q = [origin]
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
                    q.insert(0, c)
                else:
                    q.append(c)

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

    def enumerate_valid_placings(self, tile):
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
                if x_hi - x_lo >= 5 or y_hi - y_lo >= 5:
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

    def valid_placings(self, tile):
        """
        Return the set of valid placings for tile, or the empty set if there is nowhere the tile can fit.
        """
        placings = set()
        for placing in self.enumerate_valid_placings(tile):
            placings.add(placing)
        return placings


class Game (object):
    def __init__(self, players, seed=None):
        self.random = random.Random(seed)
        # Loggers observe the play of the game.
        self.loggers = []
        self.players = players.copy()
        # Randomly decide initial player order
        self.random.shuffle(self.players)
        # Shuffle all the tiles in the deck
        self.deck = ALL_TILES.copy()
        self.random.shuffle(self.deck)
        for i, player in enumerate(self.players):
            player.number = i + 1
            player.game = self

        # deal out the first 4 tiles
        drawn = self.deck

        # Slots hold the tiles dealt for player selection at the current moment.
        # There are 8 slots arranged as 2 groups of 4.
        # Each slot holds a 2 tuple of (tile, player), either of which can be None.
        # The first group holds tiles that were previously placed and selected as well as defines the player order.
        # The second group holds tiles that are newly dealt and are being bid upon.
        self.slots = [
            # Group 0: contains the randomly chosen player order, but no tiles yet.
            [(None, self.players[i]) for i in range(0, 4)],
            # Group 1: contains the first 4 tiles drawn.
            self._draw()
        ]


    def _draw(self):
        """
        Draws 4 tiles from the deck, sorts them in ascending order, and returns them as slots with no player yet
        assigned to each slot.
        """
        # deal the top 4 tiles in the deck
        drawn = self.deck[-4:]
        del self.deck[-4:]

        # sort them in ascending order by tile number
        drawn.sort(key=lambda tile: tile.number)

        # return slots
        return [(tile, None) for tile in drawn]


    def _deal(self):
        """
        Rotates the 4 chosen tiles from previous round into slots[0] and then draws tiles from the deck into slots[1].
        """
        # assert everyone took their tile and token back after the previous round
        assert(all((None, None) == s for s in self.slots[0]))
        self.slots[0] = self.slots[1]

        # Populate the slots with each of the sorted drawn tiles.
        # As yet, nobody has selected their tile next tile, so we put None for the player.
        self.slots[1] = self._draw()

    def step(self):
        """
        Play one step of the game.
        Return True if the game still will continue after this step, False if the game is over.
        """

        # Find the first player in slots who has yet to pick their next tile.
        # It is their turn.
        # Note that the slots in slot group 0 are ordered in increasing order,
        # so the first one we find is the next to act
        # (players who chose lower numbered tiles in the last round go first in the next).

        whose_turn = None
        whose_tile = None
        for slot in self.slots[0]:
            if slot[1]:
                (whose_tile, whose_turn) = slot
                break

        if not whose_turn:
            # Everyone has finished their turn so deal new tiles or end game.
            if not self.deck:
                # There's no tiles left in the deck so the game is over.
                return False
            else:
                # Deal the next 4 tiles.
                self._deal()
                # Consider having dealt to be one step. Nobody acts this step.
                return True

        # Check and see if the player has chosen their new tile yet.
        has_chosen = any(slot[1] is whose_turn for slot in self.slots[1])

        if not has_chosen:
            # Player still needs to place their token on their new tile
            # Narrow down their options to the tiles that have not yet been chosen
            choices = [slot[0] for slot in self.slots[1] if not slot[1]]
            choice = whose_turn.choose_tile(choices)
            if choice:
                # Player made a choice. Put their token on their tile.
                self.log(f'{whose_turn} chose {choice}')
                for i in range(0, 4):
                    if self.slots[1][i][0] == choice:
                        self.slots[1][i] = (choice, whose_turn)
                        break
                # End this step. In the next step, this same player will still be active
                # and they can place their previous tile (if any).
            else:
                # Player didn't make a choice
                # Human players don't always choose instantly, they have to think ...
                # so just leave the game state as is and we will see if they have decided next step.
                pass

        else:
            # Player has already chosen their next tile. Now they place their previous tile.
            # As a special case at the start of the game, their previous tile (whose_tile)
            # will be None and so there's nothing to do.

            # tracks whether the player took action and therefore we advance the game or not.
            did_place = False

            if whose_tile:
                # see where whose_turn wants to place whose_tile
                placements = whose_turn.valid_placings(whose_tile)
                if not placements:
                    # There are no valid placements for the tile. It must be discarded.
                    self.log(f'{whose_turn} forced to discard {whose_tile}.')
                    did_place = True
                else:
                    # There is at least 1 valid placement. Let the player choose amongst them.
                    # Note that player may return None meaning they need more time to think.
                    # In that case, we don't remove their token, and the game will resume in this
                    # same place next step.
                    placement = whose_turn.place_tile(whose_tile, placements)
                    did_place = placement is not None
                    if did_place:
                        self.log(f'{whose_turn} places {whose_tile} at {placement}')
                        whose_turn.set_tile(placement, whose_tile)
            else:
                # no previous tile, so just remove their token from the slot to advance the game
                did_place = True

            if did_place:
                for i in range(0, 4):
                    if self.slots[0][i][1] == whose_turn:
                        self.slots[0][i] = (None, None)
                        break

        return True

    def add_log_listener(self, listener):
        """
        Add a log listener, which is a function(msg)
        """
        self.loggers.append(listener)

    def remove_log_listener(self, listener):
        self.loggers.remove(listener)

    def log(self, msg):
        print(msg)
        for logger in self.loggers:
            logger(msg)


def test1():
    c1 = Cell(Environment.OCEAN, 1)
    c2 = Cell(Environment.FOREST, 0)
    t = Tile(1, (c1, c2))
    print(t)

    p = Player()
    for p in p.valid_placings(t):
        print(p)

def test2():
    game = Game([Player() for i in range(0, 4)])
    while game.step():
        pass
    for player in game.players:
        print(f'{player} scores {player.score()}')

if __name__ == '__main__':
    test2()
