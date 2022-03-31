# video_annotator
Run object detection on input video stream using YoLoV5 model
## Installation
Python version: >= 3.9  
Install `poetry`

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

Install project dependencies

```bash
poetry install
```

## Usage
Annotate live input video (from webcam)
```bash
poetry run python video_annotate.py live
```
Annotate Youtube video from input url
```bash
poetry run python video_annotate.py youtube --url https://www.youtube.com/watch\?v\=nSblgPqKtwo
```
### Model type
There are 5 different Yolo model types (`n`,`s`,`m`,`l`,`x`) that can be used with `--model-type` argument

```bash
poetry run python video_annotate.py live --model-type l
```
The model configuration and performance can be viewed from the table below

[assets]: https://github.com/ultralytics/yolov5/releases

[TTA]: https://github.com/ultralytics/yolov5/issues/303

|Model |size<br><sup>(pixels) |mAP<sup>val<br>0.5:0.95 |mAP<sup>val<br>0.5 |Speed<br><sup>CPU b1<br>(ms) |Speed<br><sup>V100 b1<br>(ms) |Speed<br><sup>V100 b32<br>(ms) |params<br><sup>(M) |FLOPs<br><sup>@640 (B)
|---                    |---  |---    |---    |---    |---    |---    |---    |---
|[YOLOv5n][assets]      |640  |28.0   |45.7   |**45** |**6.3**|**0.6**|**1.9**|**4.5**
|[YOLOv5s][assets]      |640  |37.4   |56.8   |98     |6.4    |0.9    |7.2    |16.5
|[YOLOv5m][assets]      |640  |45.4   |64.1   |224    |8.2    |1.7    |21.2   |49.0
|[YOLOv5l][assets]      |640  |49.0   |67.3   |430    |10.1   |2.7    |46.5   |109.1
|[YOLOv5x][assets]      |640  |50.7   |68.9   |766    |12.1   |4.8    |86.7   |205.7

### Confidence threshold
Confidence threshold can be set with `--confidence-threshold` argument. Only object with confidence higher than threshold will be visualized
```bash
poetry run python video_annotate.py youtube --confidence-threshold 0.4
```
## License
[MIT](https://choosealicense.com/licenses/mit/)