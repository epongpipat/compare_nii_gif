# compare_nii_gif

Create a gif that compares nifti files in axial, sagittal, and coronal views.

## Install

```
pip install git+https://github.com/epongpipat/compare_nii_gif.git
```

## Usage
```
compare_nii_gif -i <in_path1> <in_path2> -o <out_path>
```

## Example

An example comparing my raw versus brain extracted T1w image.

```
compare_nii_gif -i T1w_raw.nii.gz T1w_bet.nii.gz -o example.gif --titles raw bet
```

![](example.gif)

We can also manually adjust the slices.

```
compare_nii_gif -i T1w_raw.nii.gz T1w_bet.nii.gz -o example.gif --titles raw bet -z -80 -70 -60 -50 -40 -30 -20 -10 0 10 20 30 40
```

![](example_adj_z.gif)
