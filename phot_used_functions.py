import numpy as np
from scipy.spatial.distance import cdist
from scipy import signal
import cv2

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

def determine_shift(imageList, referenceImage = None, middle_index = None):
    print('Number of images to process:', len(imageList))
    shifts = []
    warp_mode = cv2.MOTION_TRANSLATION
    #warp_mode = cv2.MOTION_HOMOGRAPHY
    warp_matrix = np.eye(2, 3, dtype=np.float32)
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 1000, 1e-5) # default was 1000, 1e-5

    if referenceImage is None:
        middle_index = len(imageList)//2
        print('middle index is: ',middle_index)
        reference_image = imageList[middle_index].astype(np.float32)
    else:
        reference_image = referenceImage.astype(np.float32)
    
    for i, image in enumerate(imageList):
      if middle_index is None: 
        image = image.astype(np.float32)
        _, warp_matrix = cv2.findTransformECC(reference_image, image, warp_matrix, warp_mode, criteria)
        shift_x, shift_y = warp_matrix[0, 2], warp_matrix[1, 2]
        shifts.append((shift_x, shift_y))
      else:
        if i == middle_index:
            shifts.append((0, 0))  # No shift for the reference image
        else:
          image = image.astype(np.float32)
          _, warp_matrix = cv2.findTransformECC(reference_image, image, warp_matrix, warp_mode, criteria)
          shift_x, shift_y = warp_matrix[0, 2], warp_matrix[1, 2]
          shifts.append((shift_x, shift_y))

    return shifts