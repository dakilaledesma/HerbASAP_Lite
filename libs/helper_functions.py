import cv2
import numpy as np
import rawpy
import json


def scale_images_with_info(im, largest_dim=1875):
    """
    Function that scales images proportionally, and returns both the original image size as a tuple of image
    dimensions, and the scaled down image.
    :param im: Image to be scaled down.
    :type im: cv2 Image
    :param largest_dim: The largest dimension to be scaled down to.
    :type largest_dim: int
    :return: Returns both the original image dimensions as a tuple and the scaled image.
    :rtype: tuple, cv2 Image
    """
    image_height, image_width = im.shape[0:2]

    if image_width > image_height:
        reduced_im = cv2.resize(im,
                                (largest_dim,
                                 round((largest_dim / image_width) * image_height)),
                                interpolation=cv2.INTER_NEAREST)
    else:
        reduced_im = cv2.resize(im,
                                (round((largest_dim / image_height) * image_width),
                                 largest_dim),
                                interpolation=cv2.INTER_NEAREST)
    return (image_width, image_height), reduced_im


def apply_corrections(crc_avg_white, raw_base, flip_value):
    """
    applies postprocessing to self.raw_base based on what was learned
    from the initial openImageFile object.
    """
    cc_avg_white = crc_avg_white
    if cc_avg_white:  # if a cc_avg_white value was found
        # get max channel value
        maxChan = max(cc_avg_white)
        # get position of max channel value
        maxPos = cc_avg_white.index(maxChan)
        # get the average channel value from all 3 channels
        avgChan = np.mean(cc_avg_white)
        # avgChan = np.partition(cc_avg_white, 1)[1]
        # divide all values by the max channel value
        cc_avg_white = [maxChan / x for x in cc_avg_white]

        # replace the max channel value with avgchannel value / itself
        cc_avg_white[maxPos] = avgChan / maxChan
        r, g, b = cc_avg_white
        # adjust green channel for the 4-to-3 channel black magicks
        g = g / 2
        wb = [r, g, b, g]
        use_camera_wb = False
    else:  # otherwise use as shot values
        use_camera_wb = True
        wb = [1, 1, 1, 1]

    rgb_cor = raw_base.postprocess(demosaic_algorithm=rawpy.DemosaicAlgorithm.AHD,
                                   # dcb_enhance=True,
                                   # use_auto_wb=True,
                                   use_camera_wb=use_camera_wb,
                                   user_wb=wb,
                                   # highlight_mode=rawpy.HighlightMode.Blend,
                                   output_color=rawpy.ColorSpace.sRGB,
                                   # output_bps=8,
                                   user_flip=flip_value,
                                   user_sat=None,
                                   auto_bright_thr=None,
                                   bright=1.0,
                                   exp_shift=None,
                                   chromatic_aberration=(1, 1),
                                   # exp_preserve_highlights=1.0,
                                   no_auto_scale=False,
                                   gamma=None
                                   )
    raw_base.close()
    del raw_base
    return rgb_cor


def cli_print(message, running_interface=True):
    if not running_interface:
        print(message)


def set_input_folder(folder: str):
    set_settings("input_folder", folder)


def set_output_folder(folder: str):
    set_settings("output_folder", folder)


def set_settings(key: str, value: str):
    settings = read_settings()
    settings[key] = value
    write_settings(settings)


def write_settings(settings: dict):
    with open("../config/Default.json", 'w') as out_file:
        json.dump(settings, out_file, indent=4, sort_keys=True)


def read_settings(filepath: str) -> dict:
    with open(filepath) as json_file:
        settings = json.load(json_file)
    return settings