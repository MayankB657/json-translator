# JSON Translator Tool

A simple tool to translate a JSON file from one language to another

## Features

- Best for create laravel multilanguage json files
- Translate a JSON file from one language to another
- List supported languages
- Only values are translated, not the keys

## Installation

```bash
pip install -r requirements.txt
```

## Running the Tool

```bash
python app.py en.json es
```

- `en.json` is the input file
- `es` is the target language (Spanish)

```bash
python app.py languages
```

- List supported languages

```bash
python openai.py en.json italian
```

- `en.json` is the input file
- `italian` is the target language
