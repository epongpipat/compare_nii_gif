from setuptools import setup

setup(name='compare_nii_gif',
      version='0.1',
      description='Create a gif that compares nifti files in axial, sagittal, and coronal views',
      url='',
      author='Ekarin E. Pongpipat',
      author_email='epongpipat@gmail.com',
      license='MIT',
      packages=['compare_nii_gif'],
      entry_points={'console_scripts': [
          'compare_nii_gif = compare_nii_gif.__main__:main']},
      zip_safe=False)
