import requests
import json
from models import VocabNote

ANKICONNECT_URL = "http://localhost:8765"


def add_note(deck_name: str, note: VocabNote) -> dict:
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": note.model_name,
                "fields": note.fields,
                "tags": []
            }
        }
    }

    # FIXME: should return the ID if it succeeds, or False if it fails

    response = requests.post(ANKICONNECT_URL, json=payload)
    return response.json()

def can_add_note(deck_name: str, note: VocabNote) -> bool:
    payload = {
        "action": "canAddNotesWithErrorDetail",
        "version": 6,
        "params": {
            "notes": [
                {
                    "deckName": deck_name,
                    "modelName": note.model_name,
                    "fields": note.fields,
                    "tags": ['Korean']
                }
            ]
        }
    }
    response = requests.post(ANKICONNECT_URL, json=payload)
    return all([result['canAdd'] == True for result in response.json()['result']])



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