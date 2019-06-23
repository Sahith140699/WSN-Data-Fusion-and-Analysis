fromimport requests
import time
from picamera import PiCamera

url1 = 'http://192.168.0.4:8090/rest/things/hue%3A0210%3A001788afee6e%3A2'


camera = PiCamera()
prev_image = ""
pres_image = ""



status1 = "\"ONLINE\""
while True:
    prev_status1 = status1
    r1 = requests.get(url1)
    status1 = r1.text.split(",")[0].split(":")[2]
    print(status2)
    if(prev_status1 == "\"OFFLINE\"" and status1 == "\"ONLINE\""):
        print("Motion Detected by PIR sensor 1")
        prev_image = cv2.imread("/home/pi/Desktop/image.png",1)
        cv2.imwrite("/home/pi/Desktop/prev_image.png",prev_image)
        camera.start_preview()
        sleep(1)
        camera.capture('/home/pi/Desktop/image.png')
        camera.stop_preview()
        pres_image = cv2.imread("/home/pi/Desktop/image.png",0)
        
