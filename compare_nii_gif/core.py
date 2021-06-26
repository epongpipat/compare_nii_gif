import imageio
from imageio.core.util import Array
import tempfile
from nilearn.plotting import plot_anat
import numpy as np

def compare_nii_gif(paths, out_path, titles = None, frames_per_sec = 1):

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
            if titles == None:
                plot_anat(paths[i], display_mode = display_mode, cut_coords = cut_coords, output_file = tmp_dir + '/fig-' + str(i) + '_dir-' + display_mode + '.png')
            else:
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
