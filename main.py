import numpy as np
from PIL import Image


def create_image_encoding(file, image_segments, width, height):
    cur_file_data = open(file, 'rb').read()
    cur_file_size = len(cur_file_data)
    characters_in_one_frame = ((width * height) * 3) // 16  # Number of characters in one frame
    image_clump = []
    cur_frame = 0
    cur_character = 0
    cur_image = np.zeros((height, width, 3), dtype=np.uint8)

    while cur_character < cur_file_size:
        if cur_character % characters_in_one_frame == 0 and cur_character != 0:
            cur_frame += 1
            img = Image.fromarray(cur_image, 'RGB')
            img.save(f'frame_{cur_frame}.png')
            cur_image = np.zeros((height, width, 3), dtype=np.uint8)

        r_val = cur_file_data[cur_character] if cur_character < cur_file_size else 0
        g_val = cur_file_data[cur_character + 1] if cur_character + 1 < cur_file_size else 0
        b_val = cur_file_data[cur_character + 2] if cur_character + 2 < cur_file_size else 0

        # Calculate the block index
        block_index = (cur_character - cur_frame * characters_in_one_frame) // 3

        # Calculate the starting position of the 4x4 block
        blocks_per_row = width // 4  # Number of 4x4 blocks per row
        block_row = (block_index // blocks_per_row) * 4  # Starting row of the 4x4 block
        block_col = (block_index % blocks_per_row) * 4  # Starting column of the 4x4 block

        # Fill the 4x4 block with the RGB values
        for i in range(4):
            for j in range(4):
                if block_row + i < height and block_col + j < width:
                    cur_image[block_row + i, block_col + j] = [r_val, g_val, b_val]

        cur_character += 3

    # Adding the last image if it has not been added
    if cur_image.any():
        image_clump.append(cur_image)

    image_segments.append(image_clump)


def main():
    width = 1920
    height = 1080
    files_to_upload = open("files_to_encode.txt")
    files_to_read = files_to_upload.read().split("\n")
    image_segments = []
    print(files_to_read)
    # np.ones((width, height))
    for file in files_to_read:
        create_image_encoding(file, image_segments, width, height)


if __name__ == '__main__':
    main()




