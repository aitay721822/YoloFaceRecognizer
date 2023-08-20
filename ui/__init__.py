
import os
from PyQt5.QtWidgets import QApplication
from .image_select import ImageLabelingApp

def build_datasets(unlabel_path: str, dataset_path: str):
    if not os.path.exists(dataset_path):
        os.mkdir(dataset_path)
    
    def label_callback(image_label_map):
        for image, label in image_label_map.items():
            if label:
                classes_path = os.path.join(dataset_path, label)
                if not os.path.exists(classes_path):
                    os.mkdir(classes_path)
                    
                image_name = os.path.basename(image)
                os.rename(image, os.path.join(classes_path, image_name))
        
    app = QApplication([])
    image_labeling_app = ImageLabelingApp(unlabel_path, label_callback)
    image_labeling_app.show()
    app.exec()
    