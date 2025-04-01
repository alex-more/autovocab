# TODOs

## 🔧 Bugs / Fixes
- [ ] Bring text to speech code from desktop

## ✨ Features
- [x] Add LLM logic in-code with Google Gemini
- [ ] Enable code to generate card for one word, with necessary command args
- [ ] Add AI image generation
- [ ] Improve llm_assistant by reviewing this doc: https://ai.google.dev/gemini-api/docs/text-generation
- [ ] Add logic to adapt model to any vocab card using LLM

## 🧹 Refactoring / Cleanup
- [ ] Investigate using pydantic in VocabNote
- [ ] Decide on the vocab fields I want to be able to make once and for all and refactor VocabNoteFields so each field has its own description
- [ ] Refactor anki_interface to always pass VocabNote
- [ ] Refactor anki_interface so it's a class and contains the model/deck names
- [ ] Add target_language in anki_interface tags
- [ ] Improve anki_interface by reviewing: https://git.sr.ht/~foosoft/anki-connect#deck-actions

## 💭 Ideas / Non-code
- [ ] Test AnkiBrain
- [ ] Try KimchiReader extension
- [ ] Try Fast Word Query addon
