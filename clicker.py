import os
from astropy.io import fits
from plotting import show_image
from saving import save_image
from matplotlib import pyplot 
import matplotlib.pyplot as plt
import pyperclip

Path = '/home/finn/visual_Studio_Code/data/2024-01-10/image_for_CMD/lightCor_HIP102488_ref_30s_R (Johnson)_30.0s_10_images_stacked_0.fit'

series = 'ms' #type in df or ms for choosing every second clicked position or every pos execpt the 1. 

hdul = fits.open(Path)
image=hdul[0].data
header=hdul[0].header
date = hdul[0].header["DATE-OBS"][:10]

clicked_positions = []
def onclick(event):
    if event.button == 1:
        x = round(event.xdata,1)
        y = round(event.ydata,1)
        clicked_positions.append((x, y))
        print(f"Clicked at pixel position: x={x}, y={y}")

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.set_title(f"{date}_{os.path.splitext(Path)[0][63:]}")
show_image(image, fig=fig, ax=ax, percl=99.8)
fig.canvas.mpl_connect('button_press_event', onclick)  # Connect the onclick function to mouse click events

plt.subplots_adjust(left=0, bottom=0, right=0.7, top=1)
plt.show()

if series == 'df':
    zoom_removed = [clicked_positions[i] for i in range(len(clicked_positions)) if i % 2 == 1]
    print("positions_faint = ", zoom_removed, " (already copied to clipboard)")
    pyperclip.copy(str(zoom_removed)) # this copies list to clipboard

if series == 'ms' :
    print("clicked positions=", clicked_positions[1:], " (already copied to clipboard)") #remove first entry (zooming)
    pyperclip.copy(str(clicked_positions[1:]))
