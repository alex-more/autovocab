import sys
import csv
import uuid
from anki_interface import add_note, can_add_note, create_model, create_deck, does_deck_exist, does_model_exist
from image_generator import fetch_and_select_image
from models import VocabNote

# TODO: Figure out an efficient flow for batch note creation VS single note creation

# TODO: Get more inspiration for this project by browsing reddit language learning, r/Anki, reddit korean

# TODO: Break down the logic better. I should have a function that generates ONE Anki note.
    # However, if I'm trying to create multiple notes in a batch, it would be inefficient to query ChatGPT for each individual one
    # So the function generate_anki_note()'s params should already contain all the data ChatGPT can come up with by itself

# TODO: Test Fast Word Query addon

# TODO: Test AnkiBrain

# TODO: Make my script prompt ChatGPT directly, in a way that avoids generating words already in the deck

# Before going into any of the following TODOs, I should use my script on a daily basis, and experiment with existing
# Anki addons that do similar things. Also experiment with existing browser extensions.

# TODO: Somehow improve image selection, it still feels very crude. Investigate other APIs, possibly even AI image generation.
    # NOTE: Just like how AwesomeTTS lets users pick which AI tts service to use, 
        # I could let users pick which image generation model to use

# TODO: Investigate making this an actual Anki addon or browser extension


TARGET_LANG = "korean"
KNOWN_LANG = "english"

DECK_NAME = "Korean AutoVocab"
MODEL_NAME = "AutoVocab"
CARD_NAME = "AutoVocab"

CSV_FILE = "new_words.csv"


def add_anki_notes(filename: str):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            if any(field not in row for field in VocabNote.REQUIRED_FIELDS):
                print(f"WARNING: Skipping invalid row (missing required fields): {row}")
                continue
            
            # FIXME: Refactor the whole main.py, I now provide a fields dict to VocabNote and it throws an error if one is invalid

            noteFields = VocabNoteFields(row['TargetWord'], row['KnownWord'], row['Sentence1'], row['Sentence2'], row['Sentence3'])
            note = VocabNote(MODEL_NAME, TARGET_LANG, KNOWN_LANG, noteFields, row['SearchPrompt'])

            can_add_response = can_add_note(DECK_NAME, note.model_name, note.get_fields())
            if all([result['canAdd'] == True for result in can_add_response['result']]):
                image_url = fetch_and_select_image(note)
                if not image_url:
                    print(f"WARNING: Failed to fetch or select the image for {note}")
                else:
                    note.fields.image_url = image_url

                add_note_response = add_note(DECK_NAME, note.model_name, note.get_fields())
                print(f"Note added: {add_note_response['result']}")
            else:
                print(f"\nERROR: Can't add note for {note})")
                print(f"AnkiConnect response: {can_add_response['result'][0]['error']}\n")

# NOTE: Instead of taking a note, this function could hypothetically take a single word.
# That would be great for making a single Anki note at a time, but inefficient for bulk note creation
# Because I could have ChatGPT add every text field in bulk at the start for the whole list of words
# I could force ChatGPT for batch note creation, and allow other methods for getting translations and gloss for individual words
def generate_anki_note(note: VocabNote, generateImage: bool, generateAudio: bool) -> bool:
    """ Takes a VocabNote, generates the missing data, and adds it to your Anki deck """
    pass

def validate_collection():
    """This ensures the user has the required deck and model in their Anki collection"""
    random_strings = [str(uuid.uuid4()) for _ in range(6)]
    testFields = VocabNoteFields(random_strings[0], random_strings[1], random_strings[2], random_strings[3], random_strings[4], random_strings[5])
    testNote = VocabNote(MODEL_NAME, TARGET_LANG, KNOWN_LANG, testFields)
    testResult = can_add_note(DECK_NAME, MODEL_NAME, testNote.get_fields())

    isCollectionValid = all([result['canAdd'] == True for result in testResult['result']])

    if not isCollectionValid:
        print('WARNING: Collection had missing objects')
        setup_collection(testNote)
    else:
        print("Collection is valid")

def setup_collection(sampleNote: VocabNote):
    """This creates the required objects in Anki for AutoVocab"""
    print('Setting up the collection...')

    if not does_deck_exist(DECK_NAME):
        print('Creating missing deck...')
        create_deck(DECK_NAME)

    if not does_model_exist(sampleNote.model_name):
        print('Creating missing model...')
        create_model(sampleNote.model_name, VocabNote.get_field_names(), load_html_templates())

    testResult = can_add_note(DECK_NAME, MODEL_NAME, sampleNote.get_fields())

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
    validate_collection()

    add_anki_notes(CSV_FILE)