import imghdr
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QScrollArea, QListWidget, QSizePolicy,QSpacerItem
from PyQt5.QtGui import QPixmap

class ImageLabelingApp(QMainWindow):
    def __init__(self, image_paths: list, label_callback=None):
        super().__init__()
        
        self.label_callback = label_callback
        self.initUI(image_paths)

    def initUI(self, image_paths):
        self.setWindowTitle("資料集建構工具")
        self.setGeometry(100, 100, 800, 400)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)

        # 左佈局
        left_widget = QWidget(self)
        left_layout = QVBoxLayout(left_widget)

        self.image_list = QListWidget()
        self.image_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.prev_button = QPushButton("上一張")
        self.next_button = QPushButton("下一張")
        left_layout.addWidget(self.image_list)
        left_layout.addWidget(self.prev_button)
        left_layout.addWidget(self.next_button)

        self.prev_button.clicked.connect(self.show_previous_image)
        self.next_button.clicked.connect(self.show_next_image)

        left_layout.addStretch()

        # 右佈局
        right_widget = QWidget(self)
        right_layout = QVBoxLayout(right_widget)

        self.image_display = QLabel()
        self.image_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_input = QLineEdit()
        self.label_combobox = QComboBox()
        self.save_button = QPushButton("保存")

        right_layout.addWidget(self.image_display)
        right_layout.addWidget(QLabel("選擇或輸入標籤:"))
        right_layout.addWidget(self.label_combobox)
        right_layout.addWidget(self.label_input)
        right_layout.addWidget(self.save_button)

        right_layout.addStretch()

        self.save_button.clicked.connect(self.save_label)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.image_display)

        main_layout.addWidget(left_widget)
        main_layout.addWidget(scroll_area)
        main_layout.addWidget(right_widget)
        
        self.image_list.itemDoubleClicked.connect(self.navigate_to_image)

        self.image_paths = []
        self.image_label_map = {}
        self.load_image(image_paths)

    def load_image(self, image_paths):
        self.image_paths = [os.path.join(image_paths, f) for f in os.listdir(image_paths) if imghdr.what(os.path.join(image_paths, f))]
        self.image_list.addItems(self.image_paths)
        self.current_image_index = 0
        self.show_image()

    def show_image(self):
        if self.current_image_index >= 0 and self.current_image_index < len(self.image_paths):
            image_path = self.image_paths[self.current_image_index]
            pixmap = QPixmap(image_path)
            self.image_display.setPixmap(pixmap.scaled(self.image_display.size(), aspectRatioMode=1, transformMode=0))
            self.image_list.setCurrentRow(self.current_image_index)
            self.label_input.setText(self.image_label_map.get(image_path, ""))

    def show_previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image()

    def show_next_image(self):
        if self.current_image_index < len(self.image_paths) - 1:
            self.current_image_index += 1
            self.show_image()
            
    def updateHistoryCombo(self):
        self.label_combobox.clear()
        self.label_combobox.addItems(sorted(set([v for k, v in self.image_label_map.items()])))
        
    def save_label(self):
        selected_image = self.image_list.currentItem()
        
        combo_text = self.label_combobox.currentText()
        label_text = self.label_input.text() if self.label_input.text() else combo_text
        self.label_input.clear()
        
        if selected_image and label_text:
            image_path = selected_image.text()
            self.image_label_map[image_path] = label_text
            if len(self.image_label_map) == len(self.image_paths):
                if self.label_callback:
                    self.label_callback(self.image_label_map)
                self.close()
                
        self.updateHistoryCombo()
        self.show_next_image()
            
    def navigate_to_image(self, item):
        selected_index = self.image_list.row(item)
        if selected_index >= 0 and selected_index < len(self.image_paths):
            self.current_image_index = selected_index
            self.show_image()