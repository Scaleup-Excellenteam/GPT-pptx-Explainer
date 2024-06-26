from pptx import Presentation
import os
import json
import logging

logger = logging.getLogger('ExplainerLogger')
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))


def extract_slide_text(slide, counter) -> str:
    slide_text = f"Slide number: {counter}\n"
    for shape in slide.shapes:
        if hasattr(shape, 'text'):
            try:
                text = shape.text.strip()
                slide_text += text.encode('utf-8').decode('utf-8') + '\n'
            except UnicodeEncodeError:
                slide_text += "[Error: Unable to decode text]\n"
    return slide_text.strip()

def extract_text_from_presentation(presentation_path: str) -> list[tuple[int, str]]:
    if not os.path.isfile(presentation_path):
        raise FileNotFoundError(f"The presentation file '{presentation_path}' does not exist.")
    
    try:
        presentation = Presentation(presentation_path)
    except Exception as e:
        raise Exception(f"Failed to load presentation: {e}")

    slides_text = []
    counter = 1
    for slide in presentation.slides:
        slide_text = extract_slide_text(slide, counter)
        if slide_text:
            slides_text.append((counter, slide_text))
        counter += 1
    logger.info(f"Extracted text from {len(slides_text)} slides in {presentation_path}")
    return slides_text

def text_to_json_file(summarized_text: dict[int, str], path: str, output_dir: str) -> None:
    name = os.path.splitext(os.path.basename(path))[0]
    output_directory = output_dir
    print(f"Output directory: {output_directory}")  
    os.makedirs(output_directory, exist_ok=True)
    
    json_file_name = os.path.join(output_directory, name + '.json')
    print(f"JSON file name: {json_file_name}")  
    with open(json_file_name, 'w', encoding='utf-8') as writer:
        json.dump(summarized_text, writer, indent=4, ensure_ascii=False)
    logger.info(f"Summarized text saved to {json_file_name}")
    print(f"Summarized text saved to {json_file_name}")  

