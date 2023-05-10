# Overlay all the images in output folder on top of one another with different colors
# to see the overlap of the images

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

# Get all the images in the output folder
path = 'output_images/image_3000304/'
all_files = sorted(glob.glob(os.path.join(path, "*.png")))

# Create a new image with the same size as the first image
first_image = Image.open(all_files[0])
width, height = first_image.size
new_image = Image.new('RGB', (width, height))


# Images are one channel, assign a random color to each image
new_image = np.array(new_image)
for file in all_files[1:]:
    image = Image.open(file)
    image = image.convert('RGB')
    # Create a random color
    color = np.random.randint(0, 255, 3)
    # Assign the color to the image
    image = np.array(image)
    # Find all the pixels where the value = 255 and convert them to the random color
    idx = np.where(image != [0, 0, 0])

    # Assign these indices in the new_image to the random color
    new_image[idx[0], idx[1], :] = color


plt.imsave('output_images/image_3000304/overlay.png', new_image)
