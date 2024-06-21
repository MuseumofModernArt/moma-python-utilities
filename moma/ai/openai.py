import openai
import os

OPENAI_API_KEY=os.getenv('OPENAI_API_KEY_ENV')
DEFAULT_MODEL="gpt-4o"

def gpt4_getdesc(prompt_txt, base64_image, api_key=None, model=DEFAULT_MODEL):
    text, error = gpt4_getdesc_with_error(prompt_txt, base64_image, api_key, model)
    if text is None:
        return error
    return text

def gpt4_getdesc_with_error(prompt_txt, base64_image, api_key=None, model=DEFAULT_MODEL):
    error = None
 
    if base64_image is None:
        return None, "Error processing URL"
    else: 
        if api_key is None:
            api_key = OPENAI_API_KEY

        openai.api_key = api_key

        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt_txt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            return response['choices'][0]['message']['content'], None
        except openai.error.APIError as e:
            error = f"Error processing URL: An API error occurred: {e}"
        except openai.error.OpenAIError as e:
            error = f"Error processing URL: An OpenAI error occurred: {e}"
        except Exception as e:
            error = f"Error processing URL: An unexpected error occurred: {e}"
    return None, error
