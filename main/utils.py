import os
import openai

def get_translation(text_to_translate: str, target_language: str) -> str:
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    
    system_prompt = f"You are a professional translator. Translate the following text into {target_language}. Respond only with the translated text, without any additional comments or explanations."

    try:
        response = openai.responses.create(
            model="gpt-4.1",
            instructions=system_prompt,
            input=text_to_translate,
        )
        return response.output_text
    except Exception as e:
        print(f"Translate error: {e}")
        return f"An error occurred during translation."