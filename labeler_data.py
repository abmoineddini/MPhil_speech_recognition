import cv2
import os
import numpy as np

labels = ['Or_To_Take_Arms', 'That_Is_The_Question', 'To_be_or_not_to_be', 'To_die', 'To_Sleep', 'Whether']
#img_size = 32
def get_data(data_dir, img_size):
    data = []
    for label in labels:
        path = os.path.join(data_dir, label)
        class_num = labels.index(label)
        for img in os.listdir(path):
            try:
                img_arr = cv2.imread(os.path.join(path, img))[...,::-1] #convert BGR to RGB format
                resized_arr = cv2.resize(img_arr, (img_size, img_size)) # Reshaping images to preferred size
                data.append([resized_arr, class_num])
            except Exception as e:
                print(e)
    return np.array(data)