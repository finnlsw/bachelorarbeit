import numpy as np
import matplotlib.pyplot as plt
from astropy import visualization as aviz
from astropy.nddata.blocks import block_reduce


def show_image(image,
               percl=99.5, percu=None, is_mask=False,
               figsize=(10, 10),
               cmap='gray', fs_colorbar=15, log=False, clip=True,
               show_colorbar=True, show_ticks=True,
               fig=None, ax=None, input_ratio=None):
    if percu is None: # determine percentile range of the stretch
        percu = percl
        percl = 100 - percl
    if (fig is None and ax is not None) or (fig is not None and ax is None):
        raise ValueError('Must provide both "fig" and "ax" '
                         'if you provide one of them')
    elif fig is None and ax is None:
        if figsize is not None:
            image_aspect_ratio = image.shape[0] / image.shape[1]
            figsize = (max(figsize) * image_aspect_ratio, max(figsize))
        fig, ax = plt.subplots(1, 1, figsize=figsize)
    fig_size_pix = fig.get_size_inches() * fig.dpi
    ratio = (image.shape // fig_size_pix).max()
    if ratio < 1:
        ratio = 1
    ratio = input_ratio or ratio
    reduced_data = block_reduce(image, ratio)
    if not is_mask:
         reduced_data = reduced_data / ratio**2
    extent = [0, image.shape[1], 0, image.shape[0]]
    if log:
        stretch = aviz.LogStretch()
    else:
        stretch = aviz.LinearStretch()
    norm = aviz.ImageNormalize(reduced_data,
                               interval=aviz.AsymmetricPercentileInterval(percl, percu),
                               stretch=stretch, clip=clip)
    if is_mask:
        reduced_data = reduced_data > 0
        scale_args = dict(vmin=0, vmax=1)
    else:
        scale_args = dict(norm=norm)
    im = ax.imshow(reduced_data, origin='lower',
                   cmap=cmap, extent=extent, aspect='equal', **scale_args)
    if show_colorbar:
        #fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04 )
        cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        # Set the size of the colorbar tick labels
        cbar.ax.tick_params(labelsize=fs_colorbar) 
    if not show_ticks:
        ax.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)