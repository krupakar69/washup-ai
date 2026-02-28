from rembg import remove
from PIL import Image
import io

def remove_background(image_bytes: bytes) -> bytes:
    print("Starting background removal...")
    input_image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    print("Image loaded, running rembg...")
    output_image = remove(input_image)
    print("Done! Sending result...")
    output_bytes = io.BytesIO()
    output_image.save(output_bytes, format="PNG")
    return output_bytes.getvalue()