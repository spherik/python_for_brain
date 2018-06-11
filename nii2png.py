import numpy
import os
import nibabel as nib
from PIL import Image


example_file = 'sub-mni_T1w.nii'
img = nib.load(example_file)
image_data = img.get_data()
print(image_data.shape)

if not os.path.exists(os.path.join('.', 'nii2png')):
    os.makedirs(os.path.join('.', 'nii2png'))

if not os.path.exists(os.path.join('.', 'nii2png', 'axial')):
    os.makedirs(os.path.join('.', 'nii2png', 'axial'))

if not os.path.exists(os.path.join('.', 'nii2png', 'coronal')):
    os.makedirs(os.path.join('.', 'nii2png', 'coronal'))

if not os.path.exists(os.path.join('.', 'nii2png', 'sagital')):
    os.makedirs(os.path.join('.', 'nii2png', 'sagital'))

for s in range(0,image_data.shape[0]):
    im = Image.fromarray(image_data[s,:,:])
    im = im.convert('RGB')
    im.save(os.path.join('.', 'nii2png', 'sagital','sagital_'+str(s)+'.png'))
    print(s)

for s in range(0,image_data.shape[1]):
    im = Image.fromarray(image_data[:,s,:])
    im = im.convert('RGB')
    im.save(os.path.join('.', 'nii2png', 'coronal','coronal_'+str(s)+'.png'))
    print(s)

for s in range(0,image_data.shape[2]):
    im = Image.fromarray(image_data[:,:,s].transpose())
    im = im.convert('RGB')
    im.save(os.path.join('.', 'nii2png', 'axial','axial_'+str(s)+'.png'))
    print(s)

# f = open('test.rawl', 'w')
# slice.tofile(f)
# f.close()
