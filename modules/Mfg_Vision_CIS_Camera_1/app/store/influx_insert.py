from datetime import datetime
import time
import json
from influxdb import InfluxDBClient

class InsertInference():

    def __init__(self, detection_count, inference):
        now = datetime.now()
        self.model_name = str(inference['model_name'])
        self.object_detected = str(inference['object_detected'])
        self.camera_id = str(inference['camera_id'])
        self.camera_name = str(inference['camera_name'])
        self.raw_image_name = str(inference['raw_image_name'])
        self.raw_image_path = str(inference['raw_image_local_path'])
        self.annotated_image_name = str(inference['annotated_image_name'])
        self.annotated_image_path = str(inference['annotated_image_path'])
        self.inferencing_time = str(inference['inferencing_time'])
        self.created = now
        self.unique_id = str(inference['unique_id'])
        self.detections = inference['detected_objects']
        self.detection_count = detection_count

        self.tag_name = "none"
        self.tag_id = "-1"
        self.probability = "-1.0"
        self.bbox = "none"
    

        self.t_begin = int(time.time() * 1000)
        self.t_end = time.time()
        self.t_insert = 0

        print(f"SQL package:  {json.dumps(inference)}")
        self.client = InfluxDBClient(host='localhost', port=8088)

        self.create_record()
    
    def create_record(self):
        data = []
        current_point_time = self.t_begin
        for i in range(self.detection_count - 1):
            self.tag_id = self.detections[i]['labelId']
            self.tag_name = self.detections[i]['labelName']
            self.probability = round(self.detections[i]['probability'],2)
            self.bbox = self.detections[i]['bbox']
            data.append(
                {
                    "model_name": self.model_name, 
                    "object_detected": self.object_detected, 
                    "camera_id": self.camera_id, 
                    "camera_name": self.camera_name, 
                    "raw_image_name": self.raw_image_name, 
                    "raw_image_local_path": self.raw_image_path,
                    "annotated_image_name": self.annotated_image_name, 
                    "annotated_image_path": self.annotated_image_path, 
                    "inferencing_time": self.inferencing_time, 
                    "created": self.created, 
                    "tag_name": self.tag_name, 
                    "tag_id": self.tag_id, 
                    "probability": self.probability, 
                    "bbox": self.bbox,
                    "unique_id":  self.unique_id,
                    "time": current_point_time
                }
            )
        
        client_write_start_time = time.perf_counter()

        self.client.write_points(data, database='defectdb', time_precision='ms', batch_size=1000, protocol='json')

        client_write_end_time = time.perf_counter()

        print("InfluxDB write time: {time}s".format(time=client_write_end_time - client_write_start_time))

        
