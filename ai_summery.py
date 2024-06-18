import openai
import asyncio


def load_api_key(filepath):
    with open(filepath, "r") as file:
        return file.read().strip()


async def generate_summary(api_key, text, timeout=5):
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
        return summary
    except asyncio.TimeoutError:
        return "Summary generation timed out."
