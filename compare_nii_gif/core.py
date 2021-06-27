import imageio
from imageio.core.util import Array
import tempfile
from nilearn.plotting import plot_anat, find_xyz_cut_coords, find_cut_slices
from nilearn.image import load_img
import numpy as np

# def get_coords(in_file, slice_gap, n_slices):
#     xyz_coords = find_xyz_cut_coords(in_file)
#     x_mid = round(xyz_coords[0])
#     y_mid = round(xyz_coords[1])
#     z_mid = round(xyz_coords[2])
#     x_idx = [x_mid]
#     y_idx = [y_mid]
#     z_idx = [z_mid]
#     for i in range(1, n_slices + 1):
#         for sign in [-1, 1]:
#             x_idx.append(x_mid + (slice_gap * sign * i))
#             y_idx.append(y_mid + (slice_gap * sign * i))
#             z_idx.append(z_mid + (slice_gap * sign * i))
#     x_idx.sort()
#     y_idx.sort()
#     z_idx.sort()
#     x_idx.pop(0)
#     x_idx.pop(0)
#     del x_idx[-1]
#     return x_idx, y_idx, z_idx


# img = load_img(in_path)
# data = img.get_fdata()
# data > 1
# x_min = (data > 1)
# np.multiply(hdr.get_data_shape(), hdr.get_zooms())


# def get_dim_bb(data, axis = 0):
#     idx = []
#     for i in range(data.shape[axis]):
#         data_axis = data.take(indices = i, axis = axis)
#         if np.sum(data_axis != 0) > 0:
#             idx.append(i)
#     idx.sort()
#     min = idx[0]
#     max = idx[len(idx)-1]
#     return min, max
#
# def get_brain_coords(data):
#     x_min, x_max = get_dim_bb(data, 0)
#     y_min, y_max = get_dim_bb(data, 1)
#     z_min, z_max = get_dim_bb(data, 2)
#     x = round(np.mean([x_min, x_max]))
#     y = round(np.mean([y_min, y_max]))
#     z = round(np.mean([z_min, z_max]))
#     return {'x': {'min': x_min, 'mid': x, 'max': x_max},
#             'y': {'min': y_min, 'mid': y, 'max': y_max},
#             'z': {'min': z_min, 'mid': z, 'max': z_max}}
#
# def get_brain_idx(in_path, n_slices = 5, slice_gap = 'auto'):
#     img = load_img(in_path)
#     data = img.get_fdata()
#
#
#     dim_list = ['x', 'y', 'z']
#     coords = get_brain_coords(data)
#     slice_gaps = dict()
#     if slice_gap == 'auto':
#         for i in range(len(dim_list)):
#             slice_gaps[dim_list[i]] = np.floor((coords[dim_list[i]]['max'] - coords[dim_list[i]]['min']) / n_slices / 2)
#     idx = dict()
#     for dim in dim_list:
#         idx[dim] = [coords[dim]['mid']]
#         for i in range(1, n_slices + 1):
#             idx[dim].append(coords[dim]['mid'] + i * slice_gaps[dim])
#             idx[dim].append(coords[dim]['mid'] - i * slice_gaps[dim])
#         idx[dim].sort()
#     idx['x'].pop(0)
#     idx['x'].pop(len(idx['x'])-1)
#     return idx

def compare_nii_gif(paths, out_path, titles = None, frames_per_sec = 1, x_coords = [-50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50], y_coords = [-60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60], z_coords = [-60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60]):

    tmp_dir = tempfile.mkdtemp()

    if titles != None and len(paths) != len(titles):
        error_msg = 'error, titles must be None or length of titles (' + str(len(titles)) + ') must match length of paths (' + str(len(paths)) + ')'
        raise Exception(error_msg)


    coords = dict()
    coords['x'] = x_coords
    coords['y'] = y_coords
    coords['z'] = z_coords

    # create and save individual direction plots
    for display_mode in ['x', 'y', 'z']:
        for i in range(len(paths)):
            if titles == None:
                plot_anat(paths[i], display_mode = display_mode, cut_coords = coords[display_mode], output_file = tmp_dir + '/fig-' + str(i) + '_dir-' + display_mode + '.png')
            else:
                plot_anat(paths[i], display_mode = display_mode, cut_coords = coords[display_mode], title = titles[i], output_file = tmp_dir + '/fig-' + str(i) + '_dir-' + display_mode + '.png')

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
