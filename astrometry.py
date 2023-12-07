import glob
import os
from astroquery.astrometry_net import AstrometryNet
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u

'''
def plate_solve(path):
    input_files = glob.glob(os.path.join(path, '*.fit')) 
    ast = AstrometryNet()
    ast.api_key = 'fpcodtulvgmteoid'  # XXXXXXXXXXXXXXXXX change personal api key at end for other persons XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    for i, file in enumerate(input_files):
        try:
            wcs_header = ast.solve_from_image(file) #determines and upload source list to plate solve 
            if wcs_header is None or len(wcs_header) == 0: 
                wcs_header = ast.solve_from_image(file, force_image_upload=True) # if its not working upload image (=slower)
                print(f"Image {i+1} solved using force_image_upload")
            else:
                print(f"Image {i+1} solved using source list")
            
            hdul = fits.open(file, mode='update')
            hdul[0].header.extend(wcs_header, useblanks=True)
            hdul.flush() #write changes to disk
            hdul.close()
        except Exception as e:
            print(f"Error processing image {i+1}: {str(e)}")
    print("finished for all images")
'''


def plate_solve(path):
    input_files = glob.glob(os.path.join(path + '*.fit')) 
    ast = AstrometryNet()
    ast.api_key = 'fpcodtulvgmteoid'  # XXXXXXXXXXXXXXXXX change personal api key at end for other persons XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    
    for i, file in enumerate(input_files):
        hdul = fits.open(file)
        header = hdul[0].header
        ra_input = header['OBJCTRA']
        dec_input = header['OBJCTDEC']
        hdul.close()
        ra_deg = SkyCoord(ra=ra_input, dec=dec_input, unit=(u.hourangle, u.deg)).ra.deg
        dec_deg = SkyCoord(ra=ra_input, dec=dec_input, unit=(u.hourangle, u.deg)).dec.deg
       
        wcs_header = None
        fail = False
        try:
            wcs_header = ast.solve_from_image(file, center_dec=dec_deg, center_ra=ra_deg, radius= 0.266, scale_est=0.661,scale_units= 'arcsecperpix') #determines and upload source list to plate solve        
        except Exception as e:
            print(f"Error processing sourcelist {i+1}: {str(e)}, try upload image now")
            fail = True
        if fail == True: 
            try:
                wcs_header = ast.solve_from_image(file, force_image_upload=True, center_dec=dec_deg, center_ra=ra_deg, radius= 0.266, scale_est=0.661,scale_units= 'arcsecperpix')
            except Exception as e:
                print(f"Error processing image {i+1}: {str(e)} ")
        if wcs_header is not None: 
            hdul = fits.open(file, mode='update')
            hdul[0].header.extend(wcs_header, useblanks=True)
            hdul.flush() #write changes to disk
            hdul.close()
            print(f'success for image {i+1}')
        else:
           print(f'fail for image {i+1}')
    print("finished for all images")


#example usage: 
path = "/home/finn/visual_Studio_Code/data/2023-10-01/stacked/"
plate_solve(path)


'''
allow_commercial_use: type 'str', default value d, allowed values ('d', 'y', 'n')
allow_modifications: type 'str', default value d, allowed values ('d', 'y', 'n')
center_dec: type 'float', default value None, allowed values (-90, 90)
center_ra: type 'float', default value None, allowed values (0, 360)
crpix_center: type 'bool', default value None, allowed values ()
downsample_factor: type 'int', default value None, allowed values (1,)
parity: type 'int', default value None, allowed values (0, 2)
positional_error: type 'float', default value None, allowed values (0,)
publicly_visible: type 'str', default value y, allowed values ('y', 'n')
radius: type 'float', default value None, allowed values (0,)
scale_err: type 'float', default value None, allowed values (0, 100)
scale_est: type 'float', default value None, allowed values (0,)
scale_lower: type 'float', default value None, allowed values (0,)
scale_type: type 'str', default value None, allowed values ('ev', 'ul')
scale_units: type 'str', default value None, allowed values ('degwidth', 'arcminwidth', 'arcsecperpix')
scale_upper: type 'float', default value None, allowed values (0,)
tweak_order: type 'int', default value 2, allowed values (0,)
use_sextractor: type 'bool', default value False, allowed values ()
'''