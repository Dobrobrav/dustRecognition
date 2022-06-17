from cell import *


class DustPiece:
    current_pk = 0
    cells: set[Cell]
    _dust_field: 'DustField'

    def __init__(self, dust_field: 'DustField'):
        self.__class__.current_pk += 1
        self.pk = self.__class__.current_pk
        self.cells = set()
        self._dust_field = dust_field
        dust_field.add_dust_piece(self)

    def add_cell(self, cell: Cell) -> None:
        self.cells.add(cell)
