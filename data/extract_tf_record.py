# import os
# import tensorflow as tf
# from pprint import pprint
# import numpy as np
# import csv 
# import imageio
# options = tf.compat.v1.python_io.TFRecordOptions(tf.compat.v1.python_io.TFRecordCompressionType.NONE)

# root = "./input_images"

# filenames = ["./raw_data/" + f for f in os.listdir("./raw_data/")]
# print(filenames)
# idx = 0
# for f in filenames:
#     f_sub = f.split('.')[1][10:]
#     print(f_sub)
#     output_directory = root + "/planetscope/" + f_sub
#     if not os.path.exists(output_directory):
#         os.makedirs(output_directory)

#     satellite_features = ['B2', 'B3', 'B4']

#     print(">>>>>> Processing: " + f)
#     iterator = tf.compat.v1.python_io.tf_record_iterator(f, options=options)
#     n = 0
#     print(f)
#     iter = 10
#     csv_file = output_directory  + "/img_csv.csv"
#     csv_file_keys = ['Parcel_id', 'max_lat', 'max_lon', 'min_lat', 'min_lon']
#     with open(csv_file, 'w') as f_csv:
#         csv_writer = csv.writer(f_csv)
#         csv_writer.writerow(csv_file_keys)
    
#     while iter > 0:
#         with open(csv_file, 'a') as f_csv:
#             csv_writer = csv.writer(f_csv)
#             try:
#                 record_str = next(iterator)
#                 ex = tf.train.Example.FromString(record_str)
#                 #print(ex.features)
#                 min_lon = min(ex.features.feature['longitude'].float_list.value) 
#                 max_lon = max(ex.features.feature['longitude'].float_list.value) 
#                 min_lat = min(ex.features.feature['latitude'].float_list.value) 
#                 max_lat = max(ex.features.feature['latitude'].float_list.value) 
#                 idx = idx + 1#int(ex.features.feature['Parcel_id'].float_list.value[0])
#                 features = []
#                 for satellite_feature in satellite_features:
#                     feature = (ex.features.feature[satellite_feature].float_list.value)
#                     feature = np.array(feature)
#                     feature = feature.reshape((225, 225, 1))
#                     feature = np.flip(feature, axis=0)
#                     features.append(feature)

#                 csv_writer.writerow([idx, max_lat*10000, max_lon*10000, min_lat*10000, min_lon*10000])
#                 image = np.concatenate(features, axis=2)
#                 image = image[:224, :224, :]

#                 if idx != -1:
#                     jpeg_path = output_directory + '/' + str(idx) + '.jpeg'
                    
#                     imageio.imwrite(jpeg_path, image)
          
#                     #scipy.misc.toimage(image, cmin=0.0, cmax=...).save(jpeg_path)
#                     #writer = tf.python_io.TFRecordWriter(tfrecord_path, options=options)
#                     #writer.write(ex.SerializeToString())
#                     #writer.close()
#                 #print(idx)
#                 n += 1
#                 if n%10==0:
#                     print("       Processed " + str(n) + " records in " + f)
#             except Exception as e:
#                 iter -= 1
#                 print(e)
#                 print(">>>>>> Processed " + str(n) + " records in " + f)


import os
import shutil
import tensorflow as tf
from pyunpack import Archive

BASE_DIR = "france/"

path = BASE_DIR + "gz_files/"
tf_out_path = BASE_DIR + "tf_files/"

if os.path.exists(tf_out_path):
    print("Removing Existing Directory.....")
    shutil.rmtree(tf_out_path)

print("Creating TFRECORD Exctract Directory.....")
os.makedirs(tf_out_path)
    
gz_files = os.listdir(path)

for i in gz_files:
    Archive(path+i).extractall(tf_out_path)
    
img_out_path = BASE_DIR + "images/"
if not os.path.exists(img_out_path):
    os.makedirs(img_out_path)
    
tf_files = os.listdir(path)

# for tf_file in tf_files:
tf_file = tf_out_path + tf_files[0]
print(">>>>>> Processing: " + tf_file)
iterator = tf.compat.v1.python_io.tf_record_iterator(tf_file, options=options)
print(iterator)
#     n = 0
#     iter = 10
#     csv_file = output_directory  + "/img_csv.csv"
#     csv_file_keys = ['Parcel_id', 'max_lat', 'max_lon', 'min_lat', 'min_lon']
#     with open(csv_file, 'w') as f_csv:
#         csv_writer = csv.writer(f_csv)
#         csv_writer.writerow(csv_file_keys)