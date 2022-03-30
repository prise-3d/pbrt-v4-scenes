import os
import argparse
import time
import glob


def main():


    parser = argparse.ArgumentParser(description="Generate file with all p3d scenes")

    parser.add_argument('--scenes', type=str, help="pbrt scenes folder", required=True)
    parser.add_argument('--output', type=str, help="output file", required=True)

    args = parser.parse_args()

    scenes_folder = args.scenes
    output = args.output

    all_p3d_scenes = glob.glob(f'{scenes_folder}/**/p3d_*.pbrt')

    output_folder, _ = os.path.split(output)

    if len(output_folder) > 0 and not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(output, 'w') as f:

        for scene_path in all_p3d_scenes:
            f.write(f'{scene_path}\n')
        


if __name__ == '__main__':
    main()