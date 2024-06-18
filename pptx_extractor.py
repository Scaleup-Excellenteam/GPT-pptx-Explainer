from pptx import Presentation
import os
import json
import asyncio
import ai_summery

async def fetch_summary(ai_key, slide_text):
    return await ai_summery.generate_summary(ai_key, slide_text)

# extract text from a slide
def extract_slide_text(slide, counter):
    slide_text = 'Slide number: ' + str(counter) + '\n'
    for shape in slide.shapes:
        if hasattr(shape, 'text'):
            slide_text += shape.text.strip() + '\n'
    return slide_text.strip()

# create async tasks for each slide
def create_tasks_from_presentation(presentation_path, ai_key):
    presentation = Presentation(presentation_path)
    tasks = []
    counter = 1
    for slide in presentation.slides:
        slide_text = extract_slide_text(slide, counter)
        if slide_text:
            task = asyncio.create_task(fetch_summary(ai_key, slide_text))
            tasks.append((counter, task))
        counter += 1
    return tasks

# async function to extract and summarize the text
async def extract_text_from_presentation(presentation_path, ai_key):
    tasks = create_tasks_from_presentation(presentation_path, ai_key)
    text = {}
    for counter, task in tasks:
        summary = await task
        text[counter] = summary
    return text

def text_to_json_file(sumerized_text, path):
    name = os.path.splitext(os.path.basename(path))[0]
    output_directory = os.path.join(os.getcwd(), 'outputs')
    os.makedirs(output_directory, exist_ok=True)
    
    json_file_name = os.path.join(output_directory, name + '.json')
    with open(json_file_name, 'w') as writer:
        json.dump(sumerized_text, writer, indent=4)
