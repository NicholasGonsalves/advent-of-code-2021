"""Day 19."""


def read_file(file_name: str):
    """Read file and parse input."""
    with open(file_name) as f:
        inputs = f.readlines()
    enhancement = inputs[0].strip()
    image = [row.strip() for row in inputs[2:]]
    return enhancement, image


# y, x
directions = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 0),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def in_bounds(point, image):
    if (point[0] >= 0) and (point[0] < len(image)) and (point[1] >= 0) and (point[1] < len(image[0])):
        return True
    return False


def get_convolution_area(image, x, y, infinite_tile_value):
    """
    Get convolution area (the tile being considered, and the 8 surrounding it, in order top-left to bottom right).
    Tile to be used if a position is out of bounds is parameterised, as this can flip on each pass.
    """
    conv = []
    for y_add, x_add in directions:
        if in_bounds([y + y_add, x + x_add], image):
            conv.append(image[y + y_add][x + x_add])
        else:
            conv.append(infinite_tile_value)
    return conv


def get_index_for_enhancement(conv):
    """Convert 'convolution' (it's not really convolution) area to binary and get decimal value."""
    return int("".join(conv).replace("#", "1").replace(".", "0"), 2)


def extend_image_with_infinite_tile_padding(image, tile):
    """Pad."""
    tile_row = [tile for _ in range(len(image[0])+2)]
    new_image = [tile_row]
    for row in image:
        new_image.append([tile] + list(row) + [tile])
    new_image.append(tile_row)
    return new_image


def enhance(enhancement, image, infinite_tile):
    """Main enhance image function."""
    image = extend_image_with_infinite_tile_padding(image, infinite_tile)
    new_image = []
    for y in range(len(image)):
        new_row = []
        for x in range(len(image[0])):
            conv = get_convolution_area(image, x, y, infinite_tile)
            index = get_index_for_enhancement(conv)
            new_value = enhancement[index]
            new_row.append(new_value)
        new_image.append(new_row)

    return new_image


def count_lit_pixels(image):
    count = 0
    for row in image:
        for pixel in row:
            if pixel == '#':
                count += 1
    return count


def part_one(enhancement, image):
    """Apply enhancement twice."""
    # Two enhancements are called here with differing inf_tile parameters.
    # This is because the infinite set of tiles outside of the image can flip
    # depending on the value of the first tile in 'enhancement'.
    image = enhance(enhancement, image, ".")
    image = enhance(enhancement, image, enhancement[0])
    return count_lit_pixels(image)


def part_two(enhancement, image):
    """Apply enhancement 50 times."""
    for _ in range(25):
        image = enhance(enhancement, image, ".")
        image = enhance(enhancement, image, enhancement[0])
    return count_lit_pixels(image)


if __name__ == "__main__":
    data1, data2 = read_file("day20.txt")

    print(part_one(data1, data2))
    print(part_two(data1, data2))

