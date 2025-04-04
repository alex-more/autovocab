from pydantic import BaseModel

"""
TODO: Refactor this once and for all
Useful fields: Translation, Gloss, ExampleSentence, QueryPrompt (if image generation is activated)

A VocabNote should not have a defined set of fields, instead it should have a fields dict that
is dynamically created/inferred on app startup.

I should have a Default/Recommended VocabNote type

VocabField should be its own abstract class and the different fields should inherit from it
"""

class VocabField:
    pass  # TODO:

class VocabNote:
    class VocabNoteFields:
        """ Defines fields used for Anki vocab notes """
        def __init__(self, TargetWord='', Sentence1='', Sentence2='', Sentence3='', ImageUrl='', TargetAudio='', Translation='', Gloss=''):
            self.TargetWord = TargetWord
            self.Sentence1 = Sentence1
            self.Sentence2 = Sentence2
            self.Sentence3 = Sentence3
            self.ImageUrl = ImageUrl
            self.TargetAudio = TargetAudio
            self.Translation = Translation
            self.Gloss = Gloss

    def __init__(self, model_name: str, target_language: str, known_language: str, fields: dict, search_prompt: str=''):
        self.model_name = model_name
        self.target_language = target_language
        self.known_language = known_language
        self.tags = [target_language]
        self.fields = self.VocabNoteFields()
        self.set_fields(fields)
        self.search_prompt = search_prompt or self.fields.Translation

    def nice_print(self):
        return f"{self.fields.TargetWord} ({self.fields.Translation})"
    
    def set_fields(self, fields: dict):
        """ Accepts a dictionary and sets the corresponding fields """
        valid_fields = vars(self.fields).keys()
        invalid_keys = [key for key in fields if key not in valid_fields]

        if invalid_keys:
            raise ValueError(f"Invalid fields provided: {', '.join(invalid_keys)}")

        for key, value in fields.items():
            setattr(self.fields, key, value)

    @classmethod
    def get_field_names(cls) -> list:
        """ Return the field names of the VocabNoteFields """
        return list(vars(cls.VocabNoteFields()).keys())
    

if __name__ == "__main__":
    model_name = "TestModel"
    target_language = "korean"
    known_language = "english"

    fields = {
        "Vocab": "우유",
        "Translation": "milk",
        "ImageUrl": "",
        "Sentence": "우유가 좋아요~",
        "VocabAudio1": ""
    }

    myNote = VocabNote(model_name, target_language, known_language, fields)

    print(VocabNote.get_field_names())