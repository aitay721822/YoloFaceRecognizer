from dataclasses import asdict, dataclass

@dataclass
class RecognizerConfig:
    # Model Path
    model_path: str = 'weights/recognizer.pt'
    
    # training parameters
    epochs: int = 100
    batch_size: int = 32
    image_size: int = 640

    # confidence threshold
    conf_threshold: float = 0.5

    def yolo_config(self):
        return {
            'conf': self.conf_threshold,
            'imgsz': self.image_size,
            'batch': self.batch_size,
            'epochs': self.epochs,
        }
