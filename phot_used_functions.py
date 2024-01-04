import numpy as np
from scipy.spatial.distance import cdist
from scipy import signal
import cv2
from astropy.stats import sigma_clipped_stats, mad_std
from astropy.table import Table
from photutils import CircularAperture, CircularAnnulus, aperture_photometry, ApertureStats
import glob
import os
from datetime import datetime
from astropy.io import fits
import astroalign as aa

def filter_sources(positions, sources, min_separation=50.0, min_edge_distance=50.0):
    distances = cdist(positions, positions)
    edge_distance_x = np.minimum(positions[:, 0], 2048 - positions[:, 0])
    edge_distance_y = np.minimum(positions[:, 1], 2048 - positions[:, 1])
    keep_sources = np.ones(len(positions), dtype=bool)
    for i in range(len(positions)):
        if keep_sources[i]:
            for j in range(i + 1, len(positions)):
                if distances[i, j] < min_separation:
                    flux_i = sources['flux'][i]
                    flux_j = sources['flux'][j]
                    dist_ij = distances[i, j]
                    # Keep the brighter source if it's within the minimum separation
                    if flux_j > flux_i and dist_ij < min_separation:
                        keep_sources[i] = False
                    elif flux_i > flux_j and dist_ij < min_separation:
                        keep_sources[j] = False
            if edge_distance_x[i] < min_edge_distance or edge_distance_y[i] < min_edge_distance:
                keep_sources[i] = False
    filtered_positions = positions[keep_sources]
    filtered_sources = sources[keep_sources]
    return filtered_positions, filtered_sources




def determine_distance(data, positions,max_value=30):
    valid_positions = []
    distance_list = []
    x_values = [int(value[0]) for value in positions]
    y_values = [int(value[1]) for value in positions]

    #fig, ax = plt.subplots(len(positions), 1, figsize=(8, 6 * len(positions)))
    for i in range(len(positions)):
        size = 40
        if x_values[i] < size or x_values[i] >= data.shape[1] - size:
            row_values = data[y_values[i], x_values[i] - x_values[i]: x_values[i] + x_values[i]]
        else:
            row_values = data[y_values[i], x_values[i] - size: x_values[i] + size]
        x_coordinates = range(len(row_values))
        row_values_bkg = row_values + np.median(row_values)  # add median as background
        peaks, _ = signal.find_peaks(row_values, distance=5)
        peak_values = [(row_values[peak], peak) for peak in peaks]
        sorted_peak_values = sorted(peak_values, reverse=True)
        top_two_values = sorted_peak_values[:2] #(y1,x1),(y2,x2)
        distance = np.abs(top_two_values[0][1]- top_two_values[1][1])
        #ax[i].plot(x_coordinates, row_values)
        #ax[i].scatter(top_two_values[0][1], top_two_values[0][0])
        #ax[i].scatter(top_two_values[1][1], top_two_values[1][0])
        if distance <= max_value and distance > 0:
            distance_list.append(distance)
            valid_positions.append(positions[i])

    return distance_list, valid_positions


def determine_shift(imageList, referenceImage = None, wanted_index = None):
    print('Number of images to process:', len(imageList))
    shifts = []
    warp_mode = cv2.MOTION_TRANSLATION
    #warp_mode = cv2.MOTION_HOMOGRAPHY
    warp_matrix = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 1000, 1e-5) # default was 1000, 1e-5

    if referenceImage is None:
        if wanted_index is None:
          wanted_index = len(imageList)//2
        print('we use image: ',wanted_index,"from given list as reference image")
        reference_image = imageList[wanted_index].astype(np.float32)
    else:
        reference_image = referenceImage.astype(np.float32)
    
    for i, image in enumerate(imageList):
      if i == wanted_index: 
        shifts.append((0,0)) #no shift for the reference image relativ to itself
      else:
        image = image.astype(np.float32)
        _, warp_matrix = cv2.findTransformECC(reference_image, image, warp_matrix, warp_mode, criteria)
        shift_x, shift_y = warp_matrix[0, 2], warp_matrix[1, 2]
        shifts.append((shift_x, shift_y))

    return shifts


def determine_shift_aa(imageList, referenceImage = None, wanted_index = None):
    print('Number of images to process:', len(imageList))
    shifts = []

    if referenceImage is None:
        if wanted_index is None:
          wanted_index = len(imageList)//2
        print('we use image: ',wanted_index,"from given list as reference image")
        reference_image = imageList[wanted_index].astype(np.float32)
    else:
        reference_image = referenceImage.astype(np.float32)
    
    for i, image in enumerate(imageList):
      if i == wanted_index: 
        shifts.append((0,0)) #no shift for the reference image relativ to itself
      else:
        image = image.astype(np.float32)
        #_, warp_matrix = cv2.findTransformECC(reference_image, image, warp_matrix, warp_mode, criteria)
        transf, (source_list, target_list) = aa.find_transform(image, referenceImage)
        print(transf)
        shift_x, shift_y = transf[0, 2], transf[1, 2]
        shifts.append((shift_x, shift_y))

    return shifts

# function to determine individual radii
def determine_fwhm(data, positions,max_value=20):
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
        if calculated_fwhm <= max_value and calculated_fwhm > 0:
            fwhm.append(calculated_fwhm)
            valid_positions.append(positions[i])
    return valid_positions, fwhm



def determine_magnitudes(image, positions, star_radius, exptime):
  #for bright star
  if len(positions) == 1:
    aperture = CircularAperture(positions, r=star_radius)
    annulus_aperture = CircularAnnulus(positions, r_in=star_radius+15, r_out=star_radius+45)
    aperture.plot(color='red', lw=1.0, alpha=0.5);
    annulus_aperture.plot(color="blue", lw=1.0, alpha=0.5);
    phot_table = aperture_photometry(image, aperture, method='subpixel', subpixels=5)
    aperstats = ApertureStats(image, annulus_aperture)
    bkg = aperstats.median
    aperture_area = aperture.area_overlap(image)
    total_bkg = bkg * aperture_area
    phot_table['total_bkg'] = total_bkg
    for line in phot_table:
      magnitudes = - (2.5*np.log10(abs(line[3]-line[4])/exptime)) #here single value
    
  else:
    apertures = [CircularAperture(position, r=star_radius) for position in positions]
    annulus_apertures = [CircularAnnulus(position,r_in=star_radius+5, r_out=star_radius+15) for position in positions]
    for aperture in apertures:
        aperture.plot(color="red", lw=1.0, alpha=0.5)
    for anulus in annulus_apertures:
        anulus.plot(color="blue", lw=1.0, alpha=0.5)
    phot_table_faint = Table(names=('id', 'xcenter', 'ycenter', 'aperture_sum', 'total_bkg'), dtype=('int', 'float', 'float', 'float', 'float'))
    for j in range(len(apertures)):
        aperstats = ApertureStats(image, annulus_apertures[j])
        bkg = aperstats.median
        aperture_area = apertures[j].area_overlap(image)
        total_bkg = bkg * aperture_area
        phot_table = aperture_photometry(image, apertures[j])
        phot_table['total_bkg'] = total_bkg
        phot_table_faint.add_row([j, phot_table['xcenter'][0], phot_table['ycenter'][0], phot_table['aperture_sum'][0], phot_table['total_bkg'][0]])
    magnitudes=[]
    for row in phot_table_faint:
        magnitude =  - (2.5 * np.log10(abs(row['aperture_sum'] - row['total_bkg']) / exptime))
        magnitudes.append(magnitude) #magnitudes here list
  return magnitudes 

def import_images(input_path):
    image_list, header_list, titles = [], [], []
    file_names = glob.glob(os.path.join(input_path[:-6] + '*.fit')) 
    files_list = [file for file in file_names]
    files_list.sort(key=lambda file_path: datetime.strptime(fits.getheader(file_path).get('DATE-OBS', ''), '%Y-%m-%dT%H:%M:%S')) #sort by time
    for file in files_list:
        hdul = fits.open(file)
        image_list.append(hdul[0].data)
        header_list.append(hdul[0].header)
        titles.append(os.path.basename(file)[:-4]) # Extracting filename without extension
        exptime = header_list[0]["EXPTIME"] 
        hdul.close()
    
    return image_list, header_list, titles, exptime