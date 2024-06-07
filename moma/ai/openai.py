import openai
import os

OPENAI_API_KEY=os.getenv('OPENAI_API_KEY_ENV')

def gpt4_getdesc(prompt_txt, base64_image, api_key=None, model="gpt-4o"):
    image_desc=""
        
    if base64_image is None:
      return("Error processing URL")
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
        image_desc = response['choices'][0]['message']['content']
      except openai.error.APIError as e:
        image_desc = f"Error processing URL: An API error occurred: {e}"
      except openai.error.OpenAIError as e:
        image_desc = f"Error processing URL: An OpenAI error occurred: {e}"
      except Exception as e:
        image_desc = f"Error processing URL: An unexpected error occurred: {e}"
    return(image_desc)
