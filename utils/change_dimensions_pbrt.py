# main imports
import sys, os, argparse
import json


xresolution_line = "\"integer xresolution\""
yresolution_line = "\"integer yresolution\""

def main():

    parser = argparse.ArgumentParser(description="Update image output dimensions of pbrt scene")

    parser.add_argument('--xresolution', type=int, help='xresolution to set into image output scene', required=True)
    parser.add_argument('--yresolution', type=int, help='yresolution to set into image output scene', required=True)
    parser.add_argument('--pbrt', type=str, help='pbrt scene name (this one to convert)', required=True)

    args = parser.parse_args()

    p_xresolution = args.xresolution
    p_yresolution = args.yresolution
    p_pbrt        = args.pbrt
    

    output_content = ""
    # read existing pbrt file
    pbrt_file = open(p_pbrt, 'r')
    pbrt_lines = pbrt_file.readlines()

    for line in pbrt_lines:

        output_line = line
        
        # Update xresolution into file
        if line.find(xresolution_line) != -1:
            output_line = "\t" + xresolution_line + " " + str(p_xresolution) + '\n'

        # Update yresolution into file
        if line.find(yresolution_line) != -1:
            output_line = "\t" + yresolution_line + " " + str(p_yresolution) + '\n'

        output_content = output_content + output_line

    # close all buffers
    pbrt_file.close()

    # update content
    pbrt_outfile = open(p_pbrt, 'w')
    pbrt_outfile.write(output_content)
    pbrt_outfile.close()

if __name__== "__main__":
    main()