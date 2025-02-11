import os
import argparse
import time
import glob



def main():

    parser = argparse.ArgumentParser(description="Convert EXR image to PNG using imagemagick")

    parser.add_argument('--folder', type=str, help="exr folder", required=True)
    parser.add_argument('--output', type=str, help="", required=True)
    args = parser.parse_args()

    folder = args.folder
    output = args.output

    # create empty directory if not exists
    if not os.path.exists(output):
        os.makedirs(output)


    exr_files = glob.glob(os.path.join(folder, '**', '*.exr'), recursive=True)
    
    for exr in sorted(exr_files):
        output_exr = exr.replace(folder, output).replace('.exr', '.png')
        head, _ = os.path.split(output_exr)

        if not os.path.exists(head):
            os.makedirs(head)

        print(f'convert {exr} in {output_exr}')
        os.system(f'convert {exr} -colorspace RGB -gravity center -crop 800x800+0+0 {output_exr}')


if __name__ == '__main__':
    main()