import sys

''' PATH TO THE TENSORFLOW INSTALLATION SHOULD BE IN THE PYTHON PATH. See official Tensorflow object detection installation instructions'''
sys.path.append('/home/peps/Class Files/models/research')

import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import cv2
import time

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from object_detection.utils import label_map_util

# global variables used 
detection_graph = None
category_index = None
session = None

# Path to frozen detection graph. This is the actual model that is used for the object detection.

#PATH_TO_CKPT = '/home/peps/Class-Files/mobilenet/frozen_inference_graph.pb'
PATH_TO_CKPT = '<INSERT PATH TO TO THE PB FILE>'

# List of the strings that is used to add correct label for each box.

#PATH_TO_LABELS = '/home/peps/Class-Files/mobilenet/label_map.pbtxt'
PATH_TO_LABELS = '<INSERT PATH TO THE LABEL FILE>'

# Number of classes to detect
NUM_CLASSES = 3

# init function called at the time of flask app startup
def init_detection_graph():
    global detection_graph
    global session
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        session = tf.Session(graph=detection_graph)

# init function called at the time of flask app startup
def init_label_map():
    global category_index
    # Loading label map
    # Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(
        label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)


def init_tensorflow():
    print("Tensorflow init started")
    if detection_graph is None or category_index is None or session is None:
        print("running initialization.....")
        init_detection_graph()
        init_label_map()
        print("initialization completed")
    else:
        print("already initialized::")

# input:: numpy image array
# output:: Class (String)
def infer(image_np):
    print(image_np.shape)
    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    start_time = time.time()
    image_np_expanded = np.expand_dims(image_np, axis=0)
    # Extract image tensor
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Extract detection boxes
    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    #print(boxes)
    # Extract detection scores
    scores = detection_graph.get_tensor_by_name('detection_scores:0')
    # Extract detection classes
    classes = detection_graph.get_tensor_by_name('detection_classes:0')
    #print(classes)
    # Extract number of detectionsd
    num_detections = detection_graph.get_tensor_by_name(
        'num_detections:0')
    end_time = time.time()
    #print('time taken::prerun', end_time - start_time)
    # Actual detection.
    start_time = time.time()
    (boxes, scores, classes, num_detections) = session.run(
        [boxes, scores, classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
    end_time = time.time()
    print('time taken::run', end_time - start_time)
    res = ([category_index.get(value) for index,value in enumerate(classes[0]) if scores[0,index] > 0.5])
    return res[0]['name']