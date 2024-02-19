import os
import time
import datetime
from collections import defaultdict
from typing import Optional
import logging


def check_unix_timestamp(timestamp: str) -> Optional[float]:
    # check if timestamp is in unix format

    try:
        _ = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
        return int(timestamp) / 1000
    except ValueError:
        logging.error(f'Incorrect timestamp format: {timestamp}')
        return None


def parse_timestamp(filename: str) -> float:
    # convert all timestamps to unix format

    # extract timestamp from filename after removing file extension
    timestamp = os.path.basename(filename).split('.')[0].replace('-', '_').split('_', 1)[-1]

    try:
        return time.mktime(datetime.datetime.strptime(timestamp, "%Y_%m_%d__%H_%M_%S").timetuple())
    except ValueError:
        return check_unix_timestamp(timestamp)


def sort_filenames_by_timestamp(file_names: list) -> dict:
    # returns a dictionary with camera id as keys and filename as values. The filenames are sorted by timestamp
    # for each camera id.

    camid_filename_dict = defaultdict(list)
    for filename in file_names:
        # extract camera id from filename and add filenames to the corresponding camera id in the dict
        camera_id = os.path.basename(filename).replace('-', '_').split('_', 1)[0]
        camid_filename_dict[camera_id].append(filename)

    for cam_id, camid_filenames in camid_filename_dict.items():
        # remove filenames where timestamps are incorrect and sort them by timestamps in the dict
        camid_filename_dict[cam_id] = [im_name for im_name in camid_filenames if parse_timestamp(im_name) is not None]
        camid_filename_dict[cam_id] = sorted(camid_filename_dict[cam_id], key=lambda im_name: parse_timestamp(im_name))

    return camid_filename_dict
