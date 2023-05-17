import torch
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import sys
import geopandas as gpd
from torch.utils.data import Dataset, DataLoader

class ParcelDataset(Dataset):
    """Parcel dataset
    --------------------------------
    This class is used to load the dataset.
    The data is stored in a folder with the following structure:
    - data
        - france
            - parcels
                - xxxxx.png
                - xxxxx.geojson
                - ...

    The labels is loaded using the `geopandas` library.
    The images are loaded using the `matplotlib.pyplot` module.
    The labels are stored in boolean masks. The masks are stored in a list.
    """
    
    def __init__(self, path):
        """
        Args:
            path (string): Path to the folder containing the dataset.
        """
        self.path = path
        self.data = gpd.read_file(path + "parcel_data.geojson") 
        self.images, self.labels = self._get_image_and_pixel_masks(self.data)
        self.length = len(self.data)
        
    def __len__(self):
        return self.length
    
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
            
        image_path = self.images[idx]
        label = self.labels[idx]
        
        # Handle the case where the idx is list
        if isinstance(image_path, str):
            image_path = [image_path]
                
        all_images = []
        for path in image_path:
            image = cv2.imread(path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            all_images.append(image)
            
        return np.array(all_images), np.array(label, dtype=object)


    def _get_image_and_pixel_masks(self, parcel_data, size=(224, 224)):
        """Convert the polygon masks to pixel masks

        Args:
            size (tuple): Size of the pixel masks HxW; 224x224 by default.

        Returns:
            image_list: List of image paths.
            list: List of pixel masks.
        """
        # Create a black background
        background = np.zeros(size)
        processed_data = {
            'image_paths': [],
            'pixel_masks': []
        }
        
        for _, row in parcel_data.iterrows():
            # Store the image path
            processed_data['image_paths'].append(self.path + row['parcel_id'] + '.png')
            # Read the label list
            label_list = gpd.read_file(self.path + row['parcel_id'] + '.geojson')

            # If the parcel has no labels, Just append the background
            if len(label_list) == 0:
                processed_data['pixel_masks'].append(np.array([background.copy().astype(dtype=bool)]))
                continue
            
            # Get the polygon bounds
            min_lon, min_lat, max_lon, max_lat = row.geometry.bounds
            
            # Get the width and height of the parcel
            height = max_lat - min_lat
            width = max_lon - min_lon

            # Get the pixel width and height
            pixel_height = size[0]/height
            pixel_width = size[1]/width

            pixel_masks = []
            for label in label_list.geometry:
                pixel_mask = background.copy()
                # Iterate over the polygons in the multipolygon
                for polygon in label.geoms:
                    coords = polygon.exterior.coords.xy

                    # Get the pixel coords
                    pixel_coords = []
                    for i in range(len(coords[0])):
                        x = coords[0][i]
                        y = coords[1][i]

                        # Get the pixel x and y
                        pixel_x = (x - min_lon) * pixel_width
                        pixel_y = (max_lat - y) * pixel_height

                        pixel_coords.append([pixel_x, pixel_y])

                    # Convert to int to make it work with cv2
                    pixel_coords = np.array(pixel_coords, dtype=np.int32)
                    # Fill the polygons and append to the pixel mask
                    cv2.fillPoly(pixel_mask, pts=[pixel_coords], color=255)
                pixel_masks.append(pixel_mask.astype(dtype=bool))

            # Append the pixel masks to the list
            processed_data['pixel_masks'].append(np.array(pixel_masks))

        return processed_data['image_paths'], processed_data['pixel_masks']
    

if __name__ == '__main__':
    dataset = ParcelDataset(path='data/france/dataset_chunk/')
    print(len(dataset))