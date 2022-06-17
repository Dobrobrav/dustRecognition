class Cell:
    i: int
    j: int
    color: int
    _dust_piece: 'DustPiece | None' = None

    def __init__(self, i: int, j: int, color: int):
        self.i = i
        self.j = j
        self.color = color

    def __repr__(self) -> str:
        return str(self.color)

    @property
    def dust_piece(self) -> 'DustPiece | None':
        return self._dust_piece

    @dust_piece.setter
    def dust_piece(self, dust_piece: 'DustPiece') -> None:
        self._dust_piece = dust_piece
        dust_piece.add_cell(self)