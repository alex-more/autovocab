import sys
import csv
import uuid
import anki_interface as anki
import ai_interface as ai
from image_generator import fetch_and_select_image
from anki_models import VocabNote

# TODO: 2 step approach, first step is asking AI to generate a lemma/vocab list (either from a theme, or parsing text)
    # > generate_vocab(prompt) or extract_vocab(text)
    # 2nd step is to "enrich/hydrate" the list with Translation, Gloss, ExampleSentence, QueryPrompt (if image generation is activated)
    # this could optionally be done through AI, or through dictionary API calls
    # dictionary API calls require a language to be "officially supported"

# TODO: Figure out an efficient flow for batch note creation VS single note creation
    # > Answer: It's simple, I should just keep a list of VocabNotes in memory and batch create them once every step has been run
    # > Or alternatively, never batch create and only add one at a time, since the bottleneck will be TTS and image gen anyway

# TODO: Test Fast Word Query addon

# TODO: Test AnkiBrain

# TODO: Test Kimchi Reader

# TODO: Make my script prompt ChatGPT directly, in a way that avoids generating words already in the deck

# Before going into any of the following TODOs, I should use my script on a daily basis, and experiment with existing
# Anki addons that do similar things. Also experiment with existing browser extensions.

# TODO: Somehow improve image selection, it still feels very crude. Investigate other APIs, possibly even AI image generation.
    # NOTE: Just like how AwesomeTTS lets users pick which AI tts service to use, 
        # I could let users pick which image generation model to use

# TODO: Investigate making this an actual Anki addon or browser extension

TARGET_LANG = "Korean"
KNOWN_LANG = "English"

DECK_NAME = f"{TARGET_LANG} AutoVocab"
MODEL_NAME = f"{TARGET_LANG}-AutoVocab"  # FIXME: Model name should be dynamic, based on target language + AutoVocab
CARD_NAME = f"{TARGET_LANG}-AutoVocab"

CSV_FILE = "./data/new_words.csv"  # FIXME: Apparently, | delimiter is better for this purpose


def add_anki_notes(filename: str):
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            if any(field not in row for field in VocabNote.REQUIRED_FIELDS):
                print(f"WARNING: Skipping invalid row (missing required fields): {row}")
                continue
            
            # FIXME: Refactor the whole main.py, I now provide a fields dict to VocabNote and it throws an error if one is invalid

            note = VocabNote(MODEL_NAME, TARGET_LANG, KNOWN_LANG, noteFields, row['SearchPrompt'])

            can_add_response = anki.can_add_note(DECK_NAME, note.model_name, note.get_fields())
            if all([result['canAdd'] == True for result in can_add_response['result']]):
                image_url = fetch_and_select_image(note)
                if not image_url:
                    print(f"WARNING: Failed to fetch or select the image for {note}")
                else:
                    note.fields.image_url = image_url

                add_note_response = anki.add_note(DECK_NAME, note.model_name, note.get_fields())
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
    testResult = anki.can_add_note(DECK_NAME, MODEL_NAME, testNote.get_fields())

    isCollectionValid = all([result['canAdd'] == True for result in testResult['result']])

    if not isCollectionValid:
        print('WARNING: Collection had missing objects')
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
    validate_collection()

    add_anki_notes(CSV_FILE)