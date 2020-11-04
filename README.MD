# annotation viewer
OpenCVベースの物体検出データセットのアノテーションを確認するビュワー  
csvとCOCO formatに対応

## Install
```shell
pip install -r requirements.txt
git clone https://github.com/cocodataset/cocoapi.git
```
This code uses OpenCV Qt expanded. Please install qt library.

## Usage
### Bounding Box
If you use option `-s [save_dir]`, you can save result images at save_dir.

#### COCO

`python coco_viewer.py -i [image_dir] -a [annotation_json]`

#### CSV
You can use csv file format this:

`file_path,x1,y1,x2,y2,class_name`

Point(x1, y1) is top-left of bbox. Point(x2, y2) is bottom-right of bbox.
Usage:

`python csv_viewer.py -a [annotation_csv]`

### Segmentation

#### CSV
You can use csv file format this:

`file_path,x1,y1,x2,y2,x3,y3,......`

Usage:

`python csv_polygon_viewer.py -i [image_dir] -a [annotation_csv]`

