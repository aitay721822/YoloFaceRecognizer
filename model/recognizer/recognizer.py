import os
from ultralytics import YOLO
from model.recognizer.config import RecognizerConfig

PRETRAINED_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'weights', 'yolov8l-cls.pt')

class Recognizer:
    
    def __init__(self, conf: RecognizerConfig) -> None:
        self.is_training = os.path.exists(conf.model_path)
        self.backend = YOLO(conf.model_path if self.is_training else PRETRAINED_MODEL_PATH, task='classify')
        self.config = conf
        
    def recognize(self, image_path: str, **kwargs):
        if not self.is_training:
            raise RuntimeError('Model is not trained yet.')
        
        overwrite = self.config.yolo_config()
        overwrite.update(kwargs)
        results = self.backend(image_path, **overwrite)
        for result in results:
            yield result.path, result.names, result.probs.top1, result.probs.top1conf
    
    def train(self, datasets_path: str, **kwargs):
        overwrite = self.config.yolo_config()
        overwrite.update(kwargs)
        self.backend.train(data=datasets_path, **overwrite)
        self.backend.export(format='torchscript')
        self.is_training = True
    
