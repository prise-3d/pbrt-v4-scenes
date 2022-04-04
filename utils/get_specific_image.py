import os
import argparse
from classes.exr import EXR


def find_by_spp(images, spp):

    f = lambda p: int(p.split('-')[-1].replace('.exr', '')) == spp
    return next(filter(f, images), None)

def main():

    parser = argparse.ArgumentParser(description="Get expected base 2 EXR image")

    parser.add_argument('--folder', type=str, help="scene folder", required=True)
    parser.add_argument('--spp', type=int, help="expected spp index", required=True)
    parser.add_argument('--output', type=str, help="output expected folder", required=True)
    parser.add_argument('--base', type=int, help="output base indices images", default=2)

    args = parser.parse_args()

    folder = args.folder
    spp = args.spp
    output = args.output
    base = args.base

    # create empty directory if not exists
    if not os.path.exists(output):
        os.makedirs(output)

    # list every images
    scene_images = sorted(os.listdir(folder))

    binary_str = "{0:b}".format(spp)[::-1]
    
    image_index = 1

    previous_exr = None

    # for each binary value, do the fusion
    for i in binary_str:

        # check if index is expected as output
        if i == "1":
            img = find_by_spp(scene_images, image_index)
            img_path = os.path.join(folder, img)
            
            current_exr = EXR.fromfile(img_path)

            if previous_exr is not None:
                current_exr = EXR.fusion([current_exr, previous_exr])

            previous_exr = current_exr

        image_index = base * image_index


    print("Obtained image contains:", previous_exr.spp)



if __name__ == '__main__':
    main()