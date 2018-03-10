import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image
from shutil import copyfile
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from utils import ops as utils_ops

from utils import label_map_util

from utils import visualization_utils as vis_util

class Added_images(QLabel):

    def __init__(self,source,cnt):
        super(Added_images, self).__init__()
        self.pixmap = QPixmap(source)
        self.pixmap = self.pixmap.scaledToHeight(300)
        self.pixmap = self.pixmap.scaledToWidth(300)
        self.setPixmap(self.pixmap)
        self.cnt = cnt


    def mousePressEvent(self, QEvent):

        self.setParent(None)

        past = os.getcwd()
        os.chdir(past + "\\\\test_images")
        os.remove("image{}.jpg".format(self.cnt))
        os.chdir(past)

    def leaveEvent(self,t):
        pass


class Example(QWidget):


    def __init__(self):
        super().__init__()

        self.setMouseTracking(True)

        self.scroll = QScrollArea()
        self.special = QWidget()
        self.special_lay = QVBoxLayout()


        self.v_right = QVBoxLayout(self)


        resolution = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, 850, 550)
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
                  (resolution.height() / 2) - (self.frameSize().height() / 2))



        self.big_label = QLabel(self)
        self.upload = QPushButton(self)
        self.message = QLabel(self)
        self.train = QPushButton(self)

        self.initUI()


    def initUI(self):

        self.setAcceptDrops(True)

        self.upload.setText('upload')
        self.upload.clicked.connect(lambda: self.openFileNamesDialog())
        self.upload.setFont(QFont('Arial', 23))

        self.message.setText('Or simply drag and drop ! \n  Click train to start !. \n Enjoy :)')
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setFont(QFont('Arial', 23))

        self.train.setText('train')
        self.train.setFont(QFont('Arial', 23))
        self.train.clicked.connect(lambda: self.start_train())



        v_left = QVBoxLayout()
        v_left.addWidget(self.upload, Qt.AlignBottom)
        v_left.addWidget(self.message)
        v_left.addWidget(self.train)

        left = QFrame(self)
        left.setFrameShape(QFrame.StyledPanel)
        left.setLayout(v_left)




        self.special.setLayout(self.special_lay)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumHeight(150)
        self.scroll.setWidget(self.special)

        qlabel = QLabel(self)
        qlabel.setText("Remove selected images by clicking over them.")
        qlabel.setFont(QFont('',7))
        self.v_right.addWidget(qlabel)
        self.v_right.addWidget(self.scroll)

        right = QFrame(self)
        right.setFrameShape(QFrame.StyledPanel)
        right.setLayout(self.v_right)

        right.setMaximumWidth(500)
        right.setMinimumWidth(450)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left)
        splitter.addWidget(right)

        vbox1 = QVBoxLayout(self)
        vbox1.addWidget(splitter)

        self.setLayout(vbox1)
        self.setWindowTitle('Train your images on raspberry pi 2 !!!')

        self.show()

 
    def openFileNamesDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
        for file in files:

            self.load_and_store(file,self.v_right)

    def dragEnterEvent(self, e):
        e.accept()
    def dropEvent(self, e):

       if e.mimeData().hasUrls:
         e.setDropAction(Qt.CopyAction)
         e.accept()
        # Workaround for OSx dragging and dropping
         for url in e.mimeData().urls():

             file = str(url.toLocalFile())
             self.load_and_store(file,self.v_right)

    def load_image(self,cnt):

        copyfile("image{}.jpg".format(cnt), "image_{}.jpg".format(cnt))
        im = Image.open("image_{}.jpg".format(cnt))
        im.save("image_{}.png".format(cnt))
        im = im.resize((250,250),Image.ANTIALIAS)
        im.close()

        tmp = Added_images("image_{}.png".format(cnt),cnt)

        os.remove("image_{}.png".format(cnt))
        os.remove("image_{}.jpg".format(cnt))

        self.special_lay.addWidget(tmp)

    def load_and_store(self,file,k):


        new_file_name = file.split(".", 1)[0] + "(1).jpg"
        copyfile(file, new_file_name)

        fname = file[::-1]
        fname = fname.split("/", 1)[0]
        fname = fname[::-1]

        past = os.getcwd()
        new = past + "\\\\test_images"

        if os.path.exists(new):
            os.chdir(new)
        else:
            os.makedirs(new)
            os.chdir(new)
        os.rename(new_file_name, os.getcwd() + "\\" + fname)
        cnt = 0
        while os.path.exists("image{}.jpg".format(cnt)):
            cnt += 1
        os.rename(fname, "image{}.jpg".format(cnt))

        im = Image.open("image{}.jpg".format(cnt))
        im = im.resize((250,250),Image.ANTIALIAS)
        self.load_image(cnt)
        im.close()

        os.chdir(past)

    def start_train(self):

        past = os.getcwd()
        os.chdir(os.getcwd() + "\\\\test_images")

        num_files = len([name for name in os.listdir('.') if os.path.isfile(name)])

        i = 0

        while i < num_files-1:
            if not os.path.exists("image{}.jpg".format(i)):
                j = i+1
                while j < 1000 and not os.path.exists("image{}.jpg".format(j)):
                    j+=1
                os.rename("image{}.jpg".format(j),"image{}.jpg".format(i))
            i+=1
        os.chdir(past)
        print("All went well after pretraining processing.")

        self.training()


    def training(self):

        if tf.__version__ < '1.4.0':
            raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')
        print(2)

        # What model to download.
        MODEL_NAME = 'raspberrpi2_image'



        # Path to frozen detection graph. This is the actual model that is used for the object detection.
        PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

        # List of the strings that is used to add correct label for each box.
        PATH_TO_LABELS = os.path.join('training', 'object-detection.pbtxt')

        NUM_CLASSES = 1

        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                    use_display_name=True)
        category_index = label_map_util.create_category_index(categories)

        def load_image_into_numpy_array(image):
            (im_width, im_height) = image.size
            return np.array(image.getdata()).reshape(
                (im_height, im_width, 3)).astype(np.uint8)

        # For the sake of simplicity we will use only 2 images:
        # image1.jpg
        # image2.jpg
        # If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
        PATH_TO_TEST_IMAGES_DIR = 'test_images'
        TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(0, 1)]

        # Size, in inches, of the output images.
        IMAGE_SIZE = (12, 8)
        print(3)

        def run_inference_for_single_image(image, graph):
            with graph.as_default():
                with tf.Session() as sess:
                    # Get handles to input and output tensors
                    ops = tf.get_default_graph().get_operations()
                    all_tensor_names = {output.name for op in ops for output in op.outputs}
                    tensor_dict = {}
                    for key in [
                        'num_detections', 'detection_boxes', 'detection_scores',
                        'detection_classes', 'detection_masks'
                    ]:
                        tensor_name = key + ':0'
                        if tensor_name in all_tensor_names:
                            tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                                tensor_name)
                    if 'detection_masks' in tensor_dict:
                        # The following processing is only for single image
                        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                            detection_masks, detection_boxes, image.shape[0], image.shape[1])
                        detection_masks_reframed = tf.cast(
                            tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                        # Follow the convention by adding back the batch dimension
                        tensor_dict['detection_masks'] = tf.expand_dims(
                            detection_masks_reframed, 0)
                    image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

                    # Run inference
                    output_dict = sess.run(tensor_dict,
                                           feed_dict={image_tensor: np.expand_dims(image, 0)})

                    # all outputs are float32 numpy arrays, so convert types as appropriate
                    output_dict['num_detections'] = int(output_dict['num_detections'][0])
                    output_dict['detection_classes'] = output_dict[
                        'detection_classes'][0].astype(np.uint8)
                    output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
                    output_dict['detection_scores'] = output_dict['detection_scores'][0]
                    if 'detection_masks' in output_dict:
                        output_dict['detection_masks'] = output_dict['detection_masks'][0]
            return output_dict

        for image_path in TEST_IMAGE_PATHS:
            image = Image.open(image_path)
            # the array based representation of the image will be used later in order to prepare the
            # result image with boxes and labels on it.
            image_np = load_image_into_numpy_array(image)
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            # Actual detection.
            output_dict = run_inference_for_single_image(image_np, detection_graph)
            # Visualization of the results of a detection.
            vis_util.visualize_boxes_and_labels_on_image_array(
                image_np,
                output_dict['detection_boxes'],
                output_dict['detection_classes'],
                output_dict['detection_scores'],
                category_index,
                instance_masks=output_dict.get('detection_masks'),
                use_normalized_coordinates=True,
                line_thickness=8)
            plt.figure(figsize=IMAGE_SIZE)
            plt.imshow(image_np)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()
