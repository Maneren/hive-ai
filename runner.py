from time import perf_counter
from typing import Any

from player import Player, parse_board, play_move


def update_players(
    move: Any,
    active_player: Player,
    passive_player: Player,
) -> None:
    """Write move made by `active_player` player."""
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


def test_game() -> None:
    from time import perf_counter

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

    p1 = Player("player1", False, board_size, small_figures, big_figures)
    p2 = Player("player2", True, board_size, big_figures, small_figures)

    p1.tournament = True
    p2.tournament = True

    filename = "output/begin.png"
    p1.saveImage(filename)

    move_idx = 0
    while move_idx < 20:
        start = perf_counter()
        move1 = p1.move()
        elapsed = perf_counter() - start
        if elapsed > 1:
            print(p1)
            raise Exception("P1 took too long to respond")
        print("P1 returned", move1, "in", elapsed, "seconds")
        update_players(move1, p1, p2)  # update P1 and P2 according to the move
        # p1.saveImage(f"output/move-{move_idx:03d}-player1.png")

        start = perf_counter()
        move2 = p2.move()
        elapsed = perf_counter() - start
        if elapsed > 1:
            print(p2)
            raise Exception("P2 took too long to respond")
        print("P2 returned", move2, "in", elapsed, "seconds")
        update_players(move2, p2, p1)  # update P2 and P1 according to the move
        # p1.saveImage(f"output/move-{move_idx:03d}-player2.png")

        if not move1 and not move2:
            print(f"End of the test game after {move_idx} moves")
            break

        move_idx += 1
        p1.myMove = move_idx
        p2.myMove = move_idx

    print("End of the test game")


def test_position() -> None:
    board_size = 13
    small_figures = {
        "q": 0,
        "a": 0,
        "b": 0,
        "s": 0,
        "g": 2,
    }
    big_figures = {
        "Q": 0,
        "A": 0,
        "B": 1,
        "S": 1,
        "G": 1,
    }

    p = Player("player", False, board_size, small_figures, big_figures)

    from textwrap import dedent

    p.set_board(
        parse_board(
            dedent(
                """
                . . . . . . . . . . . . .
                 . . . . . . . . . . . . .
                . . . . . . . . . . . . .
                 . . . . . . . . . . . . .
                . . . . . . . . . . . . .
                 . . . . . . . . . . . . .
                . . . . a . s a . . . . .
                 . . . . Q S . q . . . . .
                . . . . . . . A A . . . .
                 . . . . . B G . . . . . .
                . . . . . . . s . . . . .
                 . . . . . . . . . . . . .
                . . . . . . . . . . . . .
                """,
            ).strip(),
        )
    )

    p.myMove = 6
    p.tournament = True

    # self.board = {-6: {12: ''}, -5: {10: '', 11: '', 12: ''}, -4: {8: '', 9: '', 10: '', 11: '', 12: ''}, -3: {6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: ''}, -2: {4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: ''}, -1: {2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: ''}, 0: {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: ''}, 1: {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: 'B', 9: '', 10: '', 11: '', 12: ''}, 2: {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: 'G', 7: 'S', 8: '', 9: '', 10: '', 11: '', 12: ''}, 3: {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: 'q', 7: '', 8: 'A', 9: 'Q', 10: '', 11: '', 12: ''}, 4: {0: '', 1: '', 2: '', 3: '', 4: 'sB', 5: 'G', 6: '', 7: 'A', 8: '', 9: '', 10: '', 11: '', 12: ''}, 5: {0: '', 1: '', 2: '', 3: 'g', 4: 'g', 5: 'a', 6: 'a', 7: '', 8: '', 9: '', 10: '', 11: '', 12: ''}, 6: {0: '', 1: '', 2: 'b', 3: 's', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: ''}, 7: {0: '', 1: 'b', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: ''}, 8: {0: 'S', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: ''}, 9: {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: ''}, 10: {0: '', 1: '', 2: '', 3: '', 4: '', 5: ''}, 11: {0: '', 1: '', 2: '', 3: ''}, 12: {0: '', 1: ''}}
    # self.myMove = 44
    # self.myPieces = {'Q': 0, 'A': 0, 'B': 0, 'S': 0, 'G': 0}
    # self.rivalPieces = {'q': 0, 'a': 0, 'b': 0, 's': 0, 'g': 0}
    # self.myColorIsUpper = True
    # self.tournament = Trueself.board = {-6: {12: ''}, -5: {10: '', 11: '', 12: ''}, -4: {8: '', 9: '', 10: '', 11: '', 12: ''}, -3: {6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: ''}, -2: {4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: ''}, -1: {2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: ''}, 0: {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: ''}, 1: {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: 'B', 9: '', 10: '', 11: '', 12: ''}, 2: {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: 'G', 7: 'S', 8: '', 9: '', 10: '', 11: '', 12: ''}, 3: {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: 'q', 7: '', 8: 'A', 9: 'Q', 10: '', 11: '', 12: ''}, 4: {0: '', 1: '', 2: '', 3: '', 4: 'sB', 5: 'G', 6: '', 7: 'A', 8: '', 9: '', 10: '', 11: '', 12: ''}, 5: {0: '', 1: '', 2: '', 3: 'g', 4: 'g', 5: 'a', 6: 'a', 7: '', 8: '', 9: '', 10: '', 11: '', 12: ''}, 6: {0: '', 1: '', 2: 'b', 3: 's', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: ''}, 7: {0: '', 1: 'b', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: ''}, 8: {0: 'S', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: ''}, 9: {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: ''}, 10: {0: '', 1: '', 2: '', 3: '', 4: '', 5: ''}, 11: {0: '', 1: '', 2: '', 3: ''}, 12: {0: '', 1: ''}}
    # self.myMove = 44
    # self.myPieces = {'Q': 0, 'A': 0, 'B': 0, 'S': 0, 'G': 0}
    # self.rivalPieces = {'q': 0, 'a': 0, 'b': 0, 's': 0, 'g': 0}
    # self.myColorIsUpper = True
    # self.tournament = True

    filename = "output/begin.png"
    p.saveImage(filename)

    for i, move in enumerate(list(p.valid_moves)):
        print(move)
        # with play_move(p, move):
        #     filename = f"output/move-{i:03d}.png"
        #     p.saveImage(filename)

    print("End of found moves")

    # start = perf_counter()
    # move_brute = p.move()
    # print("P returned", move_brute, "in", perf_counter() - start)

    # print("//////////")

    # from michal import Player as MPlayer
    #
    # mp = MPlayer("michal", False, board_size, small_figures, big_figures)
    # mp.board = p.board
    #
    # for move in mp.allMyMoves(5):
    #     mm = move.moves
    #     for m in mm:
    #         print(Move(move.name, (move.p, move.q) if move.p is not None else None, m))

    start = perf_counter()
    for _ in range(1000):
        list(p.valid_moves)
    print("Moves found in", perf_counter() - start)


if __name__ == "__main__":
    test_game()
    # test_position()
