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
    dust_piece: 'DustPiece | None' = None

    def __init__(self, i: int, j: int, color: int):
        self.i = i
        self.j = j
        self.color = color

    @property
    def dust_piece(self) -> 'DustPiece | None':
        return self.dust_piece

    @dust_piece.setter
    def dust_piece(self, dust_piece: 'DustPiece') -> None:
        self.dust_piece = dust_piece
        dust_piece.add_cell(self)



class DustPiece:
    current_pk = 0
    cells: list[Cell]

    def __init__(self):
        self.__class__.current_pk += 1
        self.pk = self.__class__.current_pk
        self.cells = []

    def add_cell(self, cell: Cell) -> None:
        self.cells.append(cell)


class DustField:
    dust_pieces: list[Cell]
    field: ndarray

    def __init__(self, field: Picture):
        for i, row in enumerate(self.field):
            for j, color in enumerate(row):
                row[j] = Cell(i, j, color)
        self.field = field

    def distribute_dust_by_size(self) -> dict[DustSize, Quantity]:
        for row in self.field:
            for cell in row:
                if cell.color == 255 or cell.dust_piece:
                    continue

                self.recognize_dust_piece(cell)

    def get_neighbors(self, cell) -> list[Cell]:
        """ Return only neighbours which haven't found their dust piece yet"""
        pass

    def recognize_dust_piece(self, cell: Cell, dust_piece: DustPiece = None) -> None:
        """ Recognize the entire dust piece which contains the cell """
        cell.dust_piece = dust_piece or DustPiece()
        neighbors = self.get_neighbors(cell)
        for neighbor in neighbors:
            self.recognize_dust_piece(neighbor, dust_piece=cell.dust_piece)


def read_img(file_name: str) -> Picture:
    return io.imread(file_name)


def get_grayscale(img: Picture) -> Picture:
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


def get_blurred(img: Picture, a: int = 50, b: int = 8, c: int = 50, blur: bool = True) -> Picture:
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

    raw_img = read_img("img.jpg")

    gs_img = get_grayscale(raw_img)
    blurred_img = get_blurred(gs_img, b=B, blur=True)
    filtered_blurred_img = get_filtered(blurred_img, bound=BOUND, filter=True)

    save_to_file(filtered_blurred_img, f"{FILTERED_BLURRED_NAME}.png")

    show(gs_img, f"grayscale")
    show(filtered_blurred_img, FILTERED_BLURRED_NAME)

    print(type(gs_img[0]))




    # print(filtered_img[0])




    cv.imshow("canny_orig", cv.Canny(filtered_blurred_img, 10, 200))
    # cv.imshow("canny_filt", cv.Canny(filtered, 10, 200))

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()

