This code can be use to obtain differential magnitudes with three different techniques. Use the following steps:

1. Put your fits files in the folders: "BIAS", "DARK", "FLAT" and "LIGHT"
2. Use data_correction.py to correct your lightframes
3. Use stacking_run.py to stack your corrected images
4. Plate solve your stacked images with astrometry.py
5. Do the analyis of the images with Analysis_ls.py, Analyis_df or Analysis, depending on the observational strategy
6. Plot time series or colour-magnitude diagrams with TS_and_CMD if wanted
