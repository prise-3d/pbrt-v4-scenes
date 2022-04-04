import os
import argparse
from classes.exr import EXR

NDIGITS = 4

def main():

    parser = argparse.ArgumentParser(description="Get all base2 EXR images")

    parser.add_argument('--folder', type=str, help="all scenes with folder", required=True)
    parser.add_argument('--output', type=str, help="output expected folder", required=True)
    parser.add_argument('--base', type=int, help="output base indices images", default=2)
    args = parser.parse_args()

    folder = args.folder
    output = args.output
    base = args.base

    # create empty directory if not exists
    if not os.path.exists(output):
        os.makedirs(output)

    scenes = sorted(os.listdir(folder))

    # for each scene reconstruct all base 2 images
    for scene in scenes:

        print(f'Extract all images of {scene} using base {base}')

        scene_path = os.path.join(folder, scene)
        output_scene_path = os.path.join(output, scene)

        # do it only if folder does not exists...
        if not os.path.exists(output_scene_path):
            
            # create output folder
            os.makedirs(output_scene_path)

            # list every images
            scene_images = sorted(os.listdir(scene_path))

            previous_exr = None
            current_base_value = 1
            current_spp = 0

            for img in scene_images:
                
                img_path = os.path.join(scene_path, img)
                current_exr = EXR.fromfile(img_path)

                # increase the current number of spp
                current_spp += current_exr.spp

                # do the fusion if previous exists
                if previous_exr is not None:
                    current_exr = EXR.fusion([current_exr, previous_exr])

                # save current exr if spp corresponds to specific base
                if current_exr.spp == current_base_value:

                    # get the expected digit number
                    str_index = str(current_exr.spp)

                    while len(str_index) < NDIGITS:
                        str_index = "0" + str_index

                    # get the output filename
                    output_filename = os.path.join(output_scene_path, 
                                                f'{scene}-{str_index}.exr')

                    # save the current image
                    current_exr.save(output_filename)
                    print(f'[base: {base}] save exr file with {current_base_value} spp')

                    # increase the output base image
                    current_base_value = current_base_value * base
                
                # set new previous exr file
                previous_exr = current_exr



if __name__ == '__main__':
    main()