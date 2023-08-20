
import os
import imghdr
from PyQt5.QtWidgets import QApplication
from .image_select import ImageLabelingApp

def build_datasets(unlabel_path: str, dataset_path: str):
    if not os.path.exists(dataset_path):
        os.mkdir(dataset_path)
    
    image_paths = [os.path.join(unlabel_path, image_name) for image_name in os.listdir(unlabel_path) if imghdr.what(os.path.join(unlabel_path, image_name))]
    def label_callback(labels: list):
        for i, image_path in enumerate(image_paths):
            if labels[i]:
                image_name = os.path.basename(image_path)
                os.rename(image_path, os.path.join(dataset_path, labels[i], image_name))
        
    app = QApplication([])
    image_labeling_app = ImageLabelingApp(image_paths, label_callback)
    image_labeling_app.show()
    app.exec()