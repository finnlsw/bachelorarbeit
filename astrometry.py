import glob
import os
from astroquery.astrometry_net import AstrometryNet
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u


def plate_solve(path):
    input_files = glob.glob(os.path.join(path, '*.fit')) 
    ast = AstrometryNet()
    ast.api_key = # XXXXXXXXXXXXXXXXX my key: 'fpcodtulvgmteoid', please generate our own personal api key at astrometry.net (takes only 2min) XXXXXXXXXXXXXXXXXXXXXX
    
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
path= "/home/finn/visual_Studio_Code/data/2024-01-10"
plate_solve(path)
