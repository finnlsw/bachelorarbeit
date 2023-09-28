import os
from astropy.io import fits
from plotting import show_image
from saving import save_image
from matplotlib import pyplot as plt


'''
Path = os.path.join('/home/finn/visual_Studio_Code/data/2023-09-11/lightCor/lightCor_HIP100587_focused_B (Johnson)_1.0s_6.fit')
hdul = fits.open(Path)
image=hdul[0].data
header=hdul[0].header

#testpath= '/home/finn/visual_Studio_Code/data/2023-09-11/testtest'
show_image(image)
plt.show()
'''


folder_path = '/home/finn/visual_Studio_Code/data/2023-09-25/stacked/'

# Get a list of FITS files in the folder
fits_files = [file for file in os.listdir(folder_path) if file.endswith('.fit')]
imagelist=[]

# Plot the Raw and Corrected images in the grid
for i, fits_file in enumerate(fits_files):
    fits_path = os.path.join(folder_path, fits_file)
    hdul = fits.open(fits_path)
    image = hdul[0].data
    imagelist.append(image)


for i in range (1,len(imagelist),2):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    show_image(imagelist[i-1], ax=ax1, fig=fig)
    ax1.set_title(f'image {i-1} out of {len(imagelist)}')
    show_image(imagelist[i], ax=ax2, fig=fig)
    ax2.set_title(f'image {i} out of {len(imagelist)}')
    plt.show()


'''
folder_path = '/home/finn/visual_Studio_Code/data/2023-09-11/lightCor/'

# Get a list of FITS files in the folder
fits_files = [file for file in os.listdir(folder_path) if file.endswith('.fit')]
imagelist = []

# Plot the Raw and Corrected images in pairs
for i in range(0, len(fits_files), 2):
    # Construct the full path to the FITS files
    raw_fits_path = os.path.join(folder_path, fits_files[i])
    corrected_fits_path = os.path.join(folder_path, fits_files[i + 1])

    # Open the FITS files and read the image data
    raw_hdul = fits.open(raw_fits_path)
    corrected_hdul = fits.open(corrected_fits_path)

    raw_image = raw_hdul[0].data
    corrected_image = corrected_hdul[0].data

    # Plot the images in pairs
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    ax1.imshow(raw_image, cmap='gray')
    ax1.set_title('Raw Image')
    ax2.imshow(corrected_image, cmap='gray')
    ax2.set_title('Corrected Image')
    plt.show()
    
    # Close the FITS files
    raw_hdul.close()
    corrected_hdul.close()
'''





'''
def test(add):
    plt.savefig(f"date{add}")

def main():
    test(3)


if __name__ == '__main__':
    main()
'''