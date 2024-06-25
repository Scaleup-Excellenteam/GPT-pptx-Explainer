import openai
import asyncio
import os
import logging

logger = logging.getLogger('ExplainerLogger')

def load_api_key() -> str:
    """
    Load the OpenAI API key from environment variables.

    Returns:
        str: The OpenAI API key.
    """
    return os.getenv("OPENAI_API_KEY")

async def generate_summary(api_key: str, text: str, timeout: int = 15) -> str:
    """
    Generate a summary using the OpenAI GPT-3.5 API.

    Args:
        api_key (str): The OpenAI API key.
        text (str): The text to be summarized.
        timeout (int): Timeout for the API request in seconds.

    Returns:
        str: The generated summary or a timeout message if the request times out.
    """
    openai.api_key = api_key
    loop = asyncio.get_event_loop()
    try:
        response = await asyncio.wait_for(
            loop.run_in_executor(
                None,
                lambda: openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an assistant that helps computer science students summarize lectures from PPTX presentations "
                                       "so they can study efficiently and clearly. Provide concise information without headings or chapter titles. "
                                       "If there are important concepts mentioned for the first time, provide an explanation for them. "
                                       "If a concept is touched upon multiple times in the presentation, try to expand the explanation to make it educational.",
                        },
                        {"role": "user", "content": text},
                    ],
                ),
            ),
            timeout,
        )
        summary = response.choices[0].message["content"].strip()
        logger.info("Generated summary using OpenAI API")
        return summary
    except asyncio.TimeoutError:
        logger.error("Summary generation timed out")
        return "Summary generation timed out."
