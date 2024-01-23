import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from plotting import show_image

# Function to load and plot FITS images
def open_image(file_path):
    with fits.open(file_path) as hdul:
        image = hdul[0].data  # Get image data
    return image


# df example
'''image = open_image('/home/finn/visual_Studio_Code/data/2024-01-11/stacked/lightCor_HIP75458_df_B_3_5s_B (Johnson)_3.5s_50_images_stacked_0.fit')
fig, ax = plt.subplots(1,1)
show_image(image, ax=ax, fig=fig, percl=99.7, show_colorbar = False, show_ticks=False, cmap = 'gray_r' )

# Remove ticks
ax.set_xticks([])
ax.set_yticks([])
fig.set_size_inches(9, 9)
plt.tight_layout()
plt.show()'''


#mesh comarison
'''file_paths_B = ['/home/finn/visual_Studio_Code/data/2023-09-26/test/lightCor__B (Johnson)_10.0s_0.fit',
                '/home/finn/visual_Studio_Code/data/2023-09-26/test/lightCor__B (Johnson)_10.0s_1.fit',                '/home/finn/visual_Studio_Code/data/2023-09-26/test/lightCor__B (Johnson)_10.0s_2.fit']

file_paths_R = ['/home/finn/visual_Studio_Code/data/2023-09-26/test/lightCor__R (Johnson)_10.0s_0.fit',
                '/home/finn/visual_Studio_Code/data/2023-09-26/test/lightCor__R (Johnson)_10.0s_1.fit',
                '/home/finn/visual_Studio_Code/data/2023-09-26/test/lightCor__R (Johnson)_10.0s_2.fit']

fig, ax = plt.subplots(3, 2, figsize= (30,20) )
fs=15 #fontsize
for i in range(3):
    image_B = open_image(file_paths_B[i])
    image_R = open_image(file_paths_R[i])
    show_image(image_B, ax=ax[i][0], fig=fig, percl=99.6, show_colorbar = False, show_ticks=False)
    show_image(image_R, ax=ax[i][1], fig=fig, percl=99.6, show_colorbar = False, show_ticks=False)
ax[0][0].set_title('B filter', fontsize = fs)
ax[0][1].set_title('R filter', fontsize = fs)
ax[0][0].set_ylabel('0.2 mm', fontsize = fs, rotation=0)
ax[1][0].set_ylabel('0.5 mm', fontsize = fs, rotation=0)
ax[2][0].set_ylabel('1.0 mm', fontsize = fs, rotation=0)


#plt.subplots_adjust(wspace=-0.8, hspace=0.1)
fig.set_size_inches(9, 11)
# Remove ticks
for row in ax:
    for col in row:
        col.tick_params(left=False, bottom=False)
# Prevent y-label from going behind the image
for i in range(3):
    ax[i][0].yaxis.set_label_coords(-0.2, 0.5)
plt.tight_layout()
plt.savefig('/home/finn/Pictures/Different_mesh_sizes.png')'''



'''def determine_fwhm(data, positions,max_value=20):
    valid_positions = []
    fwhm = []
    x_values = [int(value[0]) for value in positions]
    y_values = [int(value[1]) for value in positions]
    for i in range(len(positions)):
        size = 30
        if x_values[i] < size or x_values[i] >= data.shape[1] - size:
            row_values = data[y_values[i], x_values[i] - x_values[i]: x_values[i] + x_values[i]]
        else:
            row_values = data[y_values[i], x_values[i] - size: x_values[i] + size]
        x_coordinates = range(len(row_values))
        row_values_bkg = row_values + np.median(row_values)  # add median as background
        half_max = (np.max(row_values_bkg) / 2)
        above_half_max_indices = np.where(row_values > half_max)[0]
        lower_index = above_half_max_indices[0]
        upper_index = above_half_max_indices[-1]
        x_lower = x_coordinates[lower_index]
        x_upper = x_coordinates[upper_index]
        calculated_fwhm = x_upper - x_lower
        plt.plot(x_coordinates, row_values)
        plt.xlabel("x coordinate [pixel]", fontsize=12)
        plt.ylabel("counts [ADU]", fontsize=12)
        #plt.title("1d profile for HIP100587_focused_B (Johnson)_0.7s_25.09.23")
        if calculated_fwhm <= max_value and calculated_fwhm > 0:
            fwhm.append(calculated_fwhm)
            valid_positions.append(positions[i])
    return valid_positions, fwhm

determine_fwhm(image_list_short[1], pos_br_mean[1])'''


# File paths for the FITS images
file_path_1 = '/home/finn/visual_Studio_Code/data/2023-09-04/LIGHT/HIP_100587-001_30.fit'
file_path_2 = '/home/finn/visual_Studio_Code/data/2023-09-04/stacked_old/lightCor_HIP_100587_B (Johnson)_30.0s_long_short_10_images_stacked_0.fit'
#file_path_3 = '/home/finn/visual_Studio_Code/data/2023-09-25/lightCor/lightCor_HIP100587_B (Johnson)_40.0s_6.fit'
file_list = [file_path_1, file_path_2]

#raw = open_image(file_path_3)
fig, ax = plt.subplots(1,2, figsize=(20,10))
for i in range (len(file_list)):
    image = open_image(file_list[i])
    show_image(image, ax=ax[i], fig=fig, percl= 99.5, fs_colorbar=16, show_ticks=False)
    #ax[i].set_yticks([])
    #ax[i].set_xticks([])

plt.tight_layout()
plt.subplots_adjust(wspace=0.21)
#plt.savefig('/home/finn/Pictures/raw_vs_corr+stacked.png')
plt.show()


#### todo search same image in stacked old, new and with other method (aa)