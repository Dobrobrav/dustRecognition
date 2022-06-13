# from PIL import Image
from numpy import ndarray
from skimage import io, img_as_float
import cv2 as cv
from typing import TypeAlias


Picture: TypeAlias = ndarray


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
        # print(row)
        for j, pixel_value in enumerate(row):
            if pixel_value > bound:
                # print(pixel_value)
                row[j] = 255

    return copy_img


def save_to_file(img: Picture, name: str = "result_50_8_50.png") -> None:
    cv.imwrite(name, img)


def show(img: Picture, name: str = "some_img") -> None:
    cv.imshow(name, img)


def main():
    BOUND = 155
    FILTERED_BLURRED_NAME = f"Afiltered Blurred Bound: {BOUND}"
    FILTERED_NON_BLURRED_NAME = f"Afiltered Non-Blurred Bound: {BOUND}"

    raw_img = read_img("img.jpg")

    gs_img = get_grayscale(raw_img)
    blurred_img = get_blurred(gs_img, b=6, blur=False)
    filtered_blurred_img = get_filtered(blurred_img, bound=BOUND, filter=True)
    filtered_non_blurred_img = get_filtered(blurred_img, bound=BOUND, filter=False)

    save_to_file(filtered_blurred_img, f"{FILTERED_BLURRED_NAME}.png")

    show(gs_img, f"grayscale")
    # show(blurred_img, f"blurred")
    show(filtered_blurred_img, FILTERED_BLURRED_NAME)
    show(filtered_non_blurred_img, FILTERED_NON_BLURRED_NAME)

    # print(filtered_img[0])




    # cv.imshow("canny_orig", cv.Canny(img, 10, 200))
    # cv.imshow("canny_filt", cv.Canny(filtered, 10, 200))

    cv.waitKey(0)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()

