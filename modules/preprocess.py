# import os
# import ast
# import pandas as pd
# import numpy as np
# import seaborn as sns
# from tqdm import tqdm
# from pydicom import dcmread
# from skimage.io import imsave
# from skimage.transform import resize

# def dicom_to_png(data, data_dir='E:/vindr_mammo/Data', image_size=(512,512)):
#     preproc_dir = 'images_512x512'
#     out_dir = os.path.join(data_dir,preproc_dir)

#     if not os.path.exists(out_dir):
#         os.makedirs(out_dir)

#     for idx, _ in enumerate(tqdm(range(len(data)), desc='Processing Data')):    
        
#         out_path = os.path.join(out_dir, data.loc[idx, 'study_id'])
#         if not os.path.exists(out_path):
#             os.makedirs(out_path)

#         img_path = os.path.join(data_dir, 'images', data.loc[idx, 'study_id'], data.loc[idx, 'image_id'] + '.dicom')
#         out_fn = os.path.join(out_path, data.loc[idx, 'image_id'] + '.png')
        
#         if not os.path.exists(out_fn):

#             dicom = dcmread(img_path)
#             image = dicom.pixel_array
            
#             window = np.array(ast.literal_eval(data.loc[idx, 'Window Width']))
#             level = np.array(ast.literal_eval(data.loc[idx, 'Window Center']))

#             # Multiple window/level settings for IMS Giotto images
#             if data.loc[idx, "Manufacturer's Model Name"] == 'GIOTTO IMAGE 3DL' or data.loc[idx, "Manufacturer's Model Name"] == 'GIOTTO CLASS':
#                 window = window[0]
#                 level = level[0]

#             # MONOCHROME1 images need special handling for inverting pixel intensities
#             if data.loc[idx, 'Photometric Interpretation'] == 'MONOCHROME1':
#                 image[image==1] += data.loc[idx, 'Pixel Padding Value']
#                 level = np.max(image) - level
#                 image = np.max(image) - image

#             # Resize image
#             image = resize(image, output_shape=image_size, preserve_range=True).astype(np.float32)

#             # Normalize pixel intensities, and convert to 8-bit
#             image -= (level - window/2)
#             image /= window
#             image[image<0] = 0
#             image[image>1] = 1
#             image *= 255

#             # Flip image with laterality equals right
#             # if data.loc[idx, 'laterality'] == 'R':
#             #     image = image[:, ::-1]

#             imsave(out_fn, image.astype(np.uint8))

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