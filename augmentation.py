import Augmentor
import os

# def apply_data_augmentations(input_image_path, output_directory):
#     # Create an Augmentor pipeline for each augmentation
#     pipelines = []

#     # Augmentation 1: Flipping horizontally
#     pipeline = Augmentor.Pipeline(input_image_path, output_directory)
#     pipeline.flip_left_right(probability=1)
#     pipelines.append(pipeline)

#     # Augmentation 2: Flipping both horizontally and vertically
#     pipeline = Augmentor.Pipeline(input_image_path, output_directory)
#     pipeline.flip_left_right(probability=1)
#     pipeline.flip_top_bottom(probability=1)
#     pipelines.append(pipeline)

#     # Augmentation 3: Flipping vertically
#     pipeline = Augmentor.Pipeline(input_image_path, output_directory)
#     pipeline.flip_top_bottom(probability=1)
#     pipelines.append(pipeline)

#     # Augmentation 4: 30° rotation
#     pipeline = Augmentor.Pipeline(input_image_path, output_directory)
#     pipeline.rotate_without_crop(probability=1, max_left_rotation=30, max_right_rotation=30)
#     pipelines.append(pipeline)

#     # Augmentation 5: 30° rotation and flipping horizontally
#     pipeline = Augmentor.Pipeline(input_image_path, output_directory)
#     pipeline.rotate_without_crop(probability=1, max_left_rotation=30, max_right_rotation=30)
#     pipeline.flip_left_right(probability=1)
#     pipelines.append(pipeline)

#     # Augmentation 6: -30° rotation
#     pipeline = Augmentor.Pipeline(input_image_path, output_directory)
#     pipeline.rotate_without_crop(probability=1, max_left_rotation=-30, max_right_rotation=-30)
#     pipelines.append(pipeline)

#     # Augmentation 7: -30° rotation and horizontal flip
#     pipeline = Augmentor.Pipeline(input_image_path, output_directory)
#     pipeline.rotate_without_crop(probability=1, max_left_rotation=-30, max_right_rotation=-30)
#     pipeline.flip_left_right(probability=1)
#     pipelines.append(pipeline)

#     # Execute pipeline to create augmented images
#     pipeline.sample(7)


# def apply_data_augmentations_to_folder(root_folder, output_folder):
#     for label in os.listdir(root_folder):
#         label_folder = os.path.join(root_folder, label)
#         if os.path.isdir(label_folder):
#             output_label_folder = os.path.join(output_folder, label)
#             os.makedirs(output_label_folder, exist_ok=True)
#             apply_data_augmentations(label_folder, output_label_folder)

import cv2

def get_rotation_matrix(image, angle):
    height, width = image.shape[:2]

    # Calculate the rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    return rotation_matrix

def apply_augmentations(image_path, output_folder):
    # Read the original image
    original_image = cv2.imread(image_path)
    height, width = original_image.shape[:2]

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    

    # Define the augmentation operations
    augmentations = [
        ("flip_horizontal", cv2.flip(original_image, 1)),
        ("flip_horizontal_vertical", cv2.flip(original_image, -1)),
        ("flip_vertical", cv2.flip(original_image, 0)),
        # ("rotate_30", cv2.warpAffine(original_image, get_rotation_matrix(original_image, angle=30), (width, height))),
        # ("rotate_30_flip_horizontal", cv2.flip(cv2.warpAffine(original_image, get_rotation_matrix(original_image, angle=30), (width, height)), 1)),
        # ("rotate_-30", cv2.warpAffine(original_image, get_rotation_matrix(original_image, angle=-30), (width, height))),
        # ("rotate_-30_flip_horizontal", cv2.flip(cv2.warpAffine(original_image, get_rotation_matrix(original_image, angle=-30), (width, height)), 1))
    ]

    # Save augmented images
    base_filename = os.path.splitext(os.path.basename(image_path))[0]
    for name, augmented_image in augmentations:
        output_path = os.path.join(output_folder, f"{base_filename}_{name}.jpg")
        cv2.imwrite(output_path, augmented_image)

def apply_augmentations_to_folder(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through each subfolder (label) in the input folder
    for label_folder in os.listdir(input_folder):
        label_folder_path = os.path.join(input_folder, label_folder)

        # Skip if the item is not a directory
        if not os.path.isdir(label_folder_path):
            continue

        # Create a subfolder in the output folder for the current label
        output_label_folder = os.path.join(output_folder, label_folder)
        if not os.path.exists(output_label_folder):
            os.makedirs(output_label_folder)

        # Iterate through each image in the current label folder and apply augmentations
        for filename in os.listdir(label_folder_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(label_folder_path, filename)
                apply_augmentations(image_path, output_label_folder)