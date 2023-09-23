# -*- coding: utf-8 -*-
"""firstTryAstroPhot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bVdMlH53ekl26gkw4hFfk1Unxoumc9Mi
"""


# Commented out IPython magic to ensure Python compatibility.
import os
import astrophot as ap
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from time import time
from astropy.nddata.blocks import block_reduce
from astropy import visualization as aviz
from plotting import show_image
# %matplotlib inline



#stacked short exptime
Path = os.path.join('/content/drive/MyDrive/ColabNotebooks/data/2023-09-04/stackedImages/stackedImage_HIP_100587_0.5')
hdul = fits.open(Path)
target_data = np.array(hdul[0].data,dtype=np.float64)

#combined and masked image
Path2 = os.path.join('/content/drive/MyDrive/ColabNotebooks/data/2023-09-04/stackedImages/stackedImage_HIP_100587_0')
hdul2 = fits.open(Path2)
target_data2 = np.array(hdul2[0].data, dtype=np.float64)



# Create a target object with the calculated variance
target = ap.image.Target_Image(
    data=target_data,
    pixelscale=0.66,
    zeropoint = 25,
    variance = np.ones(target_data.shape)/1e3,
    #mask=mask
)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
show_image(target_data, ax=ax1, fig=fig)
show_image(target_data2, ax=ax2, fig=fig)

live_psf_model = ap.models.AstroPhot_Model(
  name = "psf",
  model_type = "moffat star model",
  target = target,
  window = [[0,2048],[0,2048]],
  parameters = {
    "n": 2., # controls the power-law index of the wings of the PSF. A value of 2 typically corresponds to a Gaussian PSF
    #"Rd": 3
    "center": {"value": [1024,1024], "locked":True},
    "I0": {"value": 1., "locked":True},
  },
  #psf_mode = "full",
)
live_psf_model.initialize()

### takes a while ca 1-2min
#result = ap.fit.lm(live_psf_model, verbose=1).fit()
result = ap.fit.LM(live_psf_model, verbose = 1).fit()
print("Fit message:",result.message)

print(f"min chi2 value is: {result.res_loss()}")

  # Update parameter uncertainties
result.update_uncertainty()

# Extract multivariate Gaussian of uncertainties
mu = result.res()
cov = result.covariance_matrix
print(mu)
print(cov)

live_psf_model.initialize()
# Plotting the initial parameters and residuals
fig, ax = plt.subplots(1, 3, figsize = (22,6))

ap.plots.target_image(fig, ax[0], target)
ax[0].set_title("target")
ap.plots.model_image(fig, ax[1], live_psf_model)
ax[1].set_title("model")
ap.plots.residual_image(fig, ax[2], live_psf_model) #should look random and near zero
ax[2].set_title("residuals")
plt.show()







# first a psf is needed, this is stored with the target object
# Here we simply construct a gaussian PSF image that is 31 pixels across
# Note the PSF must always be odd in its dimensions
xx, yy = np.meshgrid(np.linspace(-5,5,301), np.linspace(-5,5,301))
PSF = np.exp(-(xx**2 + yy**2)/0.8**2)
PSF /= np.sum(PSF)
target = ap.image.Target_Image(
    data = target_data,
    pixelscale = 0.262,
    zeropoint = 22.5,
    psf = PSF,
)

model_nopsf = ap.models.AstroPhot_Model(
    name = "model without psf",
    model_type = "sersic galaxy model",
    target = target,
    parameters = {"center": [250,250], "q": 0.6, "PA": 60*np.pi/180, "n": 2, "Re": 10, "Ie": 1},
    psf_mode = "none", # no PSF convolution will be done
)
model_psf = ap.models.AstroPhot_Model(
    name = "model with psf",
    model_type = "sersic galaxy model",
    target = target,
    parameters = {"center": [250,250], "q": 0.6, "PA": 60*np.pi/180, "n": 2, "Re": 10, "Ie": 1},
    psf_mode = "full", # now the full window will be PSF convolved
)

PSF2 = np.exp(-(xx**2 + yy**2)/0.4**2)
PSF2[:,148:153] += 0.01
PSF2[148:153,:] += 0.01
PSF2 /= np.sum(PSF2)
model_mask = torch.zeros_like(target.data)
model_mask[100:150,400:450] = 1
model_selfpsf = ap.models.AstroPhot_Model(
    name = "model with self psf",
    model_type = "sersic galaxy model",
    target = target,
    parameters = {"center": [250,250], "q": 0.6, "PA": 60*np.pi/180, "n": 4, "Re": 10, "Ie": 1},
    psf_mode = "full",
    psf = PSF2, # Now this model has its own PSF, instead of using the target psf
    mask = model_mask, # Now this model has its own mask, *as well as* the target mask
)
print("psf mode: ", model_psf.psf_mode)

# With a convolved sersic the center is much more smoothed out
fig, ax = plt.subplots(1,3,figsize = (15,4))
ap.plots.model_image(fig, ax[0], model_nopsf)
ax[0].set_title("No PSF convolution")
ap.plots.model_image(fig, ax[1], model_psf)
ax[1].set_title("With PSF convolution")
ap.plots.model_image(fig, ax[2], model_selfpsf)
ax[2].set_title("With model PSF different than target")
plt.show()
# the warning below is just because the model mask values are zero and the plot is in log scale

model3 = ap.models.AstroPhot_Model(
    name = "model with target",
    model_type = "sersic galaxy model",
    target = target,
    window = [[850, 1150],[850, 1150]],
)

model3.initialize()

# We can plot the "model window" to show us what part of the image will be analyzed by that model
fig6, ax6 = plt.subplots(1,2, figsize = (16,8))
ap.plots.target_image(fig6, ax6[0], model3.target)
ap.plots.model_window(fig6, ax6[0], model3)
ap.plots.model_image(fig6, ax6[1], model3)

result = ap.fit.LM(model3, verbose = 1).fit()
print("Fit message:",result.message)

fig5, ax5 = plt.subplots(1, 2, figsize = (16,6))
ap.plots.model_image(fig5, ax5[0], model3)
ap.plots.residual_image(fig5, ax5[1], model3)
plt.show()

#fig10, ax10 = plt.subplots(figsize = (8,8))
ap.plots?
#galaxy_light_profile(fig10, ax10, model3)
#ap.plots.radial_median_profile(fig10, ax10, model3)
#plt.show()

from scipy.special import jv
xx, yy = np.meshgrid(np.linspace(-150,150,301), np.linspace(-150,150,301))
x = np.sqrt(xx**2 + yy**2)/5 +1e-6
PSF = (2*jv(1, x)/x)**2 + 1e-4 # the PSF can be any image, here we construct an airy disk
target = ap.image.Target_Image(data = target_data, pixelscale = 0.261, psf = PSF) # the target image holds the PSF for itself

M = ap.models.AstroPhot_Model(name = "psf star", model_type = "psf star model", target = target, parameters = {"center": [300,300], "flux": 1})
print(M.parameter_order)
print(tuple(P.units for P in M.parameters))
M.initialize()

fig, ax = plt.subplots(1,2, figsize = (14,6))
ap.plots.model_image(fig, ax[0], M)
x = np.linspace(-149,49,99)/5 + 1e-6
ax[1].plot(x, np.log10((2*jv(1, x)/x)**2))
plt.show()

import os
import numpy as np
from astropy.io import fits
import astrophot as ap
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

# Load your target image data
Path = os.path.join('/content/drive/MyDrive/ColabNotebooks/data/2023-08-11/lightCor/lightCor_1.0_1.fit')
hdul = fits.open(Path)
target_data = np.array(hdul[0].data, dtype=np.float64)

# Calculate variance and ensure it's not too small
variance = target_data + 1e-6
variance = np.maximum(variance, 1e-6)

# Create a target object with the calculated variance
target = ap.image.Target_Image(
    data=target_data,
    pixelscale=0.262,
    variance=variance,
)

# Define the window boundaries
x_min, x_max = 850, 1150
y_min, y_max = 850, 1150

# Create the meshgrid within the window
xx, yy = np.meshgrid(np.arange(x_min, x_max + 1), np.arange(y_min, y_max + 1))

# Create the PSF pattern using multivariate normal distribution
amplitude = 1.0
sigma = 5.0
psf_pattern = multivariate_normal(mean=[(x_max - x_min) / 2, (y_max - y_min) / 2], cov=[[sigma, 0], [0, sigma]])
PSF = psf_pattern.pdf(np.stack((xx, yy), axis=-1)) * amplitude

# Create the PSF target image
psf_target = ap.image.Target_Image(
    data=PSF,
    pixelscale=0.262,
    variance= 1e-6,
)

# Create the AstroPhot_Model
M = ap.models.AstroPhot_Model(
    name="psf star",
    model_type="psf star model",
    target=psf_target,
    parameters={"center": [(x_max - x_min) / 2, (y_max - y_min) / 2], "flux": 1},
)
M.initialize()

# Create a figure to show the results
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Plot the model image
ap.plots.model_image(fig, ax[0], M)
ax[0].set_title('Model Image')

# Plot the original PSF pattern
ax[1].imshow(PSF, cmap='viridis', extent=(x_min, x_max, y_min, y_max))
ax[1].set_title('Original PSF Pattern')

plt.tight_layout()
plt.show()

pip install git+https://github.com/mfouesneau/ezpadova

pip install photutils