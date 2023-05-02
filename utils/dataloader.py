import torch
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import geopandas as gpd

path = "data/france/data_10.gpkg"

# Load the data
data = gpd.read_file(path)
data = data.to_crs(epsg=4326)

roi = [
[[-0.3188344314545766, 49.842186963435914],
 [2.0768077353481242, 49.842186963435914],
 [2.0768077353481242, 42.347232877570896],
 [-0.3188344314545766, 42.347232877570896]]
]


d1 = data[data.bounds.maxy < 46]

# Save d1
d1.to_file("data/france/d1.gpkg", driver="GPKG")
