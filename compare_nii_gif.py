import argparse
import os
from compare_nii import *

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--in_paths",
    help = "required. specificy location of paths of nifti files to compare (must be comma seperated)",
    type = str,
    required = True)
parser.add_argument("-o", "--out_path",
    help = "required. specificy path output directory",
    required = True)
parser.add_argument("--titles",
    help = "optional. title of each nifti image (must be comma seperated)",
    type = str,
    required = False)
parser.add_argument("--frames_per_sec",
    help = "optional. specify speed of switching between files in frames per second. Default: 1",
    required = False)

args = parser.parse_args()

# add defaults
if args.frames_per_sec == None:
    args.frames_per_sec = 1

args.in_paths = [item for item in args.in_paths.split(',')];
args.titles = [item for item in args.titles.split(',')];

def compare_nii(paths, out_path, titles = None, frames_per_sec = 1):

    import imageio
    from imageio.core.util import Array
    import tempfile
    from nilearn.plotting import plot_epi, plot_anat
    import numpy as np

    tmp_dir = tempfile.mkdtemp()

    if titles != None and len(paths) != len(titles):
        error_msg = 'error, titles must be None or length of titles (' + str(len(titles)) + ') must match length of paths (' + str(len(paths)) + ')'
        raise Exception(error_msg)

    # create and save individual direction plots
    for display_mode in ['x', 'y', 'z']:
        if display_mode == 'x':
            cut_coords = [-50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50]
        else:
            cut_coords = [-60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60]
        for i in range(len(paths)):
            plot_anat(paths[i], display_mode = display_mode, cut_coords = cut_coords, title = titles[i], output_file = tmp_dir + '/fig-' + str(i) + '_dir-' + display_mode + '.png')

    images = []
    for i in range(len(paths)):

        # read
        tmp_x = imageio.imread(tmp_dir + '/fig-' + str(i) + '_dir-x.png')
        tmp_y = imageio.imread(tmp_dir + '/fig-' + str(i) + '_dir-y.png')
        tmp_z = imageio.imread(tmp_dir + '/fig-' + str(i) + '_dir-z.png')
        dims = np.vstack((tmp_x.shape, tmp_y.shape, tmp_z.shape)).max(axis = 0)

        # expand to max dim and fill with zeros
        tmp_x_std = np.zeros(dims)
        tmp_x_std[:tmp_x.shape[0], :tmp_x.shape[1], :tmp_x.shape[2]] = tmp_x
        tmp_y_std = np.zeros(dims)
        tmp_y_std[:tmp_y.shape[0], :tmp_y.shape[1], :tmp_y.shape[2]] = tmp_y
        tmp_z_std = np.zeros(dims)
        tmp_z_std[:tmp_z.shape[0], :tmp_z.shape[1], :tmp_z.shape[2]] = tmp_z

        # combine plot directions
        tmp = np.append(tmp_x_std, tmp_y_std, axis = 0)
        tmp = np.append(tmp, tmp_z_std, axis = 0)

        # combine all plots
        images.append(Array(tmp))

    # save plot
    imageio.mimsave(out_path, images, fps = frames_per_sec)


compare_nii(args.in_paths, args.out_path, args.titles, args.frames_per_sec)
