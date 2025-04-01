import requests
from models import VocabNote

"""
NOTE: The goal of this whole file/class should simply be: Given a word or prompt, find/generate images as effectively as possible
Effectively meaning accurate (good pictures), fast, and ample (more than one image), and ideally free
DeepAI has a simple API I can use for this
"""


WIKIMEDIA_API_URL = "https://commons.wikimedia.org/w/api.php"

ACCEPTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.gif']

MAX_IMAGE_WIDTH = "500px"

IMAGE_SEARCH_LIMIT = 15
IMAGE_SELECTION_LIMIT = 3

INTERACTIVE_IMAGE_SELECTION = True


def fetch_and_select_image(note: VocabNote) -> str:
    images = fetch_images(note.search_prompt)

    if len(images) < IMAGE_SEARCH_LIMIT/2:
        images = fetch_images(note.fields.known_word)

    if len(images) < IMAGE_SEARCH_LIMIT/2:
        images = fetch_images(note.fields.known_word, IMAGE_SEARCH_LIMIT*2)

    if INTERACTIVE_IMAGE_SELECTION:
        return pick_an_image(note, images)
    else:
        return images[0]

def fetch_images(keyword, search_limit=IMAGE_SEARCH_LIMIT):
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'imageinfo',
        'iiprop': 'url',
        'generator': 'search',
        'gsrsearch': keyword,
        'gsrnamespace': 6,
        'gsrlimit': search_limit,
    }

    print(f"!DEBUG: search prompt: {keyword}")

    response = requests.get(WIKIMEDIA_API_URL, params=params)
    data = response.json()

    images = []
    if 'query' in data:
        pages = data['query']['pages']
        # print(f"!DEBUG: pages: {pages}")
        for page_id, page_data in pages.items():
            if 'imageinfo' in page_data:
                image_info = page_data['imageinfo'][0]
                image_url = get_thumbnail_url(image_info['url'])
                if any(image_url.endswith(ext) for ext in ACCEPTED_IMAGE_FORMATS):
                    images.append(image_url)
    return images

def pick_an_image(note: VocabNote, images: list) -> str:
    image_options = images[:IMAGE_SELECTION_LIMIT]
    start_index = 0

    print(f"\nChoose an image that best fits the following word to you: {note}")

    for i, img_url in enumerate(image_options, 1):
        print(f"{i}. {img_url}")

    while True:
        choice = input(f"\nEnter a number (1 to {IMAGE_SELECTION_LIMIT}) or X if you want new image options: ")

        if choice in [str(i) for i in range(1, IMAGE_SELECTION_LIMIT + 1)]:
            selected_image_url = image_options[int(choice) - 1]
            return selected_image_url
        elif choice in ['x', 'X']:
            next_index = start_index + IMAGE_SELECTION_LIMIT
            start_index = next_index if next_index < len(images) else 0
            image_options = images[start_index : start_index+IMAGE_SELECTION_LIMIT]
            for i, img_url in enumerate(image_options, 1):
                print(f"{i}. {img_url}")
        else:
            print(f"Invalid input. Please select a number between 1 and {IMAGE_SELECTION_LIMIT}.")

def get_thumbnail_url(image_url: str) -> str:
    filename = image_url.split('/')[-1]
    thumbnail_url = image_url.replace('/commons/', '/commons/thumb/') + f'/{MAX_IMAGE_WIDTH}-{filename}'
    return thumbnail_url

if __name__ == "__main__":
    prompt = "Metal soup ladle"
    # fields = VocabNoteFields("휴식", "ladle", "", "", "")
    vocabNote = VocabNote('AutoVocab', 'korean', 'english', fields, prompt)
    url = fetch_and_select_image(vocabNote)