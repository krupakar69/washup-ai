import cv2
import numpy as np
import os

print("Loading colorization model...")

prototxt = os.path.join(os.path.dirname(__file__), "models/colorization_deploy_v2.prototxt")
caffemodel = os.path.join(os.path.dirname(__file__), "models/colorization_release_v2.caffemodel")
pts_npy = os.path.join(os.path.dirname(__file__), "models/pts_in_hull.npy")

net = cv2.dnn.readNetFromCaffe(prototxt, caffemodel)
pts = np.load(pts_npy)

class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

print("Colorization model ready!")

def colorize_image(image_bytes: bytes) -> bytes:
    print("Colorizing image...")

    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert to higher quality LAB color space
    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_BGR2LAB)

    # Use larger input size for better detail (320 instead of 224)
    resized = cv2.resize(lab, (320, 320))
    L = cv2.split(resized)[0]
    L -= 50

    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

    L_original = cv2.split(lab)[0]
    colorized = np.concatenate((L_original[:, :, np.newaxis], ab), axis=2)
    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2BGR)

    # Boost color saturation for more vibrant results
    colorized_uint8 = (np.clip(colorized, 0, 1) * 255).astype("uint8")
    hsv = cv2.cvtColor(colorized_uint8, cv2.COLOR_BGR2HSV).astype("float32")
    hsv[:, :, 1] *= 1.5  # boost saturation by 50%
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
    colorized_uint8 = cv2.cvtColor(hsv.astype("uint8"), cv2.COLOR_HSV2BGR)

    _, buffer = cv2.imencode('.png', colorized_uint8)
    print("Colorization done!")
    return buffer.tobytes()