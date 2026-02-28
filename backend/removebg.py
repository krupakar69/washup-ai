from rembg import remove, new_session
from PIL import Image
import io

print("Loading rembg model...")
session = new_session("isnet-general-use")
print("Rembg model ready!")

def remove_background(image_bytes: bytes) -> bytes:
    print("Removing background...")

    input_image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")

    output = remove(
        input_image,
        session=session,
        alpha_matting=False,
        post_process_mask=True
    )

    if output.mode != "RGBA":
        output = output.convert("RGBA")

    output_bytes = io.BytesIO()
    output.save(output_bytes, format="PNG", optimize=False)
    output_bytes.seek(0)
    print("Done!")
    return output_bytes.getvalue()