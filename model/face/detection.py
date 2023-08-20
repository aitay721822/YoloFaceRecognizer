from ultralytics import YOLO
from PIL import Image

class FaceDetector:
    
    def __init__(self, model_path: str) -> None:
        self.model = YOLO(model_path, task='detect')
        self.config = {}
        
    def apply_config(self, overwrite: dict):
        self.config.update(overwrite)
    
    def detect(self, image_path: str, **kwargs):
        results = self.model.predict(image_path, **kwargs)
        for result in results:
            if result.boxes is None or len(result.boxes) == 0:
                continue
            
            for coords in result.boxes.xyxy:
                yield result.path, result.orig_img[:, :, ::-1], coords.tolist()
                
    def detect_face(self, image_path: str):
        for path, image, coord in self.detect(image_path, **self.config):
            yield path, Image.fromarray(image, 'RGB').crop(tuple(coord))