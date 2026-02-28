import cv2
import numpy as np
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

# Load model ONCE when server starts (not every request)
print("Loading enhancement model...")

model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64,
                num_block=23, num_grow_ch=32, scale=4)

upsampler = RealESRGANer(
    scale=4,
    model_path='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth',
    model=model,
    tile=400,        # ← splits image into tiles, much faster on CPU
    tile_pad=10,
    pre_pad=0,
    half=False
)

print("Enhancement model ready!")

def enhance_image(image_bytes: bytes) -> bytes:
    print("Enhancing image...")

    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Resize input to max 500px before enhancing — much faster
    h, w = img.shape[:2]
    max_size = 500
    if max(h, w) > max_size:
        scale = max_size / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))
        print(f"Resized to {img.shape[1]}x{img.shape[0]} for faster processing")

    output, _ = upsampler.enhance(img, outscale=2)  # ← 2x instead of 4x, way faster
    
    _, buffer = cv2.imencode('.png', output)
    print("Enhancement done!")
    return buffer.tobytes()