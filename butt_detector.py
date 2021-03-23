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

            viz_utils.visualize_boxes_and_labels_on_image_array(
                  image_np_with_detections,
                  detections['detection_boxes'],
                  detections['detection_classes'],
                  detections['detection_scores'],
                  self.category_index,
                  use_normalized_coordinates=True,
                  max_boxes_to_draw=200,
                  min_score_thresh=.30,
                  agnostic_mode=False)

            # get the coordinates of the bounding box
            coordinates = self.return_coordinates(
                  image_np_with_detections,
                  detections['detection_boxes'],
                  detections['detection_classes'],
                  detections['detection_scores'],
                  self.category_index,
                  use_normalized_coordinates=True,
                  max_boxes_to_draw=200,
                  min_score_thresh=.30,
                  agnostic_mode=False)

            # calculate the center of the box
            center = [(coordinates[0]+coordinates[1])/2, (coordinates[2]+coordinates[3])/2]

            # send the center to the queue
            self.detection_q.put(center)

        return

    def visualize_detections(self):

        return

    def return_coordinates(  # https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10/issues/69#issuecomment-410620593
        image,
        boxes,
        classes,
        scores,
        category_index,
        instance_masks=None,
        instance_boundaries=None,
        keypoints=None,
        use_normalized_coordinates=False,
        max_boxes_to_draw=20,
        min_score_thresh=.5,
        agnostic_mode=False,
        line_thickness=4,
        groundtruth_box_visualization_color='black',
        skip_scores=False,
        skip_labels=False):

      STANDARD_COLORS = [  # this copied from research/object_detection/utils/visualization_utils.py
          'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
          'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
          'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
          'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
          'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
          'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
          'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
          'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
          'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
          'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
          'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
          'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
          'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
          'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
          'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
          'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
          'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
          'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
          'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
          'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
          'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
          'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
          'WhiteSmoke', 'Yellow', 'YellowGreen'
      ]

      # Create a display string (and color) for every box location, group any boxes
      # that correspond to the same location.
      box_to_display_str_map = collections.defaultdict(list)
      box_to_color_map = collections.defaultdict(str)
      box_to_instance_masks_map = {}
      box_to_instance_boundaries_map = {}
      box_to_score_map = {}
      box_to_keypoints_map = collections.defaultdict(list)
      if not max_boxes_to_draw:
        max_boxes_to_draw = boxes.shape[0]
      for i in range(min(max_boxes_to_draw, boxes.shape[0])):
        if scores is None or scores[i] > min_score_thresh:
          box = tuple(boxes[i].tolist())
          if instance_masks is not None:
            box_to_instance_masks_map[box] = instance_masks[i]
          if instance_boundaries is not None:
            box_to_instance_boundaries_map[box] = instance_boundaries[i]
          if keypoints is not None:
            box_to_keypoints_map[box].extend(keypoints[i])
          if scores is None:
            box_to_color_map[box] = groundtruth_box_visualization_color
          else:
            display_str = ''
            if not skip_labels:
              if not agnostic_mode:
                if classes[i] in category_index.keys():
                  class_name = category_index[classes[i]]['name']
                else:
                  class_name = 'N/A'
                display_str = str(class_name)
            if not skip_scores:
              if not display_str:
                display_str = '{}%'.format(int(100*scores[i]))
              else:
                display_str = '{}: {}%'.format(display_str, int(100*scores[i]))
            box_to_display_str_map[box].append(display_str)
            box_to_score_map[box] = scores[i]
            if agnostic_mode:
              box_to_color_map[box] = 'DarkOrange'
            else:
              box_to_color_map[box] = STANDARD_COLORS[
                  classes[i] % len(STANDARD_COLORS)]

      # Draw all boxes onto image.
      coordinates_list = []
      counter_for = 0
      for box, color in box_to_color_map.items():
        ymin, xmin, ymax, xmax = box
        height, width, channels = image.shape
        ymin = int(ymin*height)
        ymax = int(ymax*height)
        xmin = int(xmin*width)
        xmax = int(xmax*width)
        coordinates_list.append([ymin, ymax, xmin, xmax, (box_to_score_map[box]*100)])
        counter_for = counter_for + 1

      return coordinates_list
