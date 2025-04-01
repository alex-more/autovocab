import csv
import uuid
import argparse

import anki_interface as anki
import ai_interface as ai
import image_generator as img_gen
from anki_models import VocabNote


"""
The main file for AutoVocab

Try to only keep the entry points of the program in here, and keep the core logic elsewhere
"""

TARGET_LANG = "Korean"
KNOWN_LANG = "English"

DECK_NAME = f"{TARGET_LANG} AutoVocab"
MODEL_NAME = f"{TARGET_LANG}-AutoVocab"
CARD_NAME = f"{TARGET_LANG}-AutoVocab"

CSV_FILE = "data/new_words.csv"


def generate_anki_notes_for_text(textblock: str) -> bool:
    """ Takes a block of text and generates Anki notes accordingly """
    pass

def generate_anki_notes_by_prompt(prompt: str) -> bool:
    """ Takes a prompt and generates Anki notes accordingly """
    pass

def generate_anki_note_for_word(word: str) -> bool:
    """ Takes a foreign word and generates an Anki note for it """
    vocab_fields = { 'TargetWord': word }
    note = VocabNote(MODEL_NAME, TARGET_LANG, KNOWN_LANG, vocab_fields)

    note = bulk_enrich_vocab_text_fields([note]).pop()
    
    note = enrich_vocab_note(note)

    if anki.can_add_note(DECK_NAME, note):
        return anki.add_note(DECK_NAME, note.model_name, note.fields)
    else:
        return False

def bulk_enrich_vocab_text_fields(notes: list[VocabNote]) -> list[VocabNote]:
    """ Takes a list of VocabNotes and fills in the text fields using LLM """
    pass

def enrich_vocab_note(note: VocabNote) -> VocabNote:
    """ Takes a VocabNote and fills in all the missing fields """
    pass

def create_anki_notes(filename: str):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            vocab_fields = {key:row[key] for key in VocabNote.get_field_names()}
            note = VocabNote(MODEL_NAME, TARGET_LANG, KNOWN_LANG, vocab_fields, row['SearchPrompt'])

            try:
                generate_anki_note(note, generateImage=True, generateAudio=True)
            except Exception as e:
                print(f"ERROR: Could not generate the note for row {row} \n{e}")

def generate_anki_note(note: VocabNote, generateImage: bool, generateAudio: bool) -> bool:
    """ Takes a VocabNote, generates the missing data, and adds it to your Anki deck """
    if anki.can_add_note(DECK_NAME, note):
        image_url = img_gen.fetch_and_select_image(note)
        if not image_url:
            print(f"WARNING: Failed to fetch or select the image for {note}")
        else:
            note.fields.ImageUrl = image_url

        add_note_response = anki.add_note(DECK_NAME, note.model_name, note.get_fields())
        print(f"Note added: {add_note_response['result']}")
        return True
    else:
        print(f"\nERROR: Can't add note for {note})")
        return False

def validate_collection():
    """This ensures the user has the required deck and model in their Anki collection"""
    testFields = {key:str(uuid.uuid4()) for key in VocabNote.get_field_names()}
    testNote = VocabNote(MODEL_NAME, TARGET_LANG, KNOWN_LANG, testFields)
    testResult = anki.can_add_note(DECK_NAME, MODEL_NAME, testNote.get_fields())

    isCollectionValid = all([result['canAdd'] == True for result in testResult['result']])

    if not isCollectionValid:
        print("WARNING: Collection had missing objects")
        setup_collection(testNote)
    else:
        print("Collection is valid")

def setup_collection(sampleNote: VocabNote):
    """This creates the required objects in Anki for AutoVocab"""
    print('Setting up the collection...')

    if not anki.does_deck_exist(DECK_NAME):
        print('Creating missing deck...')
        anki.create_deck(DECK_NAME)

    if not anki.does_model_exist(sampleNote.model_name):
        print('Creating missing model...')
        anki.create_model(sampleNote.model_name, VocabNote.get_field_names(), load_html_templates())

    testResult = anki.can_add_note(DECK_NAME, MODEL_NAME, sampleNote.get_fields())

    isCollectionValid = all([result['canAdd'] == True for result in testResult['result']])

    if not isCollectionValid:
        print("ERROR: Failed to properly setup the collection")

    
def load_html_templates() -> dict:
    with open('front_template.html', 'r', encoding='utf-8') as file:
        front_template = file.read()
    with open('back_template.html', 'r', encoding='utf-8') as file:
        back_template = file.read()
    
    cardTemplate = [
        {
            "Name": CARD_NAME,
            "Front": front_template,
            "Back": back_template
        }
    ]
    return cardTemplate
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "~ Welcome to Autovocab ~")
    parser.add_argument("filename", help="CSV file with a list of words")
    args = parser.parse_args()


    # validate_collection()

    # create_anki_notes(CSV_FILE)