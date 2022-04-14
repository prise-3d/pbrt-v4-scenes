import os
import argparse
import time

# some parameters
SPP = 1
INDEPENDENT = 0
NIMAGES = 30

def get_nspp_image(filename):
    print(filename.split('.')[0])
    print(filename.split('.')[0].split('-'))
    return int(filename.split('.')[0].split('-')[-2].replace('S', ''))

def main():

    parser = argparse.ArgumentParser(description="Run multiple instance of pbrt v4")

    parser.add_argument('--pbrt', type=str, help="pbrt executable", required=True)
    parser.add_argument('--scenes', type=str, help='File of scenes list', required=True)
    parser.add_argument('--estimators', type=str, help='estimators', required=True)
    parser.add_argument('--gpu', type=int, help='enable GPU (0 or 1)', default=0)
    parser.add_argument('--options', type=str, help='other options', default='')
    parser.add_argument('--output', type=str, help="output folder", required=True)

    args = parser.parse_args()

    pbrt = args.pbrt
    scenes_file = args.scenes
    estimators = args.estimators.split(',')
    gpu = args.gpu
    options = args.options
    output = args.output

    scenes = []

    with open(scenes_file, 'r') as f:
        for l in f.readlines():
            scenes.append(l.replace('\n', ''))

    # create empty directory if not exists
    if not os.path.exists(output):
        os.makedirs(output)

    for est in estimators:

        output_est = os.path.join(output, est)
        if not os.path.exists(output_est):
            os.makedirs(output_est)

        for scene in scenes:

            # check if already images with same number of SPP are already generated
            # ToDo: improve scene folder access...
            _, scene_file = os.path.split(scene)
            output_scene_path = os.path.join(output_est, scene_file.replace('.pbrt', ''))
            print(output_scene_path)
            computed_images = os.listdir(output_scene_path)
            expected_images = [ e for e in computed_images if get_nspp_image(e) == SPP ]

            start_index = len(expected_images)

            if start_index > 0:

                if start_index == NIMAGES:
                    continue

                print(f'Restart rendering of scene {scene} with {est} from image n°{start_index}')
            else:
                print(f'Rendering of scene {scene} with {est}')

            scene_folder, pbrt_filename = os.path.split(scene)

            pbrt_cmd = f'{pbrt} {"--gpu " if gpu else ""} --folder {output_est} --spp {SPP}' \
                    f' --nimages {NIMAGES} --startindex {start_index} --independent {INDEPENDENT} --estimator {est}' \
                    f' {options} {pbrt_filename}'
                    
            # go into folder
            os.system(f'cd {scene_folder} && {pbrt_cmd} && cd ..')
            time.sleep(10)
        


if __name__ == '__main__':
    main()