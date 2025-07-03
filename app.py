import json
import sys
from google.cloud import translate_v2 as translate

# Load Google credentials
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

def translate_text(text, target_lang, translator):
    if not text.strip():
        return text  # skip empty values
    result = translator.translate(text, target_language=target_lang)
    return result['translatedText']

def translate_json_values(input_file, target_lang, output_file):
    # Load original JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    translator = translate.Client()

    translated = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated[key] = translate_text(value, target_lang, translator)
        else:
            translated[key] = value  # keep as-is if not a string

    # Save translated JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translated, f, ensure_ascii=False, indent=2)

    print(f"✅ Translated JSON saved to {output_file}")

def list_supported_languages(target_lang="en"):
    translator = translate.Client()
    results = translator.get_languages(target_language=target_lang)
    print("🌍 Supported Languages:")
    for language in results:
        print(f"{language['language']} - {language['name']}")

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "languages":
        list_supported_languages()
    elif len(sys.argv) == 3:
        input_file = sys.argv[1]
        target_lang = sys.argv[2]
        output_file = f"{target_lang}.json"
        translate_json_values(input_file, target_lang, output_file)
    else:
        print("Usage:")
        print("  python app.py en.json es      # Translate JSON")
        print("  python app.py languages       # List supported languages")

