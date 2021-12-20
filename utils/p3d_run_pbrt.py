import os
import argparse

# some parameters
SPP = 20
INDEPENDENT = 0
NIMAGES = 500


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

    for scene in scenes:

        _, scene_folder = os.path.split(scene)

        output_scene = os.path.join(output, scene_folder)
        if not os.path.exists(output_scene):
            os.makedirs(output_scene)

        for est in estimators:

            pbrt_cmd = f'{pbrt} {"--gpu " if gpu else ""} --folder {output} --spp {SPP}' \
                    f' --nimages {NIMAGES} --independent {INDEPENDENT} --estimator {est}' \
                    f' {options} {scene}'

            print(pbrt_cmd)





if __name__ == '__main__':
    main()