
settings = {
    "input_folder": "C:/Users/Dakila/Pictures/HA/Input",
    "output_folder": "C:/Users/Dakila/Pictures/HA/Output2",
    "process_crc": "T",
    "barcode_rename": "T",
    "barcode_pattern": "",
    "detect_blur": "T",
    "blur_threshold": "0.045",
    "determine_scale": "T",
    "verify_rotation": "T",
    "correct_whitebalance": "T",
    "crc_type": "ISA ColorGauge Nano",
    "partition_size": "125",
    "crc_location": "Lower right"
}


def build_menu_string():
    global settings
    out_string = f"""
    Current settings
        Input folder: {settings["input_folder"]}
        Output folder: {settings["output_folder"]}
        
    Options
        1: Change input folder
        2: Change output folder
        P: Process
        R: Refresh configuration from file
        Q: Quit
    """

    return out_string


def cli_print(message, running_interface=True):
    if not running_interface:
        print(message)


def set_input_folder():
    global settings
    input_folder = filedialog.askdirectory()
    settings["input_folder"] = input_folder


def set_output_folder():
    global settings
    output_folder = filedialog.askdirectory()
    settings["output_folder"] = output_folder


def write_settings():
    global settings
    with open("config/config.json", 'w') as out_file:
        json.dump(settings, out_file)


def read_settings():
    global settings
    with open("config/config.json") as json_file:
        settings = json.load(json_file)


def process():
    global settings

    """
    Getting number of workers for multiprocessing, minimum 3 workers
    """
    num_workers = max([3, multiprocessing.cpu_count()])

    """
    Shaping the data to follow the number of workers for multiprocessing
    """
    files = glob(f'{settings["input_folder"]}/*.CR2')
    print(f"Found {len(files)} file(s)")

    # file_batches = []
    # while True:
    #     if len(files) == 0:
    #         break
    #     elif 0 < len(files) < num_workers:
    #         file_batches.append(files)
    #         break
    #
    #     file_batches.append(files[:num_workers])
    #     del files[:num_workers]

    def compute(idx, file):
        """
        Function for computing/processing the images. This function gets fed into joblib, which gives this function to
        different threads on the CPU. This allows for multiple images to be processed at once.

        :param file: the filename of the image to be opened and processed.
        :return:
        """

        """
        Setting up functions
        """
        barcode_read = bcRead(patterns=settings["barcode_pattern"])
        blur_detection = blurDetect()
        crc_processing = ColorchipRead()
        determine_scale = ScaleRead()
        read_metadata = MetaRead()

        """
        Opening the RAW file
        """
        ext_wb = [1, 0.5, 1, 0.5]
        try:  # use rawpy to convert raw to openCV
            raw_base = rawpy.imread(file)
            base = raw_base
            im = base.postprocess(
                output_color=rawpy.ColorSpace.raw,
                use_camera_wb=False,
                highlight_mode=rawpy.HighlightMode.Ignore,
                user_flip=0,
                use_auto_wb=False,
                user_wb=ext_wb,
                no_auto_bright=False,
                demosaic_algorithm=rawpy.DemosaicAlgorithm.LINEAR
            )
        except:
            if file != '':
                print("Error opening file! Aborting.")
            raise  # Pass this up to the process function for halting

        """
        Processing the image
        """
        file_name, ext = os.path.splitext(file)
        base_name = os.path.basename(file_name)

        # Convert to grayscale for barcode reading and blur detection
        gray_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        if settings["barcode_rename"] == "T":
            barcodes = barcode_read.decodeBC(gray_image)
        if settings["detect_blur"] == "T":
            blur_threshold = float(settings["blur_threshold"])
            blur_detection.blur_check(gray_image, blur_threshold, True)

        # reduce the image for the cnn, store it incase of problem dialogs
        original_size, reduced_img = scale_images_with_info(im)

        if any([settings["determine_scale"],
                settings["verify_rotation"],
                settings["correct_whitebalance"]]):

            try:
                crc_type = settings["crc_type"]
                if crc_type == "ISA ColorGauge Nano":  # aka small crc
                    cc_location, cropped_cc, cc_crop_time = \
                        crc_processing.process_colorchip_small(reduced_img,
                                                               original_size,
                                                               high_precision=True,
                                                               partition_size=int(settings["partition_size"]))
                elif crc_type == 'Tiffen / Kodak Q-13  (8")':
                    cc_location, cropped_cc, cc_crop_time = crc_processing.process_colorchip_big(im, pp_fix=1)
                else:
                    cc_location, cropped_cc, cc_crop_time = crc_processing.process_colorchip_big(im)
                x1, y1, x2, y2 = cc_location

                if settings["determine_scale"]:
                    # scale determination code
                    full_res_cc = im[y1:y2, x1:x2]
                    # lookup the patch area and seed function
                    patch_mm_area, seed_func, to_crop = determine_scale.scale_params.get(crc_type)
                    pixels_per_mm, pixels_per_mm_uncertainty = determine_scale.find_scale(full_res_cc,
                                                                                          patch_mm_area,
                                                                                          seed_func,
                                                                                          to_crop)
                    print(f"Pixels per mm for {file_name}: {pixels_per_mm}, +/- {pixels_per_mm_uncertainty}")

                cc_quadrant = crc_processing.predict_color_chip_quadrant(original_size, cc_location)

                if settings["correct_whitebalance"]:
                    try:
                        crc_avg_white, crc_blk_point = crc_processing.predict_color_chip_whitevals(cropped_cc, crc_type)
                    # if colorchipDetect fails it will raise a SquareFindingFailed error
                    except SquareFindingFailed:
                        # Need to add function failed functionality.
                        pass

                if settings["verify_rotation"]:
                    quad_map = ['Upper right',
                                'Upper left',
                                'Lower left',
                                'Lower right']
                    user_def_quad = quad_map.index(settings["crc_location"]) + 1
                    # cc_quadrant starts at first,
                    # determine the proper rawpy flip value necessary
                    rotation_qty = (cc_quadrant - user_def_quad)
                    # rawpy: [0-7] Flip image (0=none, 3=180, 5=90CCW, 6=90CW)
                    # create a list to travel based on difference
                    rotations = [6, 3, 5, 0, 6, 3, 5]
                    startPos = 3  # starting position in the list
                    endPos = rotation_qty + startPos  # ending index in the list
                    flip_value = rotations[endPos]  # value at that position

                im = apply_corrections(raw_base=raw_base,
                                       crc_avg_white=crc_avg_white,
                                       flip_value=flip_value)

                width, height = original_size
                if flip_value == 3:
                    x1, x2, y1, y2 = width - x2, width - x1, height - y2, height - y1

                elif flip_value == 5:
                    x1, y1, x2, y2 = y1, width - x2, y2, width - x1

                elif flip_value == 6:
                    x1, x2, y1, y2 = height - y2, height - y1, x1, x2

                cc_location = x1, y1, x2, y2


            # apply corrections based on what is learned from the colorchipDetect
            except ColorChipError as e:
                return

        """
        Not implementing lens correction intentionally due to poor support
        """
        # if profile.get('lensCorrection', True):
        #     # equipment corrections
        #     eq_worker_data = EQWorkerData(self.im)
        #     eq_job = Job('eq_worker', eq_worker_data, self.eqRead.lensCorrect)
        #     self.boss_thread.request_job(eq_job)

        if settings["barcode_rename"] == "T" and len(barcodes) > 0:
            names = barcodes[0]
        else:
            names = base_name

        """
        Save the image
        """
        im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)

        # retrieve the source image exif data
        # add Additional user comment details for the metadata
        h, w = im.shape[0:2]
        addtl_user_comments = {
            'avgWhiteRGB': str(crc_avg_white),
            'barcodeValues': names,
            'origHeight': str(h),
            'origWidth': str(w),
            'ccQuadrant': str(cc_quadrant),
            'ccLocation': str(cc_location),
            'pixelsPerMM': str(pixels_per_mm),
            'pixelsPerMMConfidence': str(pixels_per_mm_uncertainty)
        }

        # meta_data = read_metadata.retrieve_src_exif(file,
        #                                             addtl_user_comments)
        final_filename = f"{settings['output_folder']}/{names}.jpg"
        cv2.imwrite(final_filename, im)
        # read_metadata.set_dst_exif(meta_data, final_filename)

        print(f"[HAL-SIGM]:bar:{idx},{len(files)}:{names}.jpg finished ({idx}/{len(files)})")

    """
    The joblib Parallel function is written in this way so that it reuses wPorkers vs. create/destroy.
    """

    # Parallel(n_jobs=num_workers)(delayed(compute)(idx, file) for idx, file in enumerate(files))

    with Parallel(n_jobs=num_workers) as parallel:
        out = parallel(delayed(compute)(idx, file) for idx, file in enumerate(files))

    # for idx, file_batch in enumerate(file_batches):
    #     out = Parallel(n_jobs=num_workers)(delayed(compute)(file) for file in file_batch)
    #     # for file in file_batch:
    #     #     compute(file)
    #     print(idx, len(file_batches))

    print(f"[HAL-DONE]")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='CLI/Interface Parser')
    parser.add_argument('--interface', dest='interface', action='store_true')
    parser.set_defaults(interface=False)

    parsed_args = parser.parse_args()
    running_interface = parsed_args.interface

    cli_print("Loading...", running_interface=running_interface)
    import json
    from joblib import Parallel, delayed
    from glob import glob
    import multiprocessing
    import os

    from libs.bcRead import bcRead
    from libs.blurDetect import blurDetect
    from libs.ccRead import ColorchipRead, ColorChipError, SquareFindingFailed
    from libs.scaleRead import ScaleRead
    from libs.metaRead import MetaRead
    from libs.helper_functions import *
    cli_print("Welcome to HerbASAP Lite v0.0.1", running_interface=running_interface)

    while True:
        # read_settings()
        cli_print(build_menu_string(), running_interface=running_interface)
        if running_interface:
            process()
            break
        else:
            _input = str(input("What would you like to do?: ")).upper()

            if _input == 'Q':
                break
            elif _input == 'R':
                continue
            elif _input == 'P':
                process()
            elif _input in [str(v) for v in range(1, 3)]:
                if _input == '1':
                    root = tk.Tk()
                    set_input_folder()
                    root.destroy()
                elif _input == '2':
                    root = tk.Tk()
                    set_output_folder()
                    root.destroy()

                # write_settings()
