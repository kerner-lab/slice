import torch
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import geopandas as gpd

path = "data/france/sampled.gpkg"

# Load the data
raw_data = gpd.read_file(path)