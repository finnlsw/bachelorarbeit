# -*- coding: utf-8 -*-
"""Photoutils_psf_first_try.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wPzKU-_ERcHV3-yqoG3yUT47HT9oHYIF
"""

pip install photutils

import numpy as np
from matplotlib import pyplot as plt
from astropy.nddata import NDData, StdDevUncertainty
from astropy.table import QTable
from astropy.io import fits
from photutils.datasets import make_test_psf_data, make_noise_image
from photutils.psf import IntegratedGaussianPRF
from photutils.detection import DAOStarFinder
from photutils.psf import PSFPhotometry
from photutils.psf import SourceGrouper
from photutils.background import LocalBackground, MMMBackground
from photutils.background import LocalBackground, MMMBackground
from photutils.psf import IterativePSFPhotometry

path= "/content/drive/MyDrive/ColabNotebooks/data/2023-08-11/lightCor/lightCor_Target_R (Johnson)_10.0s_4.fit"
#path="/content/drive/MyDrive/ColabNotebooks/data/2023-08-23/lightCor/lightCor_30.0_0.fit"
hdul = fits.open(path)
data= hdul[0].data

plt.imshow(np.log(data), origin='lower', cmap='gray')
plt.title('Data')
plt.colorbar()

# look at light curves
def plot_fwhm(ax, y_coordinate, data, title_suffix):
    row_values = data[y_coordinate, :]
    x_coordinates = np.arange(len(row_values))  # Using np.arange for consistency
    max_pixel_value = np.max(row_values)
    half_max = max_pixel_value / 2
    above_half_max_indices = np.where(row_values > half_max)[0]
    x_lower = x_coordinates[above_half_max_indices[0]]
    x_upper = x_coordinates[above_half_max_indices[-1]]
    fwhm = x_upper - x_lower
    ax.plot(x_coordinates, row_values)
    ax.scatter([x_lower, x_upper], [half_max, half_max], color='red', label='Half-Maximum Points')
    ax.set_title(f'Pixel Values vs. x-coordinate at y={y_coordinate}\nFWHM {title_suffix}= {fwhm:.2f} pixels')
    ax.set_xlabel('x-coordinate')
    ax.set_ylabel('Pixel Values')
    ax.legend()

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))
plot_fwhm(axes[0], 1024, data, 'of the brightest star')
plot_fwhm(axes[1], 1575, data, 'of the companion star')

### sigma clipping seems not usefull here
'''
#use sigma clipping
from astropy.stats import sigma_clipped_stats
mean, median, std = sigma_clipped_stats(data, sigma=3.0)
print((mean, median, std))
print(np.mean(data),np.median(data),np.std(data))
print(np.max(data))

clipped_data = np.clip(data, mean - 3 * std,mean + 3*std )
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
im1 = ax[0].imshow(np.log(data), origin='lower', cmap='gray')
ax[0].set_title("Original Data")
fig.colorbar(im1, ax=ax[0])
im2 = ax[1].imshow(np.log(clipped_data), origin='lower', cmap='gray')
ax[1].set_title("Sigma-Clipped Data")
fig.colorbar(im2, ax=ax[1])
plt.tight_layout()
'''

# masking the peak
center_x, center_y = 1000, 1000
radius = 300
x, y = np.meshgrid(np.arange(data.shape[1]), np.arange(data.shape[0]))
mask = (x - center_x)**2 + (y - center_y)**2 <= radius**2

# Apply the mask to the data
data_masked = np.ma.masked_array(data, mask).filled(1) #use 1s instead of 0s to avoid errors
#data_masked = np.ma.masked_array(data, mask)

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
im1 = ax[0].imshow(np.log(data), origin='lower', cmap='gray')
ax[0].set_title("Original Data")
fig.colorbar(im1, ax=ax[0])  # Add colorbar to the original data plot
im2 = ax[1].imshow(np.log(data_masked), origin='lower', cmap='gray')
ax[1].set_title("masked Data")
fig.colorbar(im2, ax=ax[1])  # Add colorbar to the sigma-clipped data plot
plt.tight_layout()

"""# Choose companion stars manually"""

#### Try manual input
from astropy.table import QTable
init_params = QTable()
init_params['x'] = [1037.9, 729.4, 1724.2, 25.3, 1677.1]
init_params['y'] = [1575.4, 1493.8, 1356.0, 584.3, 648.8]

def determine_fwhm(y_coordinates):
    fwhm = []
    for y_coordinate in y_coordinates:
        y_index = int(round(y_coordinate))
        row_values = data[y_index, :]
        x_coordinates = range(len(row_values))
        max_pixel_value = np.max(row_values)
        half_max = max_pixel_value / 2
        above_half_max_indices = np.where(row_values > half_max)[0]
        lower_index = above_half_max_indices[0]
        upper_index = above_half_max_indices[-1]
        x_lower = x_coordinates[lower_index]
        x_upper = x_coordinates[upper_index]
        fwhm.append(x_upper - x_lower)
    return fwhm

fwhm = determine_fwhm(init_params['y'])
print(fwhm)
fwhm1=int(round(np.mean(fwhm)))
print(fwhm1)

from photutils.detection import DAOStarFinder
from photutils.psf import PSFPhotometry
psf_model = IntegratedGaussianPRF(flux=1, sigma=fwhm1  / 2.35) ##2.35 is a conversion factor between FWHM and the standard deviation for a Gaussian distribution.
fit_shape = (7, 7) #This defines the shape of the fitting box used for PSF-fitting. It's a 5x5 pixel box where the PSF fitting is performed around the detected sources.
finder = DAOStarFinder(6.0, 6.0) #thershhold and fwhm
psfphot = PSFPhotometry(psf_model, fit_shape, finder=finder,
                        aperture_radius=3*fwhm1)

noise = make_noise_image(data.shape, mean=0, stddev=1, seed=0)
error = np.abs(noise)
############## how to get error for my picture, bacause i need an error for the psf ????

#with manual input
phot = psfphot(data_masked, error=error, init_params=init_params)

##### auromaticly for all stars dont work (stopped after 12min)
#phot = psfphot(data, error=error)

from photutils.aperture import CircularAperture
resid = psfphot.make_residual_image(data_masked, (25, 25))
aper = CircularAperture(zip(init_params['x'], init_params['y']), r=40)
plt.imshow(resid, origin='lower',cmap="gray")
aper.plot(color='red')
plt.title('Residual Image')
plt.colorbar()
### if fit successfull, there should be no sign of star in the red area, just background

phot['x_fit'].info.format = '.4f'
phot['y_fit'].info.format = '.4f'
phot['flux_fit'].info.format = '.4f'
print(phot[('id', 'x_fit', 'y_fit', 'flux_fit')])

"""# Chose bright star manually"""

init_params2 = QTable()
init_params2['x'] = [994]
init_params2['y'] = [1005]
fwhm2=determine_fwhm(init_params2['y'])
print(fwhm2)

psf_model2 = IntegratedGaussianPRF(flux=1, sigma= fwhm[0] / 2.35) ##2.35 is conversion factor between FWHM and the standard deviation for a Gaussian distribution
fit_shape2 = (2*fwhm2[0]+1, 2*fwhm2[0]+1) #This defines the shape of the fitting box used for PSF-fitting. It's a odd pixel box where the PSF fitting is performed around the detected sources.
finder2 = DAOStarFinder(6.0, fwhm2[0]) #thershhold and fwhm
psfphot2 = PSFPhotometry(psf_model2, fit_shape2, finder=finder2,
                        aperture_radius=3*fwhm2[0])

#with manual input
phot2 = psfphot2(data, error=error, init_params=init_params2)

phot2['x_fit'].info.format = '.4f'
phot2['y_fit'].info.format = '.4f'
phot2['flux_fit'].info.format = '.4f'
print(phot2[('id', 'x_fit', 'y_fit', 'flux_fit')])

from photutils.aperture import CircularAperture
resid2 = psfphot2.make_residual_image(data, (25, 25))
aper2 = CircularAperture(zip(init_params2['x'], init_params2['y']), r=100)
plt.imshow(resid2, origin='lower')
aper2.plot(color='red')
plt.title('Residual Image')
plt.colorbar()

"""# Differential Photometry

"""

def Magnitude(flux):
  return -2.5*np.log10(flux)

magnitude_bright_star=Magnitude(phot2['flux_fit'][0])
magnitudes_faint_stars =[Magnitude(flux) for flux in phot['flux_fit']]

print(f"magnitude_bright_star: {magnitude_bright_star}")
print(f"magnitudes_faint_stars:{magnitudes_faint_stars}")
for i in range (len(magnitudes_faint_stars)):
  print(f'differential magnitudes for companion star {i+1} and bright star: {magnitude_bright_star-magnitudes_faint_stars[i]}')

from google.colab import drive
drive.mount('/content/drive')

