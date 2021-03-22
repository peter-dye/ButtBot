import tensorflow as tf
import cv2
import numpy as np
from jetcam.csi_camera import CSICamera
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from multiprocessing import Process, Queue


class ButtDetector():

    def __init__(self, camera):
        self.camera = camera

        self.SAVED_MODEL_PATH = './fine_tuned_model/savd_model'
        self.LABEL_PATH = '../cig_butts/tf_record/label_map.pbtxt'

        self.detect_fn = tf.saved_model.load(self.PATH_TO_SAVED_MODEL)

        self.category_index = label_map_util.create_category_index_from_labelmap(self.PATH_TO_LABELS, use_display_name=True)

        self.detection_q = Queue()

        self.detection_process = Process(target=self.butt_detection, args=(self.detection_q,))
        self.detection_process.start()

        return

    def butt_detection(self, detection_queue):
        while True:
            image = self.camera.read()
            input_tensor = tf.convert_to_tensor(image)
            input_tensor = input_tensor[tf.newaxis, ...]

            detections = self.detect_fn(input_tensor)

            num_detections = int(detections.pop('num_detections'))
            detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
            detections['num_detections'] = num_detections

            detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

            image_np_with_detections = image.copy()

            # send coordinates to detection_q

        return

    def visualize_detections(self):

        return
