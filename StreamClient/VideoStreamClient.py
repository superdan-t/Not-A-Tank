import cv2
import imutils
import numpy as np
import imagezmq
image_hub = imagezmq.ImageHub()
while True:
    #host_name, image = image_hub.recv_image()
    #resized = imutils.resize(image, width=1280, height=720)
    host_name, jpg_buf = image_hub.recv_jpg()
    image = imutils.resize(cv2.imdecode(np.fromstring(jpg_buf, dtype='uint8'), -1), width=1280, height=720)
    cv2.imshow(host_name, image)
    cv2.waitKey(1)
    image_hub.send_reply(b'OK')
