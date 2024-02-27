import numpy as np
import cv2
import os

def resize_image(image_path=None, img=None, path=True, img_size=(224,224)):
    if path:
        original_image = cv2.imread(image_path)
    else:
        original_image = img

    if original_image is None:
        print("Unable to read the image.")
        return None

    resized_image = cv2.resize(original_image, img_size)
    return resized_image

def largest_contour(image_path=None, img=None, path=True, morph_kernel_size=30, dilation_kernel_size=50, area_per=10):
    # Read the image
    if path:
        original_image = cv2.imread(image_path)
    else:
        original_image = img

    if original_image is None:
        print("Unable to read the image.")
        return None

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding
    _, binary_image = cv2.threshold(gray_image, 40, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Apply morphological operations to remove small noise
    kernel = np.ones((morph_kernel_size, morph_kernel_size), np.uint8)
    binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
    binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)

    # Find contours in the processed image
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    contour_area_threshold = (area_per / 100) * (original_image.shape[0] * original_image.shape[1])
    valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > contour_area_threshold]

    # Create a black mask
    mask = np.zeros_like(gray_image)

    # Draw the valid contours on the mask
    cv2.drawContours(mask, valid_contours, 0, 255, thickness=cv2.FILLED)
    
    dilation_kernel = np.ones((dilation_kernel_size, dilation_kernel_size), np.uint8)
    mask = cv2.dilate(mask, dilation_kernel, iterations=1)

    # Combine the mask with the original image using bitwise AND
    result_image = cv2.bitwise_and(original_image, original_image, mask=mask)

    return result_image

def apply_gamma_correction(image_path=None, img=None, path=True, gamma=1.5):
    if path:
        original_image = cv2.imread(image_path)
    else:
        original_image = img

    if original_image is None:
        print("Unable to read the image.")
        return None

    # Normalize pixel values to the range [0, 1]
    normalized_image = original_image / 255.0

    # Apply gamma correction
    gamma_corrected_image = np.power(normalized_image, gamma)

    # Rescale pixel values back to the range [0, 255]
    gamma_corrected_image = (gamma_corrected_image * 255).astype(np.uint8)

    # Save the gamma-corrected image to the output path
    return gamma_corrected_image

def apply_clahe(image_path=None, img=None, path=True, tile_size=(4, 4), clip_limit=1.0):
    if path:
        original_image = cv2.imread(image_path)
    else:
        original_image = img

    if original_image is None:
        print("Unable to read the image.")
        return None

    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # Create a CLAHE object
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)

    # Apply CLAHE to the grayscale image
    clahe_image = clahe.apply(gray_image)

    return clahe_image

def is_pixel_blackish(pixel, threshold=30):
    # Check if all color channels are below the threshold
    return all(value <= threshold for value in pixel)

def image_not_qualified(image_path=None, img=None, path=True, threshold_percentage=0.9, pixel_threshold=30):
    if path:
        original_image = cv2.imread(image_path)
    else:
        original_image = img

    if original_image is None:
        print("Unable to read the image.")
        return None
   
    pixels = img.reshape((-1, 3))

    # Count occurrences of each unique pixel value
    unique_values, counts = np.unique(pixels, axis=0, return_counts=True)

    # Find the most common pixel value
    most_common_index = np.argmax(counts)
    most_common_count = counts[most_common_index]

    # Calculate the percentage of the most common color
    percentage = most_common_count / len(pixels)

    # Check if the most common color covers at least threshold_percentage% of the image
    if percentage > threshold_percentage:
        # Check if the most common color is black-ish
        most_common_color = unique_values[most_common_index]
        return is_pixel_blackish(most_common_color, pixel_threshold)

    return False

def preprocessing(df_row, save_dir="E:/CBIS-DDSM/preprocess"):
    img_path = df_row['img_path']

    resized_img = resize_image(image_path=img_path)
    remove_artefacts = largest_contour(img=resized_img, path=False)
    gamma_img = apply_gamma_correction(img=remove_artefacts, path=False)
    clahe_img = apply_clahe(img=gamma_img, path=False)

    check = image_not_qualified(img=cv2.cvtColor(clahe_img, cv2.COLOR_GRAY2RGB), path=False)
    if check:
        return img_path
    else:
        img_save_name = df_row['new_id']
        output_folder = f"{save_dir}/{df_row['pathology']}"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        img_save_path = f"{output_folder}/{img_save_name}.jpg"
        cv2.imwrite(img_save_path, clahe_img)
        return None
        