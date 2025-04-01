from dotenv import load_dotenv
from google import genai
from models import VocabNote
from pydantic import BaseModel
import openai
import os
import data.prompts as prompts

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

FIELDS_PROMPT = """
TargetWord: The word you are generating fields for, this one I provide you already.
Translation: The translation for the TargetWord in English (if there are multiple translations just list them), keep it short
Gloss: The gloss of the TargetWord, keep it fairly short
"""

class Recipe(BaseModel):
  recipe_name: str
  ingredients: list[str]

def generate_vocab_text_fields(notes: list[VocabNote]) -> list[VocabNote]:
    target_words = [note.fields.TargetWord for note in notes]
    word_gen_prompt = build_vocabgen_prompt(notes[0].fields, target_words, notes[0].target_language)

    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=word_gen_prompt,
        config={
            'response_mime_type': 'application/json'
        }
    )

    # enriched_notes = parse_vocabgen_response(response.text)
    print(f"response.text: {response.text}")
    print(f"response.parsed: {response.parsed}")
    return True
        
def build_vocabgen_prompt(fields: list[str], words: list[str], lang: str) -> str:
    fields = FIELDS_PROMPT  # FIXME: remove once I have refactored VocabNoteFields
    prompt = prompts.vocabgen_prompt2.format(fields=fields, words=words, lang=lang)
    return prompt

def parse_vocabgen_response(raw_response: str) -> list[VocabNote]:
    # FIXME: parse JSON instead because Gemini is made for that
    lines = raw_response.strip().splitlines()
    if not lines:
        return []

    headers = lines[0].split("|")
    entries = []

    for line in lines[1:]:
        if not line.strip():
            continue
        values = line.split("|")
        if len(values) != len(headers):
            raise Exception("ERROR")
        entry = dict(zip(headers, values))
        entries.append(entry)

    print(entries)

    notes = []
    for entry in entries:
        notes.append(VocabNote("TEST", "korean", "english", entry))

    return notes

def call_openai():
    response = openai.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-4"
        store=True,
        messages=[
            # {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Tell me a joke about space."}
        ]
    )

    print(response)

def call_ollama():
    pass

if __name__ == "__main__":
    # call_openai()

    fields_to_generate = ['TargetWord', 'Fruit', 'Color', 'IDK...']
    words = ['비밀', '나무']
    # print(call_gemini(fields_to_generate, words, lang='Korean'))

    vocabgen_res = """TargetWord|Translation|Gloss
비밀|Secret|Something kept hidden or unknown
나무|Tree|A perennial woody plant"""
    
    print(parse_vocabgen_response(vocabgen_res)[0])