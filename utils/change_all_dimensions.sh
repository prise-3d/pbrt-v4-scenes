#! /bin/bash
if [ -z "$1" ]
  then
    echo "No argument supplied"
    echo "Need previous extension used"
    exit 1
fi

if [ -z "$2" ]
  then
    echo "No argument supplied"
    echo "Need new extension to use"
    exit 1
fi


main_folder="./"
prefix="p3d_"

xresolution=$1
yresolution=$2

for folder in $(ls -d ${main_folder}*)
do
  for file in $(ls $folder)
  do
    filename=$folder/$file
    filename_fixed=${filename//\/\//\/}

    # check if filename contains 
    if [[ "$file" == ${prefix}* ]]; then
        echo "Update image extension (xresolution to ${xresolution} and yresolution to ${yresolution}) into ${filename_fixed}"
        python utils/change_dimensions_pbrt.py --xresolution ${xresolution} --yresolution ${yresolution} --pbrt ${filename_fixed}
    fi 
  done
done