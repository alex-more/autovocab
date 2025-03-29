class VocabNote:
    class VocabNoteFields:
        """ Defines fields used for Anki vocab notes """
        def __init__(self, Vocab='', Translation='', Gloss='', Sentence='', ImageUrl='', VocabAudio1='', VocabAudio2=''):
            self.Vocab = Vocab
            self.Translation = Translation
            self.Gloss = Gloss
            self.Sentence = Sentence
            self.ImageUrl = ImageUrl
            self.VocabAudio1 = VocabAudio1
            self.VocabAudio2 = VocabAudio2
            self.QueryPrompt = 'TODO: I could have a QueryPrompt field on the note fields, never display it but use it to search/generate images?'

    def __init__(self, model_name: str, target_language: str, known_language: str, fields: dict, search_prompt: str=''):
        self.model_name = model_name
        self.target_language = target_language
        self.known_language = known_language
        self.tags = [target_language]
        self.fields = self.VocabNoteFields()
        self.set_fields(fields)
        self.search_prompt = search_prompt or self.fields.Translation
        # TODO: instead of having fields on VocabNote with ephemeral data, I would make actual fields for these
        # which means I could permanently store the data for use later, if a user wants to update their existing cards

    def __str__(self):  # FIXME: change this to a separate method and keep default print
        return f"{self.fields.Vocab} ({self.fields.Translation})"
    
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

    print(myNote)

    myNote.set_fields({'Image'})