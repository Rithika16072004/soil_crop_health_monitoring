from deep_translator import GoogleTranslator

def translate_text(text, lang):
    if lang == "en":
        return text
    return GoogleTranslator(source="en", target=lang).translate(text)
