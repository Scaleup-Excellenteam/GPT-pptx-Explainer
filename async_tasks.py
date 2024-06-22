import asyncio
from ai_api import generate_summary

async def fetch_summary(ai_key: str, slide_text: str) -> str:
    """
    Fetch a summary for a slide using the OpenAI API.

    Args:
        ai_key (str): The OpenAI API key.
        slide_text (str): The text content of the slide.

    Returns:
        str: The generated summary.
    """
    return await generate_summary(ai_key, slide_text)

async def process_slide(ai_key: str, counter: int, slide_text: str) -> tuple[int, str]:
    """
    Process a single slide by generating its summary.

    Args:
        ai_key (str): The OpenAI API key.
        counter (int): The slide number.
        slide_text (str): The text content of the slide.

    Returns:
        tuple[int, str]: A tuple containing the slide number and the generated summary.
    """
    try:
        print(f"Processing task for slide {counter}...")
        summary = await fetch_summary(ai_key, slide_text)
        return (counter, summary)
    except asyncio.CancelledError:
        print(f"Task for slide {counter} was cancelled.")
        return (counter, "Task was cancelled.")
    except Exception as e:
        print(f"Error processing task for slide {counter}: {e}")
        return (counter, f"Error summarizing slide: {e}")

async def process_presentation(slides_text: list[tuple[int, str]], ai_key: str) -> dict[int, str]:
    """
    Process all slides in a presentation by generating summaries for each.

    Args:
        slides_text (list[tuple[int, str]]): A list of tuples, each containing a slide number and its text content.
        ai_key (str): The OpenAI API key.

    Returns:
        dict[int, str]: A dictionary where the keys are slide numbers and the values are the generated summaries.
    """
    tasks = [process_slide(ai_key, counter, slide_text) for counter, slide_text in slides_text]
    summaries = await asyncio.gather(*tasks)
    return {counter: summary for counter, summary in summaries}
