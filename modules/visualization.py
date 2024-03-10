import matplotlib.pyplot as plt
import pydicom
import numpy as np
import os
import cv2
import pandas as pd


def convert_dicom_to_png(dicom_file: str) -> np.ndarray:
    """
    dicom_file: path to the dicom fife

    return
        gray scale image with pixel intensity in the range [0,255]
        None if cannot convert

    """
    data = pydicom.read_file(dicom_file)
    if ('WindowCenter' not in data) or\
       ('WindowWidth' not in data) or\
       ('PhotometricInterpretation' not in data) or\
       ('RescaleSlope' not in data) or\
       ('PresentationIntentType' not in data) or\
       ('RescaleIntercept' not in data):

        print(f"{dicom_file} DICOM file does not have required fields")
        return

    intentType = data.data_element('PresentationIntentType').value
    if ( str(intentType).split(' ')[-1]=='PROCESSING' ):
        print(f"{dicom_file} got processing file")
        return


    c = data.data_element('WindowCenter').value # data[0x0028, 0x1050].value
    w = data.data_element('WindowWidth').value  # data[0x0028, 0x1051].value
    if type(c)==pydicom.multival.MultiValue:
        c = c[0]
        w = w[0]

    photometricInterpretation = data.data_element('PhotometricInterpretation').value

    try:
        a = data.pixel_array
    except:
        print(f'{dicom_file} Cannot get get pixel_array!')
        return

    slope = data.data_element('RescaleSlope').value
    intercept = data.data_element('RescaleIntercept').value
    a = a * slope + intercept

    try:
        pad_val = data.get('PixelPaddingValue')
        pad_limit = data.get('PixelPaddingRangeLimit', -99999)
        if pad_limit == -99999:
            mask_pad = (a==pad_val)
        else:
            if str(photometricInterpretation) == 'MONOCHROME2':
                mask_pad = (a >= pad_val) & (a <= pad_limit)
            else:
                mask_pad = (a >= pad_limit) & (a <= pad_val)
    except:
        # Manually create padding mask
        # this is based on the assumption that padding values take majority of the histogram
        print(f'{dicom_file} has no PixelPaddingValue')
        a = a.astype(np.int)
        pixels, pixel_counts = np.unique(a, return_counts=True)
        sorted_idxs = np.argsort(pixel_counts)[::-1]
        sorted_pixel_counts = pixel_counts[sorted_idxs]
        sorted_pixels = pixels[sorted_idxs]
        mask_pad = a == sorted_pixels[0]
        try:
            # if the second most frequent value (if any) is significantly more frequent than the third then
            # it is also considered padding value
            if sorted_pixel_counts[1] > sorted_pixel_counts[2] * 10:
                mask_pad = np.logical_or(mask_pad, a == sorted_pixels[1])
                print(f'{dicom_file} most frequent pixel values: {sorted_pixels[0]}; {sorted_pixels[1]}')
        except:
            print(f'{dicom_file} most frequent pixel value {sorted_pixels[0]}')

    # apply window
    mm = c - 0.5 - (w-1)/2
    MM = c - 0.5 + (w-1)/2
    a[a<mm] = 0
    a[a>MM] = 255
    mask = (a>=mm) & (a<=MM)
    a[mask] = ((a[mask] - (c - 0.5)) / (w-1) + 0.5) * 255

    if str( photometricInterpretation ) == 'MONOCHROME1':
        a = 255 - a

    a[mask_pad] = 0
    return a

def demo(dicom_path = "VinDr-Mammo/images/0a0c5108270e814818c1ad002482ce74/0a6a90bdc088e0cc62df8d2d58d14840.dicom"):
    png_img = convert_dicom_to_png(dicom_path)
    plt.imshow(png_img, cmap="gray")
    plt.show()

def main(df, data_dir, out_path):
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    for idx, row in df.iterrows():
        dicom_path = os.path.join(data_dir, 'images', row['study_id'], row['image_id'] + '.dicom')
        out_folder = os.path.join(out_path, row['study_id'])
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        save_path = os.path.join(out_path,row['study_id'], row['image_id'] + '.png')
        if not os.path.isfile(save_path):
            png_img = convert_dicom_to_png(dicom_path)
            cv2.imwrite(save_path, png_img)
            print("NO")
        print("OK")
        # print(save_path)
        # plt.imshow(png_img, cmap="gray")
        # plt.show()

# if __name__ == "__main__":
#     data_dir = 'E:/vindr_mammo/Data'
#     out_path = 'E:/vindr_mammo/Data/png'
#     df = pd.read_csv('./Data/full_df.csv').head(5)
#     main(df, data_dir, out_path)
    