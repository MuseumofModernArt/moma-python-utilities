import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Image

DEFAULT_MODEL="gemini-1.0-pro-vision"

def gemini_getdesc(short_prompt_txt, image_path, model=DEFAULT_MODEL):
    text, error = gemini_getdesc_with_error(short_prompt_txt, image_path, model)
    if text is None:
        return error
    return text

def gemini_getdesc_with_error(short_prompt_txt, image_path, model=DEFAULT_MODEL):
    PROJECT_ID = "moma-dw"
    REGION = "us-central1"

    vertexai.init(project=PROJECT_ID, location=REGION)

    IMAGE_FILE = "https://moma-images.museum.moma.org/Size3/Images/3_1943_CCCR.jpg"
    IMAGE_FILE = "./images/1182_2012_CCCR.jpeg"
    IMAGE_FILE = image_path

    try:
        #use below for larger images that might need to be resized. Need to use PIL also
        #with Image.open(image_path) as img:
            #rgb_im = img.convert('RGB')
            #resized_image = rgb_im.resize((400, 300))  # Resize the image - gemini needs small images

            #buffered = io.BytesIO()
            #resized_image.save(buffered, format="JPEG")
            #image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        #image = image_base64
        
        # If image is a file (not URL) load image directly
        image = Image.load_from_file(IMAGE_FILE)

        generative_multimodal_model = GenerativeModel(model)
        response = generative_multimodal_model.generate_content([short_prompt_txt, image])
    

        #print(response)
        # Assuming 'candidates', 'content', and 'parts' are lists
        text_content=None
        for candidate in response.candidates:
            for part in candidate.content.parts:
                text_content = part.text
                #print(text_content)
                return text_content, None
        
    except Exception as e:
        return  None, f"ERROR: Gemini failed to process: {e}"