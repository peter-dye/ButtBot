import tensorflow as tf
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
import cv2


def load_image_into_numpy_array(path):
    return np.array(Image.open(path))


PATH_TO_SAVED_MODEL = './fine_tuned_model/saved_model'
PATH_TO_LABELS = '../cig_butts/tf_record/label_map.pbtxt'

# real test images
IMAGE_PATHS = ['../cig_butts/real_test/images/0000.JPG',
               '../cig_butts/real_test/images/0001.JPG',
               '../cig_butts/real_test/images/0002.JPG',
               '../cig_butts/real_test/images/0003.JPG',
               '../cig_butts/real_test/images/0004.JPG',
               '../cig_butts/real_test/images/0005.JPG',
               '../cig_butts/real_test/images/0006.JPG',
               '../cig_butts/real_test/images/0007.JPG',
               '../cig_butts/real_test/images/0008.JPG',
               '../cig_butts/real_test/images/0009.JPG']

# coco test model
# PATH_TO_SAVED_MODEL = './saved_model'
# PATH_TO_LABELS = '../models/research/object_detection/data/mscoco_label_map.pbtxt'
#
# coco test images
# IMAGE_PATHS = ['../models/research/object_detection/test_images/image1.jpg',
#                '../models/research/object_detection/test_images/image2.jpg']

detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

i = 0

for image_path in IMAGE_PATHS:

    print('Running inference for {}... '.format(image_path), end='')

    image_np = load_image_into_numpy_array(image_path)

    # The input needs to be a tensor
    input_tensor = tf.convert_to_tensor(image_np)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis, ...]

    # input_tensor = np.expand_dims(image_np, 0)
    detections = detect_fn(input_tensor)

    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    image_np_with_detections = image_np.copy()

    viz_utils.visualize_boxes_and_labels_on_image_array(
          image_np_with_detections,
          detections['detection_boxes'],
          detections['detection_classes'],
          detections['detection_scores'],
          category_index,
          use_normalized_coordinates=True,
          max_boxes_to_draw=200,
          min_score_thresh=.30,
          agnostic_mode=False)

    plt.figure()
    plt.imshow(image_np_with_detections)
    print('Done')
    plt.savefig('./fine_tune_testing/inference_'+str(i)+'.png', dpi=95)
    i += 1

    # print('Done')
    # cv2.imshow('', image_np_with_detections)
    # cv2.waitKey(0)
