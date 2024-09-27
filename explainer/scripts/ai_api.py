import openai
import asyncio
import os
import logging

logger = logging.getLogger('ExplainerLogger')

def load_api_key() -> str:
    return os.getenv("OPENAI_API_KEY")

async def generate_summary(api_key: str, text: str, timeout: int = 15) -> str:
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
