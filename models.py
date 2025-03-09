class VocabNote:
    class VocabNoteFields:
        """ Defines fields used for Anki vocab notes """
        def __init__(self, TargetWord='', KnownWord='', Sentence1='', Sentence2='', Sentence3='', ImageUrl='', TargetAudio=''):
            self.TargetWord = TargetWord
            self.KnownWord = KnownWord
            self.Sentence1 = Sentence1
            self.Sentence2 = Sentence2
            self.Sentence3 = Sentence3
            self.ImageUrl = ImageUrl
            self.TargetAudio = TargetAudio

    def __init__(self, model_name: str, target_language: str, known_language: str, fields: dict, search_prompt: str=''):
        self.model_name = model_name
        self.target_language = target_language
        self.known_language = known_language
        self.tags = [target_language]
        self.fields = self.VocabNoteFields()
        self.set_fields(fields)
        self.search_prompt = search_prompt or self.fields.KnownWord

    def __str__(self):  # FIXME: change this to a separate method and keep default print
        return f"{self.fields.TargetWord} ({self.fields.KnownWord})"
    
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
        "TargetWord": "우유",
        "KnownWord": "milk",
        "ImageUrl": "",
        "Sentence1": "우유가 좋아요~",
        "Sentence2": "",
        "Sentence3": "",
        "TargetAudio": ""
    }

    myNote = VocabNote(model_name, target_language, known_language, fields)

    print(myNote)

    myNote.set_fields({'Image'})