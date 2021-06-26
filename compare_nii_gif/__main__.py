import argparse
import os
from compare_nii_gif import core, __version__

def main():
    print('compare_nii_gif v' + __version__ + '\n')
    parser = argparse.ArgumentParser(description = '')
    parser.add_argument("-i", "--in_paths",
        nargs = '*',
        action = 'append',
        help = "required. specificy location of paths of nifti files to compare",
        required = True)
    parser.add_argument("-o", "--out_path",
        help = "required. specificy path to output gif file",
        required = True)
    parser.add_argument("--titles",
        nargs = '*',
        action = 'append',
        default = None,
        help = "optional. title of each nifti image (default: None)",
        type = str,
        required = False)
    parser.add_argument("--frames_per_sec",
        default = 1,
        help = "optional. specify speed of switching between files in frames per second. (Default: 1)",
        required = False)

    args = parser.parse_args()

    #print(args.in_paths.dim)
    args.in_paths = args.in_paths[0]
    if args.titles != None:
        args.titles = args.titles[0]

    print('images to compare:')
    for i in range(len(args.in_paths)):
        if args.titles == None:
            print(str(i + 1) + '. ' + args.in_paths[i])
        else:
            print(str(i + 1) + '. ' + args.titles[i] + ': ' + args.in_paths[i])

    core.compare_nii_gif(args.in_paths, args.out_path, args.titles, args.frames_per_sec)

    print('\noutput successfully saved to ' + args.out_path + '\n')

if __name__ == "__main__":
    main()
