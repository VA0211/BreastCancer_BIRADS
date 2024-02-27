import os
import pandas as pd
import cv2
import shutil
import matplotlib.pyplot as plt

def create_df_from_subfolder(large_folder_path):

    # Initialize empty lists to store subfolder names and image paths
    subfolder_names = []
    image_paths = []

    # Iterate through subfolders
    for subfolder_name in os.listdir(large_folder_path):
        subfolder_path = os.path.join(large_folder_path, subfolder_name)
        
        # Check if the item is a directory
        if os.path.isdir(subfolder_path):
            
            # Iterate through images in the subfolder
            for image_name in os.listdir(subfolder_path):
                # Create the image path
                image_path = os.path.join(subfolder_path, image_name).replace("\\", "/")
                
                # Append subfolder name and image path to the lists
                subfolder_names.append(subfolder_name)
                image_paths.append(image_path)

    # Create a DataFrame from the lists
    df = pd.DataFrame({'pathology': subfolder_names, 'image_path': image_paths})
    return df

def show_img(image_path=None, img=None, path=True):
    if path:
        original_image = cv2.imread(image_path)
    else:
        original_image = img
    plt.imshow(original_image)
    plt.show()

def create_folder(train_folder, val_folder, test_folder):
    for folder in [train_folder, val_folder, test_folder]:
        os.makedirs(folder, exist_ok=True)

# Move images to their respective folders based on the split
def move_images(df, destination_folder, train_folder, val_folder, test_folder):
    create_folder(train_folder, val_folder, test_folder)
    for index, row in df.iterrows():
        label_folder = os.path.join(destination_folder, row['label'])
        os.makedirs(label_folder, exist_ok=True)
        shutil.copy(row['image_path'], label_folder)
    