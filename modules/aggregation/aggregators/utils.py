from typing import Text
import re

def clean_answer_value(value: Text) -> Text:
    value = re.sub("[\-!@#$%^&*\(\)]", " ", value)
    value = value.replace('\n', ' ')
    value = re.sub("[ ]* ", " ", value)
    value = capitalize_first(value)
    return value.strip()


def normalize_answer_value(value: Text) -> Text:
    return re.sub('[^a-zA-ZąćęłóńżźĄĆĘŁÓŃŻŹ0-9]', '', value.lower())


def capitalize_first(text: Text) -> Text:
    return text[0].upper() + text[1:]

