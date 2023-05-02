from pyunpack import Archive
import geopandas as gpd

Archive('france_data.7z').extractall("./france/")

path = "./france/PARCELLES_GRAPHIQUES.gpkg"

# Load the data
data = gpd.read_file(path)

# Split the data into 30 chunks and save them
# to the data/france/ directory
data_split = np.array_split(data, 30)
for i in range(len(data_split)):
    data_split[i].to_file(f"data/france/data_{i}.gpkg", driver="GPKG")