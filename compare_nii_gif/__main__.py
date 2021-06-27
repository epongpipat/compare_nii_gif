import argparse
import os
from compare_nii_gif import core, __version__

def main():
    print('compare_nii_gif v' + __version__ + '\n')
    parser = argparse.ArgumentParser(description = 'Create a gif that compares nifti files in axial, sagittal, and coronal views')
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
    parser.add_argument("-x", "--x_coords",
        nargs = '*',
        action = 'append',
        default = [[-50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50]],
        type = int,
        help = "optional. specify coordinates to display in the x-direction. (Default: -50 -40 -30 -20 -10 0 10 20 30 40 50)",
        required = False)
    parser.add_argument("-y", "--y_coords",
        nargs = '*',
        action = 'append',
        default = [[-60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60]],
        type = int,
        help = "optional. specify coordinates to display in the y-direction. (Default: -60 -50-40 -30 -20 -10 0 10 20 30 40 50 60)",
        required = False)
    parser.add_argument("-z", "--z_coords",
        nargs = '*',
        action = 'append',
        default = [[-60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60]],
        type = int,
        help = "optional. specify coordinates to display in the z-direction. (Default: -60 -50 -40 -30 -20 -10 0 10 20 30 40 50 60)",
        required = False)
    args = parser.parse_args()

    args.in_paths = args.in_paths[0]
    if args.titles != None:
        args.titles = args.titles[0]

    args.x_coords = args.x_coords[0]
    args.y_coords = args.y_coords[0]
    args.z_coords = args.z_coords[0]
    #print(args.z_coords)

    print('images to compare:')
    for i in range(len(args.in_paths)):
        if args.titles == None:
            print(str(i + 1) + '. ' + args.in_paths[i])
        else:
            print(str(i + 1) + '. ' + args.titles[i] + ': ' + args.in_paths[i])

    core.compare_nii_gif(paths = args.in_paths, out_path = args.out_path, titles = args.titles, frames_per_sec = args.frames_per_sec, x_coords = args.x_coords, y_coords = args.y_coords, z_coords = args.z_coords)

    print('\noutput successfully saved to ' + args.out_path + '\n')

if __name__ == "__main__":
    main()
