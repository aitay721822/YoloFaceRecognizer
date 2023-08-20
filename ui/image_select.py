from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class ImageLabelingApp(QMainWindow):
    def __init__(self, image_paths: str, label_callback=None):
        super().__init__()
        self.initUI(image_paths)
        self.label_callback = label_callback

    def initUI(self, image_paths: str):
        self.setWindowTitle('圖片標籤工具')
        self.setGeometry(100, 100, 800, 600)

        self.current_image_index = 0
        self.image_paths = image_paths
        self.labels = []

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)

        self.input_label = QLineEdit(self)
        self.layout.addWidget(self.input_label)

        self.confirm_button = QPushButton('確認', self)
        self.confirm_button.clicked.connect(self.confirmLabel)
        self.layout.addWidget(self.confirm_button)
        
        self.history_combo = QComboBox(self)
        self.layout.addWidget(self.history_combo)
        
        self.central_widget.setLayout(self.layout)
        self.current_image_index = 0
        self.showCurrentImage()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.confirm_button()

    def updateHistoryCombo(self):
        self.history_combo.clear()
        self.history_combo.addItems(set(self.labels))

    def nextImage(self):
        if self.current_image_index < len(self.image_paths) - 1:
            self.current_image_index += 1
            self.showCurrentImage()

    def showCurrentImage(self):
        if self.image_paths:
            image_path = self.image_paths[self.current_image_index]
            pixmap = QPixmap(image_path).scaled(600, 600, aspectRatioMode=1)
            self.image_label.setPixmap(pixmap) 

    def confirmLabel(self):
        label = self.input_label.text()
        if self.history_combo.currentText():
            label = self.history_combo.currentText()
            
        if label:
            self.labels.append(label)
            self.nextImage()
            self.updateHistoryCombo()
        
        if len(self.labels) == len(self.image_paths):
            if self.label_callback:
                self.label_callback(self.labels)
                self.close()
    
    
