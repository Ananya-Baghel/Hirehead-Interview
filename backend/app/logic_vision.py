import cv2
import numpy as np

# Using built-in Haar cascades
FACE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
EYE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

def image_metrics(img_bytes: bytes):
    arr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = FACE.detectMultiScale(gray, 1.15, 5)
    if len(faces) == 0:
        return {"face_detected": False, "eyes_ratio": None, "head_tilt_deg": None, "posture": "unknown"}

    (x,y,w,h) = max(faces, key=lambda f: f[2]*f[3])
    face = gray[y:y+h, x:x+w]
    eyes = EYE.detectMultiScale(face, 1.15, 5)

    eyes_ratio = None
    if len(eyes) >= 2:
        # Distance between first two detected eyes normalized by face width
        (x1,y1,w1,h1) = eyes[0]; (x2,y2,w2,h2) = eyes[1]
        c1 = np.array([x1+w1/2, y1+h1/2])
        c2 = np.array([x2+w2/2, y2+h2/2])
        dist = np.linalg.norm(c1-c2)
        eyes_ratio = float(dist / (w+1e-6))
        # head tilt estimate from eye line angle
        dy = (c2[1]-c1[1]); dx = (c2[0]-c1[0]); 
        angle = float(np.degrees(np.arctan2(dy, dx)))
    else:
        angle = None

    # crude posture heuristic using bounding box aspect
    posture = "attentive" if 0.8 < (h/(w+1e-6)) < 1.6 else "off-center"

    return {"face_detected": True, "eyes_ratio": eyes_ratio, "head_tilt_deg": angle, "posture": posture}
