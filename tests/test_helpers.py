from textwrap import dedent

from common import big_figures, board_size, small_figures

from player import Player, parse_board, Piece


def test_can_move_to() -> None:
    p = Player("player", True, board_size, small_figures, big_figures)

    p[2, 2] = [Piece.from_str("q")]
    p[3, 2] = [Piece.from_str("a")]
    p[2, 1] = [Piece.from_str("a")]

    assert not p.can_move_to((2, 2), (3, 1))

    assert p.can_move_to((2, 2), (2, 3))
    assert p.can_move_to((2, 2), (1, 2))

    p[2, 4] = [Piece.from_str("q")]
    p[3, 3] = [Piece.from_str("a")]
    p[2, 5] = [Piece.from_str("a")]

    assert not p.can_move_to((2, 4), (3, 4))

    assert p.can_move_to((2, 4), (2, 3))
    assert p.can_move_to((2, 4), (1, 5))


def test_str() -> None:
    p = Player("player", True, board_size, small_figures, big_figures)
    print(p)


def test_parse() -> None:
    p = Player("player", True, board_size, small_figures, big_figures)

    string = dedent(
        """
        . . . . . . . . . . . . .
         . . . . . . . . . . . . .
        . . . . . . . . . . . . .
         . . . . . . . . . . . . .
        . . . . . . . . . . . . .
         . . . . . . . . . . . . .
        . . . . . . . . . . . . .
         . . . . . . . . . . . . .
        . . . . . . . . . . . . .
         . . . . . . . . . . . . .
        . . . . . . . . . . . . .
         . . . . . . . . . . . . .
        . . . . . . . . . . . . .
        """,
    ).strip()

    p.board = parse_board(string)

    assert str(p) == string

    assert len(list(p.empty_cells)) == 13**2


def test_detect_cycle() -> None:
    p = Player("player", True, board_size, small_figures, big_figures)

    p.board = parse_board(
        dedent(
            """
            . . . . . . . . . . . . .
             . . . . . . . . . . . . .
            . . . . . . . . . . . . .
             . . . . . . . . . . . . .
            . . . . . . s . . . . . .
             . . . . . . g q . . . . .
            . . . . . . s .  . . . .
             . . . . . q a a b . . . .
            . . . . . . . . b . . . .
             . . . . . . . . . . . . .
            . . . . . . . . . . . . .
             . . . . . . . . . . . . .
            . . . . . . . . . . . . .
            """,
        ).strip()
    )

    assert not p.cycles

    p.set_board(
        parse_board(
            dedent(
                """
            . . . . . . . . . . . . .
             . . . . . . . . . . . . .
            . . . . . . . . . . . . .
             . . . . . A . . . . . . .
            . . . . . . b G . . . . .
             . . . . . Q . a . . . . .
            . . . . . . s G . . . . .
             . . . . . . g g . . . . .
            . . . . . . . . . . . . .
             . . . . . . . . . . . . .
            . . . . . . . . . . . . .
             . . . . . . . . . . . . .
            . . . . . . . . . . . . .
            """,
            ).strip()
        )
    )

    assert p.cycles == {(3, 5), (3, 6), (4, 4), (4, 6), (5, 4), (5, 5)}

    p.set_board(
        parse_board(
            dedent(
                """
                . . . . . . . . . . . . .
                 . . . . . . . . . . . . .
                . . . . . . . . . . . . .
                 . . . . . . . . . . . . .
                . . . . . . bB G . . . . .
                 . . . . A Q . a . . . . .
                . . . . . . s q . . . . .
                 . . . . . . g g . . . . .
                . . . . . . a . a . . . .
                 . . . . . . a a . . . . .
                . . . . . . . . . . . . .
                 . . . . . . . . . . . . .
                . . . . . . . . . . . . .
                """,
            ).strip()
        )
    )

    assert p.cycles == {
        (3, 5),
        (3, 6),
        (4, 4),
        (4, 6),
        (5, 4),
        (5, 5),
        (2, 8),
        (2, 9),
        (3, 7),
        (3, 9),
        (4, 7),
        (4, 8),
    }

    p.set_board(
        parse_board(
            dedent(
                """
                . . . . . . . . . . . . .
                 . . . . . . . . . . . . .
                . . . . . . . . . . . . .
                 . . . . . . . . . . . . .
                . . . . . . b G a a . . .
                 . . . . A Q . a . a . . .
                . . . . . . s g a a . . .
                 . . . . . . . . . . . . .
                . . . . . . . . . . . . .
                 . . . . . . . . . . . . .
                . . . . . . . . . . . . .
                 . . . . . . . . . . . . .
                . . . . . . . . . . . . .
                """,
            ).strip()
        )
    )

    assert p.cycles == {
        (4, 4),
        (5, 5),
        (5, 4),
        (4, 6),
        (3, 6),
        (3, 5),
        (7, 4),
        (6, 4),
        (5, 6),
        (6, 6),
        (7, 5),
    }


test_detect_cycle()
