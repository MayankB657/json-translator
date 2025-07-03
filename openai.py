import json
import sys
import os
from openai import OpenAI
from time import sleep

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  


def translate_batch(batch, target_lang, model="gpt-3.5-turbo"):
    prompt = f"""
    Translate the following JSON values from English to {target_lang}.
    Return a valid JSON object. Do not change the keys. Only translate the values.

    {json.dumps(batch, indent=2)}
    """

    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": prompt
        }],
        temperature=0.2
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except Exception as e:
        print("❌ Error parsing model output as JSON:")
        print(content)
        raise e

def translate_json_values(input_file, target_lang, output_file, model="gpt-3.5-turbo"):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    translated = {}
    batch = {}
    count = 0

    for key, value in data.items():
        if isinstance(value, str):
            batch[key] = value
            count += 1
        else:
            translated[key] = value  # leave non-strings unchanged

        # translate in batches of 20
        if count == 20:
            translated.update(translate_batch(batch, target_lang, model))
            batch = {}
            count = 0
            sleep(1)

    if batch:
        translated.update(translate_batch(batch, target_lang, model))

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translated, f, ensure_ascii=False, indent=2)

    print(f"✅ Translated JSON saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python openai.py en.json italian")
        sys.exit(1)

    input_file = sys.argv[1]
    target_lang = sys.argv[2]
    output_file = f"{input_file.replace('en.json', f'.{target_lang.lower()}.json')}"
    translate_json_values(input_file, target_lang, output_file)