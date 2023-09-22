import os
from astropy.io import fits
from plotting import show_image
from matplotlib import pyplot as plt

Path = os.path.join('/home/finn/visual_Studio_Code/data/2023-09-11/lightCor/lightCor_HIP100587_focused_B (Johnson)_1.0s_6.fit')
hdul = fits.open(Path)
image=hdul[0].data
header=hdul[0].header

show_image(image)





'''
def test(add):
    plt.savefig(f"date{add}")

def main():
    test(3)


if __name__ == '__main__':
    main()
'''