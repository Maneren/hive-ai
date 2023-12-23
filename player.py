from __future__ import annotations

from enum import IntEnum
from typing import Iterator

from base import Board

# Player template for HIVE --- ALP semestral work
# Vojta Vonasek, 2023


# PUT ALL YOUR IMPLEMENTATION INTO THIS FILE

BoardData = dict[int, dict[int, str]]
Cell = tuple[int, int]
Move = list[str, int, int, int, int] | list[str, None, None, int, int]

DIRECTIONS = ((0, -1), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0))


def play_move(board: BoardData, move: Move) -> None:
    piece, from_p, from_q, to_p, to_q = move

    # add the piece to its new position
    board[to_p][to_q] = board[to_p][to_q] + piece

    if from_p is not None:
        # remove the piece from its old position
        assert board[from_p][from_q][-1] == piece
        board[from_p][from_q] = board[from_p][from_q][:-1]


def reverse_move(board: BoardData, move: Move) -> None:
    piece, from_p, from_q, to_p, to_q = move

    if from_p is not None:
        # add the piece back to its old position
        board[from_p][from_q] = board[from_p][from_q] + board[to_p][to_q]

    # remove the piece from its new position
    assert board[to_p][to_q][-1] == piece
    board[to_p][to_q] = board[to_p][to_q][:-1]


def cells_are_neighbors(cell1: Cell, cell2: Cell) -> bool:
    p1, q1 = cell1
    p2, q2 = cell2
    return (p1 - p2, q1 - q2) in DIRECTIONS


class Node:
    class State(IntEnum):
        RUNNING = 0
        WIN = 1
        LOSS = 2
        DRAW = 3

        def is_end(self) -> bool:
            return self > 0

    move: Move
    player_is_upper: bool
    score: int
    children: list[Node]
    depth: int
    state: Node.State

    def __init__(
        self,
        move: Move,
        player_is_upper: bool,
        initial_score: int = 0,
    ) -> None:
        self.move = move
        self.player_is_upper = player_is_upper
        self.score = initial_score
        self.children = []
        self.depth = 0
        self.state = Node.State.RUNNING

    def next_depth(self, player: Player) -> None:
        assert not self.state.is_end()

        self.depth += 1

        if self.depth == 1:
            self.initialize_children(player)
            return

        play_move(player.board, self.move)

        for child in self.children:
            child.next_depth(player)

        reverse_move(player.board, self.move)

    def initialize_children(self, player: Player) -> None:
        play_move(player.board, self.move)

        for move in player.valid_moves:
            self.children.append(Node(move, not self.player_is_upper))

        reverse_move(player.board, self.move)


class Player(Board):
    hive: set[Cell]

    def __init__(
        self,
        player_name: str,
        my_is_upper: bool,
        size: int,
        my_pieces: dict[str, int],
        rival_pieces: dict[str, int],
    ) -> None:
        """
        Do not change this method
        """
        super().__init__(my_is_upper, size, my_pieces, rival_pieces)
        self.playerName = player_name
        self.algorithmName = "maneren"
        self.hive = set(self.nonempty_cells)

    @property
    def cells(self) -> Iterator[Cell]:
        """
        Iterator over all cells
        """
        return ((p, q) for p in self.board for q in self.board[p])

    @property
    def empty_cells(self) -> Iterator[Cell]:
        """
        Iterator over all empty cells
        """
        return (tile for tile in self.cells if self.is_empty(*tile))

    @property
    def nonempty_cells(self) -> Iterator[Cell]:
        """
        Iterator over all nonempty cells
        """
        return (tile for tile in self.cells if not self.is_empty(*tile))

    @property
    def my_pieces(self) -> Iterator[tuple[str, Cell]]:
        """
        Iterator over all my pieces on the board
        """
        return (
            (self[p, q], (p, q))
            for p, q in self.nonempty_cells
            if self.is_my_cell(p, q)
        )

    @property
    def valid_moves(self) -> Iterator[Move]:
        """
        Iterator over all valid moves
        """

        raise NotImplementedError

    def cells_around_hive(self) -> Iterator[Cell]:
        """
        Iterator over all cells around the hive
        """
        if not self.hive:
            return

        start_in_hive = next(iter(self.hive))

        start_around = next(self.empty_neighbors(*start_in_hive))

        stack = [start_around]
        visited = {start_around}

        while stack:
            current = stack.pop()

            yield current

            next_neighbors = (
                neighbor
                for neighbor in self.empty_neighbors(*current)
                if neighbor not in visited and self.has_nonempty_neighbors(*neighbor)
            )

            for neighbor in next_neighbors:
                visited.add(neighbor)
                stack.append(neighbor)

    def move(self) -> Move | list[None]:
        """
        return [animal, oldP, oldQ, newP, newQ],
        or [animal, None, None, newP, newQ]
        or [] if no move is possible

        this has to stay the same for compatibility with BRUTE
        """

        self.hive = set(self.nonempty_cells)

        return []

    def neighbors(self, p: int, q: int) -> Iterator[Cell]:
        """
        Iterator over all tiles neighboring the tile (p,q)
        in the hexagonal board
        """
        return (
            (p + dp, q + dq) for dp, dq in DIRECTIONS if self.in_board(p + dp, q + dq)
        )

    def empty_neighbors(self, p: int, q: int) -> Iterator[Cell]:
        return (cell for cell in self.neighbors(p, q) if self.is_empty(*cell))

    def nonempty_neighbors(self, p: int, q: int) -> Iterator[Cell]:
        return (cell for cell in self.neighbors(p, q) if not self.is_empty(*cell))

    def is_my_cell(self, p: int, q: int) -> bool:
        cell = self[p, q]
        is_upper = self.myColorIsUpper

        return cell.isupper() == is_upper or cell.islower() != is_upper

    def is_empty(self, p: int, q: int) -> bool:
        return self.board[p][q] == ""

    def in_board(self, p: int, q: int) -> bool:
        """
        Check if (p,q) is a valid coordinate within the board
        """
        return 0 <= q < self.size and -q // 2 <= p <= self.size - q // 2

    def __getitem__(self, cell: Cell) -> str:
        p, q = cell
        return self.board[p][q]

    def __setitem__(self, cell: Cell, value: str) -> None:
        p, q = cell
        self.board[p][q] = value

    def is_valid_move(self, piece: str, x: int, y: int) -> bool:
        return self.board[x][y][-1] == piece

    def is_valid_initial_placement(self, p: int, q: int) -> bool:
        """
        Check if (p,q) is a valid initial placement. Returns True if the board is empty
        """
        if self.myMove == 0 and not self.hive:
            return True

        return all(self.is_my_cell(*cell) for cell in self.nonempty_neighbors(p, q))


def update_players(move: Move, active_player: Player, passive_player: Player) -> None:
    """write move made by activePlayer player
    this method assumes that all moves are correct, no checking is made
    """
    if not move:
        return

    animal, p, q, newp, newq = move
    if p is None and q is None:
        # placing new animal
        active_player.myPieces[animal] -= 1
        passive_player.rivalPieces = active_player.myPieces.copy()
    else:
        # just moving animal
        # delete its old position
        active_player.board[p][q] = active_player.board[p][q][:-1]
        passive_player.board[p][q] = passive_player.board[p][q][:-1]

    active_player.board[newp][newq] += animal
    passive_player.board[newp][newq] += animal


def main() -> None:
    board_size = 13
    small_figures = {
        "q": 1,
        "a": 2,
        "b": 2,
        "s": 2,
        "g": 2,
    }  # key is animal, value is how many is available for placing
    big_figures = {
        figure.upper(): val for figure, val in small_figures.items()
    }  # same, but with upper case

    p1 = Player("player1", True, board_size, small_figures, big_figures)
    p2 = Player("player2", True, board_size, big_figures, small_figures)

    filename = "output/begin.png"
    p1.saveImage(filename)

    move_idx = 0
    while True:
        move = p1.move()
        print("P1 returned", move)
        update_players(move, p1, p2)  # update P1 and P2 according to the move
        p1.saveImage("output/move-{move_idx:03d}-player1.png")

        move = p2.move()
        print("P2 returned", move)
        update_players(move, p2, p1)  # update P2 and P1 according to the move
        p1.saveImage("output/move-{move_idx:03d}-player2.png")

        move_idx += 1
        p1.myMove = move_idx
        p2.myMove = move_idx

        if move_idx > 50:
            print("End of the test game")
            break


if __name__ == "__main__":
    main()
