import requests
import json
from models import VocabNote

ANKICONNECT_URL = "http://localhost:8765"

# TODO: Make this into a class instead?

# TODO: Also, why wouldn't I pass a VocabNote to fns like add_note and can_add_note?

# TODO: add tag corresponding to note.target_language

# If I used guiAddCards action I could maybe make it more user friendly?

# TODO: Review https://git.sr.ht/~foosoft/anki-connect#deck-actions and improve the anki interfacing logic accordingly

def add_note(deck_name: str, model_name: str, fields: dict) -> dict:
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": model_name,
                "fields": fields,
                "tags": []
            }
        }
    }

    response = requests.post(ANKICONNECT_URL, json=payload)
    return response.json()

def can_add_note(deck_name: str, model_name: str, fields: dict):
    payload = {
        "action": "canAddNotesWithErrorDetail",
        "version": 6,
        "params": {
            "notes": [
                {
                    "deckName": deck_name,
                    "modelName": model_name,
                    "fields": fields,
                    "tags": ['Korean']
                }
            ]
        }
    }
    response = requests.post(ANKICONNECT_URL, json=payload)
    return response.json()

def create_model(model_name: str, fields: list, card_templates: list):
    model = {
        "modelName": model_name,
        "isCloze": False,
        'inOrderFields': fields,
        'cardTemplates': card_templates,
        # 'css': '.card { font-size: 20px; text-align: center; }',
    }
    payload = {
        'action': 'createModel',
        'version': 6,
        'params': model
    }
    response = requests.post(ANKICONNECT_URL, json=payload)
    return response.json()

def create_deck(deck_name):
    payload = {
        "action": "createDeck",
        "version": 6,
        "params": {"deck": deck_name}
    }
    response = requests.post(ANKICONNECT_URL, json=payload)
    return response.json()

def get_all_deck_names():
    payload = {
        "action": "deckNames",
        "version": 6
    }
    response = requests.post(ANKICONNECT_URL, json=payload)
    return response.json()

def get_all_model_names():
    payload = {
        "action": "modelNames",
        "version": 6
    }
    response = requests.post(ANKICONNECT_URL, json=payload)
    return response.json()

def does_deck_exist(deck_name: str) -> bool:
    return deck_name in get_all_deck_names()['result']

def does_model_exist(model_name: str) -> bool:
    return model_name in get_all_model_names()['result']


if __name__ == "__main__":
    print(get_all_deck_names())