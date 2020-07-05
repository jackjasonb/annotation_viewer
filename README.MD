# annotation viewer
物体検出データセットのアノテーションを確認するビュワー  
csvとCOCOに対応

## install
`pip install numpy opencv-python cython`  
`git clone https://github.com/cocodataset/cocoapi.git`  
`cd cocoapi/PythonAPI`  
`make`  
`make install`

## 使用例
`python coco_viewer.py ./hoge/coco -s anno_image`