import numpy as np
import os
import nibabel as nib
from PIL import Image
from nibabel.freesurfer.mghformat import MGHImage
from skimage.color import gray2rgb

example_file = '/Applications/freesurfer/subjects/cvs_avg35_inMNI152/mri/brain.mgz'
example_file = '/Applications/freesurfer/subjects/cvs_avg35_inMNI152/mri/aparc+aseg.mgz'
luf_filename = '/Applications/freesurfer/FreeSurferColorLUT.txt'

# lut_filepath = resource_path(os.path.join('data', 'FreeSurferColorLUT.txt'))
#         lut_array = np.genfromtxt(lut_filepath,
#                                   dtype=None,
#                                   usecols=(0, 1, 2, 3, 4, 5),
#                                   names=['id', 'name', 'R', 'G', 'B', 'A'],
#                                   encoding='utf-8')
#
#         # Fill in a few known colors, the rest will be generated if needed
#         # Use the loop to search the id assigned to the region (using filename)
#         region_id = 0
#         color = [1.0, 1.0, 1.0]
#         for line in lut_array:
#             if line[1] == mesh_filename.split('.')[0]:
#                 region_id = line[0]
#                 color = [float(line[2]) / 255.0, float(line[3]) / 255.0, float(line[4]) / 255.0]

def read_lut(lut_filepath):
    lut_array = np.genfromtxt(lut_filepath,
                              dtype=None,
                              usecols=(0, 1, 2, 3, 4, 5),
                              names=['id', 'name', 'R', 'G', 'B', 'A'],
                              encoding='utf-8')

    print(lut_array.shape)
    lut_matrix = np.zeros((lut_array.shape[0],4), int)
    for index, line in enumerate(lut_array):

        lut_matrix[index,0] = line[0]
        lut_matrix[index,1] = line[2]
        lut_matrix[index,2] = line[3]
        lut_matrix[index,3] = line[4]

    return lut_matrix
    # import csv
    # fid = open(filenameColorfile, "r")
    # reader = csv.reader(fid)
    #
    # dictRGB = {}
    # for line in reader:
    #     dictRGB[int(line[0])] = [float(line[2])/255.0,
    #                              float(line[3])/255.0,
    #                              float(line[4])/255.0]
    # fid.close()





lut = read_lut(luf_filename)
img = nib.load(example_file)
print(img)
image_data = img.get_data()
color_image = np.zeros((image_data.shape[0],image_data.shape[1],image_data.shape[2],3), int)
unique_labels = np.unique(image_data)
for ul in unique_labels:
    indices = zip(*np.where(image_data == ul))
    color = lut[np.where(lut[:,0] == ul),1:4]
    for i,j,k in indices:
        color_image[i,j,k,:] = color

print(color_image.shape)

if not os.path.exists(os.path.join('.', 'mgh2png')):
    os.makedirs(os.path.join('.', 'mgh2png'))

if not os.path.exists(os.path.join('.', 'mgh2png', 'axial')):
    os.makedirs(os.path.join('.', 'mgh2png', 'axial'))

if not os.path.exists(os.path.join('.', 'mgh2png', 'coronal')):
    os.makedirs(os.path.join('.', 'mgh2png', 'coronal'))

if not os.path.exists(os.path.join('.', 'mgh2png', 'sagital')):
    os.makedirs(os.path.join('.', 'mgh2png', 'sagital'))

for s in range(0,image_data.shape[0]):
    im = Image.fromarray(color_image[s,:,:,:].reshape((color_image.shape[1],color_image.shape[2],3)).astype('uint8'))
    im = im.convert('RGB')
    im.save(os.path.join('.', 'mgh2png', 'sagital','sagital_'+str(s)+'.png'))
    print(s)

for s in range(0,image_data.shape[1]):
    im = Image.fromarray(color_image[:,s,:,:].reshape((color_image.shape[0],color_image.shape[2],3)).astype('uint8'))
    im = im.convert('RGB')
    im.save(os.path.join('.', 'mgh2png', 'coronal','coronal_'+str(s)+'.png'))
    print(s)
#
for s in range(0,color_image.shape[2]):
    im = Image.fromarray(color_image[:,:,s,:].reshape((color_image.shape[0],color_image.shape[1],3)).astype('uint8'))
    im = im.convert('RGB')
    im.save(os.path.join('.', 'mgh2png', 'axial','axial_'+str(s)+'.png'))
    print(s)

# f = open('test.rawl', 'w')
# slice.tofile(f)
# f.close()
