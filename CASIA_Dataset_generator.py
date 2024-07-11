import cv2
import face_recognition
import mxnet as mx
import numpy as np
import os
import shutil

rec_file = './Datasets/CASIA/archive/casia-webface/train.rec'
idx_file = './Datasets/CASIA/archive/casia-webface/train.idx'
lst_file = './Datasets/CASIA/archive/casia-webface/train.lst'

out_dir = "CASIA_WebFace_dataset"

num_id = 1000
num_samples = 6
cur_id = 0

data_iter = mx.image.ImageIter(
    batch_size=12,
    data_shape=(3, 112, 112),
    path_imgrec=rec_file,
    path_imgidx=idx_file
)
data_iter.reset()

while cur_id < num_id:
    batch = data_iter.next()
    data = batch.data[0]
    
    label = batch.label[0].asnumpy()

    for i in range(len(data)):
        id_dir_path = os.path.join(out_dir, f"identity_{str(int(label[i]))}")
        cur_id = int(label[i])

        if not os.path.exists(id_dir_path):
            os.makedirs(id_dir_path)

        if len(os.listdir(id_dir_path)) < num_samples:
            img = data[i].asnumpy().astype(np.uint8).transpose((1, 2, 0))
            img_name = os.path.join(id_dir_path, f'image_{i}.png')
            cv2.imwrite(img_name, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

            # Let's check if a face is correctly visible!
            img_rec = face_recognition.load_image_file(img_name)
            img_encodings = face_recognition.face_encodings(img_rec)

            # If the face is not recognized it's a bad photo, discard it!
            if len(img_encodings) < 1:
                os.remove(img_name)
            
            # If there are multiple faces in the image, bad photo! Discard it!
            if len(img_encodings) > 1:
                os.remove(img_name)
        else: break

# Removes the directories that do not have at least 6 faces
dataset = "./CASIA_WebFace_dataset"
counter = 0
for dir in os.listdir(dataset):
    fullpath = os.path.join(dataset, dir)
    if len(os.listdir(fullpath)) < 6:
        shutil.rmtree(fullpath)
        counter += 1

print(f"{counter} identities have been removed because they didn't have enough photos")
        
        