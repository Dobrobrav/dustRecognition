from tools import *
from dust_field import *
from dust_piece import *
from cell import *


def main():
    fig, ax = plt.subplots()

    BOUND = 160
    A = 50
    B = 5
    C = 50

    FILTERED_BLURRED_NAME = f"Afiltered Blurred Bound: {BOUND}"
    FILTERED_NON_BLURRED_NAME = f"Afiltered Non-Blurred Bound: {BOUND}"

    raw_img = read_img("../pictures/img.jpg")
    # raw_img = read_img("../pictures/test_img.jpg")

    gs_img = get_grayscale(raw_img)
    blurred_img = get_blurred(gs_img, a=A, b=B, c=C, blur=True)
    filtered_blurred_img = get_filtered(blurred_img, bound=BOUND, filter=True)

    save_to_file(filtered_blurred_img)

    show(gs_img, f"grayscale")
    show(filtered_blurred_img, FILTERED_BLURRED_NAME)

    dust_field = DustField(filtered_blurred_img)

    distribution = dust_field.distribute_dust_by_size()
    print(sum(distribution.values()))
    distribution = OrderedDict(sorted(distribution.items()))
    distribution.popitem()
    print(distribution)
    # distribution.popitem()

    build_histogram(distribution)



if __name__ == '__main__':
    main()
    cv.waitKey(0)
    cv.destroyAllWindows()
