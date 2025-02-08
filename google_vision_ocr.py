import io
from google.cloud import vision

def extract_text_with_google_vision(image_path):
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(f"Google Vision API error: {response.error.message}")

    full_text = texts[0].description if texts else ""
    lines = [line.strip() for line in full_text.split('\n') if line.strip()]
    return lines