from pptx import Presentation

def extract_text_from_presentation(presentation):
    text = ''
    counter = 0
    for slide in presentation.slides:
        slide_text = 'slide number: ' + str(counter) + '\n'
        counter += 1
        for shape in slide.shapes:
            if hasattr(shape, 'text'): # check if shape has text attribute
                slide_text += shape.text.strip() + '\n'
        if slide_text.strip(): # check if slide_text is not empty
            text += slide_text + '\n'
    return text

if __name__ == '__main__':
    prs = Presentation(r'final-exercise-DSH93\example_pptx.pptx')
    extracted_text = extract_text_from_presentation(prs)
    print(extracted_text)
