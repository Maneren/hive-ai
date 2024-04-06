from common import big_figures, board_size, small_figures

from player import Move, Piece, PieceKind, Player, play_move


def test_with_play_move() -> None:
    p = Player("player", False, board_size, small_figures, big_figures)
    board = p._board

    assert all(p.is_empty(cell) for cell in p.cells)

    start = (2, 2)
    end = (3, 3)

    with play_move(p, Move(PieceKind.Queen, None, start)):
        assert board[start] == [Piece.from_str("q")]

        move = Move(PieceKind.Queen, start, end)

        with play_move(p, move):
            assert start not in board
            assert board[end] == [Piece.from_str("q")]

        assert board[start] == [Piece.from_str("q")]
        assert end not in board

        with play_move(p, Move(PieceKind.Beetle, None, start)):
            assert board[start] == [Piece.from_str("q"), Piece.from_str("b")]

            move = Move(PieceKind.Beetle, start, end)

            with play_move(p, move):
                assert board[start] == [Piece.from_str("q")]
                assert board[end] == [Piece.from_str("b")]

            assert board[start] == [Piece.from_str("q"), Piece.from_str("b")]
            assert end not in board

        assert board[start] == [Piece.from_str("q")]

    assert all(p.is_empty(cell) for cell in p.cells)
