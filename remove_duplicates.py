import os
import cv2
from tqdm import tqdm
import logging

from imaging_interview import preprocess_image_change_detection, compare_frames_change_detection
from timestamp_utils import sort_filenames_by_timestamp


def remove_duplicates_from_folder(folder_path: str, img_size: tuple, score_min: int, cnt_area_min: int) -> list:
    """
    Removes duplicate images from a folder of images. Takes as input the folder path and other parameters and returns a
     list of filtered filenames
    :param folder_path: path to the folder where the images are stored
    :param dest_path: path where filtered images are stored (after removing duplicates)
    :param img_size: size to which all images are resized
    :param score_min: minimum score below which an image is rejected
    :param cnt_area_min: minimum contour area below which the contours are rejected
    :return: img_filtered_list: list of filtered filenames
    """

    filenames = [os.path.join(folder_path, name) for name in os.listdir(folder_path) if name.endswith('.png')]
    cam_id_filename_dict = sort_filenames_by_timestamp(filenames)   # segregate by camera id and sort by timestamp
    img_filtered_names = []

    for cam_id, filenames_sorted in cam_id_filename_dict.items():
        logging.info(f'Removing duplicates for Camera ID: {cam_id}')

        prev_frame_raw = None
        prev_frame = None
        for i in tqdm(range(1, len(filenames_sorted))):

            if prev_frame_raw is None:  # read new image for prev_frame_raw only in the first iteration or if
                # a None was encountered in the previous iteration
                prev_frame_raw = cv2.imread(filenames_sorted[i - 1])
            if prev_frame_raw is None:  # for images that cannot be read
                continue

            if prev_frame is None:  # resize and preprocess only in the first iteration or if a None was encountered
                # in the previous iteration. Avoids prev_frame from being resized again.
                prev_frame = cv2.resize(prev_frame_raw, img_size)
                prev_frame = preprocess_image_change_detection(prev_frame, [9])

            curr_frame_raw = cv2.imread(filenames_sorted[i])
            if curr_frame_raw is None:
                continue
            curr_frame = cv2.resize(curr_frame_raw, img_size)
            curr_frame = preprocess_image_change_detection(curr_frame, [9])

            score, _, _ = compare_frames_change_detection(prev_frame, curr_frame, cnt_area_min)

            if score > score_min:  # retain only curr_frame_raw if score is below this threshold
                img_filtered_names.append(filenames_sorted[i])

            prev_frame = curr_frame

    logging.info(f'Duplicates removed: {len(filenames) - len(img_filtered_names)}\n')
    return img_filtered_names



