import cv2
import pytesseract

def preprocess_image(image_path):
    # Load image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Resize the image to enlarge the text (tweak scale factors as needed)
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # Apply Gaussian blur to reduce noise
    image = cv2.GaussianBlur(image, (5, 5), 0)
    
    # Adaptive thresholding to create a binary image
    processed = cv2.adaptiveThreshold(
        image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    return processed

def extract_text_from_image(image_path):
    processed_image = preprocess_image(image_path)
    
    # Use a custom Tesseract configuration
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, lang="eng", config=custom_config)
    
    # Split text into lines and filter out very short or noisy lines
    book_titles = [line.strip() for line in text.split("\n") if len(line.strip()) > 2]
    return book_titles