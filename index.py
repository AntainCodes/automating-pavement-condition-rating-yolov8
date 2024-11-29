import torch
from ultralytics import YOLO
import mysql.connector
model = YOLO("model.pt")
class_labels = {
    0: 'D1', 1: 'D10', 2: 'D11', 3: 'D12', 4: 'D13',
    5: 'D2', 6: 'D3', 7: 'D4', 8: 'D5', 9: 'D6',
    10: 'D7', 11: 'D8', 12: 'D9'
}
results = model.predict(source="Videos/2.mp4", show=True)
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1234",
    database="shahjee3"
)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS shahjee3.YOLOv8_Output 
    (
        id INT AUTO_INCREMENT PRIMARY KEY,
        image_name VARCHAR(255),
        class_label VARCHAR(255),
        confidence VARCHAR(255),
        severity_level VARCHAR(255)
    );
''')

cursor.execute('''
    DELETE From shahjee3.YOLOv8_Output;
''')

high_threshold = 0.75
medium_threshold = 0.50
# Iterate over the results and insert them into the database
for idx, frame_results in enumerate(results):
    for bbox in frame_results.boxes:
        conf_str = "{:.4f}".format(bbox.conf.item())
        if conf_str > str(high_threshold):
            severity = "High"
        elif conf_str > str(medium_threshold):
            severity = "Medium"
        else:
            severity = "Low"
        print((
            idx,
            class_labels[bbox.cls.item()],
            conf_str,
            str(severity)))
        cursor.execute('''
            INSERT INTO shahjee3.YOLOv8_Output (image_name, class_label, confidence, severity_level)
            VALUES (%s, %s, %s, %s);
        ''', (
            idx,
            class_labels[bbox.cls.item()],
            conf_str,
            str(severity)
        ))
conn.commit()
conn.close()