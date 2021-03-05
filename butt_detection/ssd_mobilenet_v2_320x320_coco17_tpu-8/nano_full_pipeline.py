import tensorflow as tf
import cv2
import numpy as np
from jetcam.csi_camera import CSICamera
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils

camera = CSICamera(width=320, height=320, capture_width=1080, capture_height=720, capture_fps=30)

PATH_TO_SAVED_MODEL = './fine_tuned_model/savd_model'
PATH_TO_LABELS = '../cig_butts/tf_record/label_map.pbtxt'

detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

while True:
    # get the image
    image = camera.read()  # BRG8 numpy array

    # The input needs to be a tensor
    input_tensor = tf.convert_to_tensor(image)
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

    image_np_with_detections = image.copy()

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

    print('Done')
    cv2.imshow('', image_np_with_detections)
    cv2.waitKey(0)
