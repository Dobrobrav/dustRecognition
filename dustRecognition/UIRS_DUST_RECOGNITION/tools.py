from numpy import ndarray
from skimage import io
import cv2 as cv
import matplotlib.pyplot as plt
from typing import TypeAlias
from collections import OrderedDict


Picture: TypeAlias = ndarray
DustSize: TypeAlias = int
Quantity: TypeAlias = int


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


def save_to_file(img: Picture, name: str = "../results/result.png") -> None:
    cv.imwrite(name, img)


def show(img: Picture, name: str = "some_img") -> None:
    cv.imshow(name, img)


def build_histogram(distribution: OrderedDict[DustSize, Quantity]) -> None:
    n = sum(distribution.values())
    Size = list(distribution)
    W = [ni / n for ni in distribution.values()]
    # plt.figure()
    plt.plot(Size, W)
    plt.show()