# YOLO Face Recognizer

## 簡述

使用 YOLO v8 做出的人臉檢測-分類模型

### 執行邏輯

1. 先用 detect task 將人臉的 bbox 擷取出來
2. 使用擷取出的人臉去訓練 yolov8l-cls model
3. 將訓練出來的 model 去做分類任務

## 引數說明

1. `--source`: 原始圖片所在資料夾
2. `--face-weight`: YOLOv8 臉部檢測模型
3. `--recognizer-weight`: YOLOv8 分類模型
4. `--skip-face-detection`: 省略臉部檢測的步驟
5. `--skip-build-datasets`: 省略建構資料集的步驟
6. `--train-set-split`: 測試集比例(0~1)，其他做為測試集保存
7. `--epochs`: 臉部分類要訓練幾個 epochs
8. `--batch`: batch size
9. `--image-size`: 圖片 resize 的尺寸
10. `--conf-threshold`: 檢測-分類的信心閥值
11. `--target`: 保存圖像的位置

## 使用方法

安裝好所有套件後執行下述指令即可執行

```bash
python main.py --source "圖片路徑" --conf-threshold 0.7
```
