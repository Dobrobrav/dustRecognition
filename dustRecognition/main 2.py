# from PIL import Image
from numpy import ndarray
from skimage import io, img_as_float
import cv2 as cv
from typing import TypeAlias


Picture: TypeAlias = ndarray
DustSize: TypeAlias = int
Quantity: TypeAlias = int


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


class DustField:
    dust_pieces: list[DustPiece]
    _field: list[list[Cell]]

    def __init__(self, field: Picture):
        field = list([list(row) for row in field])
        self.dust_pieces = []
        for i, row in enumerate(field):
            for j, color in enumerate(row):
                row[j] = Cell(i, j, color)
        self.field = field

    def distribute_dust_by_size(self) -> dict[DustSize, Quantity]:
        self._find_dust_pieces_for_cells()
        distribution = {}
        for dust_piece in self.dust_pieces:
            current_size = len(dust_piece.cells)
            distribution[current_size] = distribution.setdefault(current_size, 0) + 1
        return distribution

    def _find_dust_pieces_for_cells(self) -> None:
        """ Searches for white (255) cells which haven't found their dust_piece yet"""
        for row in self._field:
            for cell in row:
                if cell.color == 255 or cell.dust_piece:
                    continue
                self._recognize_dust_piece(cell)

    def _recognize_dust_piece(self, cell: Cell, dust_piece: DustPiece = None) -> None:
        """ Recognize the entire dust piece which contains the cell """
        cell.dust_piece = dust_piece or DustPiece(self)
        neighbors = self._get_neighbors(cell)
        # print(cell.i, cell.j, len(neighbors))
        for neighbor in neighbors:
            self._recognize_dust_piece(neighbor, dust_piece=cell.dust_piece)

    def _get_neighbors(self, cell) -> list[Cell]:
        """ Return only neighbours which haven't found their dust piece yet """
        # Need to look for those on the right and from below
        i, j = cell.i, cell.j
        if j == len(self.field[0]) - 1 or i == len(self.field) - 1:
            return []
        candidate_cells = (
            self._field[i][j + 1],
            self._field[i + 1][j + 1],
            self._field[i + 1][j],
            self._field[i + 1][j - 1],
        )
        return list(filter(lambda cell: cell.dust_piece is None and cell.color != 255, candidate_cells))
        # return [cell for cell in candidate_cells if cell.dust_piece is None]

    def add_dust_piece(self, dust_piece: DustPiece) -> None:
        self.dust_pieces.append(dust_piece)

    @property
    def field(self) -> list[list[Cell]]:
        return self._field

    @field.setter
    def field(self, field: list[list[Cell]]) -> None:
        self._field = (
            [row + [Cell(i, len(field[0]), 255)] for i, row in enumerate(field)]
            + [[Cell(len(field) - 1, len(field[0]), 255)] * (len(field[0]) + 1)]
        )


def read_img(file_name: str) -> Picture:
    return io.imread(file_name)


def get_grayscale(img: Picture) -> Picture:
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


def get_blurred(img: Picture, a: int = 50, b: int = 8,
                c: int = 50, blur: bool = True) -> Picture:
    return cv.bilateralFilter(img, a, b, c) if blur else img


def get_filtered(img: Picture, bound: int = 180, filter: bool = True) -> Picture:
    if not filter:
        return img

    copy_img = img.copy()

    for row in copy_img:
        for j, pixel_value in enumerate(row):
            if pixel_value > bound:
                row[j] = 255

    return copy_img


def save_to_file(img: Picture, name: str = "result_50_8_50.png") -> None:
    cv.imwrite(name, img)


def show(img: Picture, name: str = "some_img") -> None:
    cv.imshow(name, img)


def main():
    BOUND = 160
    B = 10
    FILTERED_BLURRED_NAME = f"Afiltered Blurred Bound: {BOUND}"
    FILTERED_NON_BLURRED_NAME = f"Afiltered Non-Blurred Bound: {BOUND}"

    # raw_img = read_img("img.jpg")
    raw_img = read_img("test_img.jpg")

    gs_img = get_grayscale(raw_img)
    blurred_img = get_blurred(gs_img, b=B, blur=True)
    filtered_blurred_img = get_filtered(blurred_img, bound=BOUND, filter=True)

    save_to_file(filtered_blurred_img, f"{FILTERED_BLURRED_NAME}.png")

    # show(gs_img, f"grayscale")
    # show(filtered_blurred_img, FILTERED_BLURRED_NAME)

    dust_field = DustField(filtered_blurred_img)
    print(dust_field.distribute_dust_by_size())


def test() -> None:
    test_list = [
        [0 for j in range(3)]
        for i in range(3)
    ]
    dust_field = DustField(test_list)

    print(dust_field.field)





if __name__ == '__main__':
    main()
    # test()
    cv.waitKey(0)
    cv.destroyAllWindows()
