from dust_piece import *
from tools import Picture, DustSize, Quantity


class DustField:
    _dust_pieces: list[DustPiece]
    _field: list[list[Cell]]

    def __init__(self, field: Picture):
        field = list([list(row) for row in field])
        self._dust_pieces = []
        for i, row in enumerate(field):
            for j, color in enumerate(row):
                row[j] = Cell(i, j, color)
        self.field = field

    def distribute_dust_by_size(self) -> dict[DustSize, Quantity]:
        """ Distribute dust pieces in the field by size. """
        self._recognize_dust_pieces()
        return self._get_distribution_data()

    def _recognize_dust_pieces(self) -> None:
        """ Searches for dust (<255) cells which haven't found their dust_piece yet. """
        for row in self._field:
            for cell in row:
                if cell.color == 255 or cell.dust_piece:
                    continue
                self._depth_of_recursion = 1
                self._recognize_dust_piece(cell)

    def _recognize_dust_piece(self, cell: Cell, dust_piece: DustPiece = None) -> None:
        """ Recognize the entire dust piece which contains the cell. """
        cell.dust_piece = dust_piece or DustPiece(self)
        neighbors = self._get_neighboring_dust_cells(cell)
        for neighbor in neighbors:
            self._depth_of_recursion += 1
            if self._depth_of_recursion < 993:
                self._recognize_dust_piece(neighbor, dust_piece=cell.dust_piece)

    def _get_neighboring_dust_cells(self, cell) -> list[Cell]:
        """ Return only neighbours which haven't found their dust piece yet. """
        # Need to look for those on the right and from below
        i, j = cell.i, cell.j
        if j == len(self.field[0]) - 1 or i == len(self.field) - 1:
            return []

        candidate_cells = (
            self._field[i][j + 1],
            self._field[i + 1][j + 1],
            self._field[i + 1][j],
            self._field[i + 1][j - 1],
            self._field[i][j - 1],
            self._field[i - 1][j - 1],
            self._field[i - 1][j],
        )
        return_list = [
            cell for cell in candidate_cells
            if cell.dust_piece is None and cell.color != 255
        ]
        return return_list

    def add_dust_piece(self, dust_piece: DustPiece) -> None:
        self._dust_pieces.append(dust_piece)

    def _get_distribution_data(self) -> dict[DustSize, Quantity]:
        distribution = {}
        for dust_piece in self._dust_pieces:
            current_size = len(dust_piece.cells)
            distribution[current_size] = distribution.setdefault(current_size, 0) + 1
        return distribution

    @property
    def field(self) -> list[list[Cell]]:
        return self._field

    @field.setter
    def field(self, field: list[list[Cell]]) -> None:
        """ Create wrapper for field. """
        self._field = (
            [row + [Cell(i, len(field[0]), 255)] for i, row in enumerate(field)]
            + [[Cell(len(field) - 1, len(field[0]), 255)] * (len(field[0]) + 1)]
        )
