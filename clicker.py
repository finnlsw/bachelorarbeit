import os
from astropy.io import fits
from plotting import show_image
from saving import save_image
from matplotlib import pyplot as plt



Path = os.path.join('/home/finn/visual_Studio_Code/data/2023-10-01/stacked/lightCor_HIP75458_mesh_B (Johnson)_15.0s_mesh_10_images_stacked_0.fit')
hdul = fits.open(Path)
image=hdul[0].data
header=hdul[0].header
date = hdul[0].header["DATE-OBS"][:10]

'''
fig,ax = plt.subplots(1,1,figsize=(10,10))
ax.set_title(f"{date}_{os.path.splitext(Path)[0][63:]}")
show_image(image, fig=fig, ax=ax)
plt.show()
'''


clicked_positions = []

def onclick(event):
    if event.button == 1:  # Check if the left mouse button is clicked (button value 1)
        x = int(event.xdata)
        y = int(event.ydata)
        clicked_positions.append((x, y))
        print(f"Clicked at pixel position: x={x}, y={y}")

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.set_title(f"{date}_{os.path.splitext(Path)[0][63:]}")
show_image(image, fig=fig, ax=ax)
fig.canvas.mpl_connect('button_press_event', onclick)  # Connect the onclick function to mouse click events

plt.subplots_adjust(left=0, bottom=0, right=0.7, top=1) #zoom in
plt.show()

# for defocused
zoom_removed = [clicked_positions[i] for i in range(len(clicked_positions)) if i % 2 == 1]
#print("positions_faint = ", zoom_removed)

# for mesh
print("bright_positions=", clicked_positions[1:]) #remove first entry (zooming)

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