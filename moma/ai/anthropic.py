import anthropic
import os

ANTHROPIC_API_KEY=os.getenv("ANTHROPIC_API_KEY_ENV")

def claude_getdesc(short_prompt_txt, base64_image, api_key=None, model="claude-3-opus-20240229"):
    try:
        if api_key is None:
            api_key = ANTHROPIC_API_KEY

        client = anthropic.Anthropic(api_key=api_key)

        message = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64_image,
                            },
                        },
                        {
                            "type": "text",
                            "text": short_prompt_txt
                        }
                    ],
                }
            ],
        )
        
        return message.content[0].text

    except Exception as e:
        return f"ERROR: Claude failed to process: {e}"