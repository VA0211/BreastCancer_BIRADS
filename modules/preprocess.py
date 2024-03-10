import os
import pydicom
from pydicom.pixel_data_handlers.util import apply_voi_lut
import cv2
import numpy as np

def fit_image(fname):
    dicom = pydicom.dcmread(fname)

    X = apply_voi_lut(dicom.pixel_array, dicom, prefer_lut = False)
    X = (X - X.min()) / (X.max() - X.min())

    photometricInterpretation = dicom.data_element('PhotometricInterpretation').value  
    if photometricInterpretation == "MONOCHROME1":
        X = 1 - X
    
    X = X * 255
    
    # Some images have narrow exterior "frames" that complicate selection of the main data. Cutting off the frame
    X = X[10:-10, 10:-10]
    
    # regions of non-empty pixels
    output= cv2.connectedComponentsWithStats((X > 20).astype(np.uint8), 8, cv2.CV_32S)

    # stats.shape == (N, 5), where N is the number of regions, 5 dimensions correspond to:
    # left, top, width, height, area_size
    stats = output[2]
    
    # finding max area which always corresponds to the breast data. 
    idx = stats[1:, 4].argmax() + 1
    x1, y1, w, h = stats[idx][:4]
    x2 = x1 + w
    y2 = y1 + h
    
    # cutting out the breast data
    X_fit = X[y1: y2, x1: x2]
    return X_fit


def main(df, data_dir, out_path):
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    for idx, row in df.iterrows():
        dicom_path = os.path.join(data_dir, 'images', row['study_id'], row['image_id'] + '.dicom')
        
        out_folder = os.path.join(out_path, row['study_id'])
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        save_path = os.path.join(out_path, row['study_id'], row['image_id'] + '.png')
        png_img = fit_image(dicom_path)
        cv2.imwrite(save_path, png_img)


# if __name__ == '__main__':
#     main()