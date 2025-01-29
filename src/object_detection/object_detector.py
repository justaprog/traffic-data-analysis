from ultralytics import YOLO

# Load a model
#model = YOLO("yolo11n.yaml")  # build a new model from YAML
model = YOLO("src/object_detection/yolo11n.pt")  # load a pretrained model (recommended for training)
#model = YOLO("yolo11n.yaml").load("yolo11n.pt")  # build from YAML and transfer weights

# Train the model
#results = model.train(data="coco8.yaml", epochs=100, imgsz=640)
#metrics = model.val()
def object_detector(images):
    # return a list of Results objects 
    results = model([images])

    # Process results list
    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
        masks = result.masks  # Masks object for segmentation masks outputs
        keypoints = result.keypoints  # Keypoints object for pose outputs
        probs = result.probs  # Probs object for classification outputs
        obb = result.obb  # Oriented boxes object for OBB outputs
        result.show()  # display to screen
        result.save(filename="res/object_detection/result.jpg")  # save to disk

if __name__ == "__main__":
    object_detector("data/object_detection/trains.jpg")