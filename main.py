import shutil
import imghdr
from model import FaceDetector, Recognizer, RecognizerConfig
from ui import build_datasets
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=str, required=True, help='source')
parser.add_argument('--face-weight', type=str, default='model/weights/yolov8n-face.pt', help='face weight path')
parser.add_argument('--recognizer-weight', type=str, default='model/weights/recognizer.torchscript', help='recognizer weight path')
parser.add_argument('--skip-face-detection', action='store_true', help='skip face detection')
parser.add_argument('--skip-build-datasets', action='store_true', help='skip build datasets')
parser.add_argument('--train-set-split', type=float, default=0.8, help='trainset split ratio')
parser.add_argument('--epochs', type=int, default=20, help='epochs')
parser.add_argument('--batch', type=int, default=16, help='batch size')
parser.add_argument('--image-size', type=int, default=640, help='image size')
parser.add_argument('--conf-threshold', type=float, default=0.8, help='confidence threshold')
parser.add_argument('--target', type=str, default='results/face', help='target')

def build(unlabeled_path: str, target_path: str, ratio: float):
    train_size = int(len(os.listdir(unlabeled_path)) * ratio)
    train_set = unlabeled_path[:train_size]
    test_set = unlabeled_path[train_size:]
    build_datasets(train_set, os.path.join(target_path, 'train'))
    build_datasets(test_set, os.path.join(target_path, 'test'))

def face_detection(weights_path: str, source_path: str, target_path: str, conf_threshold: float):
    face = FaceDetector(weights_path)
    face.apply_config({
        'conf': conf_threshold,
    })
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    image_path_map = {}
    for i, (path, f) in enumerate(face.detect_face(source_path)):
        image_path_map[f'{i}.jpg'] = path
        f.save(os.path.join(target_path, f'{i}.jpg'))
    return image_path_map
    
def main():
    args = parser.parse_args()
    
    project, name = 'logs', 'recognizer'
    unlabeled_path = 'datasets/unlabeled'
    datasets_path = 'datasets/face'
    
    if os.path.exists(unlabeled_path):
        shutil.rmtree(unlabeled_path)
    if os.path.exists(datasets_path):
        shutil.rmtree(datasets_path)
    if os.path.exists(args.target):
        shutil.rmtree(args.target)
    
    if not args.skip_face_detection:
        image_path_map = face_detection(args.face_weight, args.source, unlabeled_path, args.conf_threshold)
        if not args.skip_build_datasets:
            build(unlabeled_path, datasets_path, args.train_set_split)
    else:
        image_path_map = {}
        for i, f in enumerate(os.listdir(args.source)):
            source, target = os.path.join(args.source, f), os.path.join(unlabeled_path, f'{i}.jpg')
            if imghdr.what(source) is not None:
                image_path_map[f'{i}.jpg'] = source
                shutil.copy(source, target)
    
    if not os.path.exists(args.target):
        os.makedirs(args.target)
    conf = RecognizerConfig(model_path=args.recognizer_weight,
                            epochs=args.epochs, 
                            batch_size=args.batch, 
                            conf_threshold=args.conf_threshold,
                            image_size=args.image_size)
    recognizer = Recognizer(conf)
    if not recognizer.is_training:
        recognizer.train(datasets_path, project=project, name=name)
        shutil.move(f'{project}/{name}/weights/best.torchscript', args.recognizer_weight)
        
    for path, names, predict_label, predict_conf in recognizer.recognize(unlabeled_path):
        print(f'{path}: {names} ({predict_label}) ({predict_conf}))')
        filename = os.path.basename(path)
        if predict_conf.item() > args.conf_threshold:
            shutil.copy(image_path_map[filename], os.path.join(args.target, f'{names[predict_label]}_{predict_conf:.2f}_{filename}'))

if __name__ == '__main__':
    main()