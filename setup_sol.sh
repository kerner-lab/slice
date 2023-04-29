# Load modules
module load mamba/latest
module load cuda-11.7.0-gcc-11.2.0

# Check if slice exists, if not create it and activate it
if conda info --envs | grep -q slice; then echo "slice already exists"; elsemamba env create -f slice_sol.yaml -y; fi
source activate slice
