import os
import cv2
import argparse
import logging
from tqdm import tqdm

from remove_duplicates import remove_duplicates_from_folder

logging.getLogger().setLevel(logging.INFO)


def write_clean_data(clean_filenames: list, dest_path: str) -> None:
    logging.info(f'Writing clean data in the subdirectory "filtered/"')
    for filename in tqdm(clean_filenames):
        cv2.imwrite(os.path.join(dest_path, os.path.basename(filename)), cv2.imread(filename))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='dataset/', help='Path to folder of images')
    args = parser.parse_args()

    filtered_path = os.path.join(args.path, "filtered/")  # folder where clean data is stored
    os.makedirs(filtered_path, exist_ok=True)

    IMG_RESIZE = (640, 480)  # size to which all images are resized
    CNT_AREA_MIN = 100  # reject contours below this threshold
    SCORE_MIN = 2000  # reject images with score below this threshold

    clean_data_list = remove_duplicates_from_folder(args.path, IMG_RESIZE, SCORE_MIN, CNT_AREA_MIN)

    write_clean_data(clean_data_list, filtered_path)
