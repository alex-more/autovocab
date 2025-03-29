from dotenv import load_dotenv
from gtts import gTTS
from io import BytesIO
import anki_interface as anki
import base64
import uuid
import os

load_dotenv()
ANKI_MEDIA_PATH = os.getenv("ANKI_MEDIA_PATH") or anki.get_media_dir_path()

# NOTE: Arguably, this file should have no concept of Anki and instead just return a tuple like so:
#   -> (audio: bytes, filename: str)

def generate_and_save_audio(text: str, lang: str, audio_method: str ='gtts') -> str:
    if audio_method == 'gtts':
        audio_data = gtts_generate_audio(text, lang)
    else:
        raise ValueError(f"Unsupported audio method: {audio_method}")

    filename = f"{audio_method}-{uuid.uuid4()}.mp3"
    response = anki.store_media_file(filename, audio_data)
    if not response:
        print(f"ERROR: Failed to store audio file in Anki for: {text}")
        return None
    
    return filename
    
def gtts_generate_audio(text: str, lang: str) -> bytes:
    tts = gTTS(text=text, lang=lang)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return base64.b64encode(mp3_fp.getvalue())

def play_anki_audio(filename: str) -> None:
    file_path = os.path.join(ANKI_MEDIA_PATH, filename)
    os.system(f'start "" "{file_path}"')


if __name__ == "__main__":
    test_sentence = "안녕하세요. 이것은 구글 텍스트 투 스피치 테스트입니다."

    filename = generate_and_save_audio(test_sentence, 'ko')

    if filename:
        play_anki_audio(filename)