import base64
from pathlib import Path

def png_to_base64_string(image_path):
    # 1. Open the image file in binary read mode ('rb')
    with open(image_path, "rb") as image_file:
        
        # 2. Read the binary data and encode it to base64
        base64_bytes = base64.b64encode(image_file.read())
        
        # 3. Decode bytes to a UTF-8 string so it can be printed
        base64_string = base64_bytes.decode('utf-8')
                
        return base64_string

favicon_data = f'data:image/png;base64,{png_to_base64_string(Path(__file__).parent.parent.parent / "resources/img/favicon.png")}'

