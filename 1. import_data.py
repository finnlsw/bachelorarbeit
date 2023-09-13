import os
from pathlib import Path
import ccdproc as ccdp
def import_data(data):
    #data directories
    data_dir = data
    snapshot_dir = os.path.join(data_dir, "SNAPSHOT")
    bias_dir = os.path.join(data_dir, "BIAS")
    dark_dir = os.path.join(data_dir, "DARK")
    flat_dir = os.path.join(data_dir, "FLAT")
    light_dir = os.path.join(data_dir, "LIGHT")

    # setting path for just masters and corrected
    master_dir = Path(data_dir, 'Masters')
    master_dir.mkdir(exist_ok=True)
    dark_cor_dir = Path(data_dir, 'dark_cor')
    dark_cor_dir.mkdir(exist_ok=True)
    flat_cor_dir = Path(data_dir, 'flat_cor')
    flat_cor_dir.mkdir(exist_ok=True)
    light_cor_dir = Path(data_dir, 'light_cor')
    light_cor_dir.mkdir(exist_ok=True)

    #creating picture dictonaries
    flat_collection= ccdp.ImageFileCollection(flat_dir)
    dark_collection= ccdp.ImageFileCollection(dark_dir)
    bias_collection= ccdp.ImageFileCollection(bias_dir)
    snapshot_collection= ccdp.ImageFileCollection(snapshot_dir)
    light_collection= ccdp.ImageFileCollection(light_dir)

#test
import_data("/home/fmahnken/PycharmProjects/data/2023-08-11")