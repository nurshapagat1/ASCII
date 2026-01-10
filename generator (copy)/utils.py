from PIL import Image
import io

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def transform_to_ascii(image_file, new_width=100):
    # Load image from the uploaded file object
    img = Image.open(image_file)
    
    # Resize and maintain aspect ratio
    width, height = img.size
    aspect_ratio = height / width / 1.65
    new_height = int(new_width * aspect_ratio)
    img = img.resize((new_width, new_height))
    
    # Convert to grayscale
    img = img.convert("L")
    
    # Map pixels to characters
    pixels = img.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    
    # Construct rows
    ascii_img = "\n".join([characters[i:(i + new_width)] for i in range(0, len(characters), new_width)])
    return ascii_img