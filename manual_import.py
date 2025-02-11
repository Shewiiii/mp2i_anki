from gemini_utils import Hibiki
from anki_utils import AnkiDeck
from pathlib import Path
from config import MANUAL_REQUEST_LIMIT

# Your document path here:
file_path = "cours/Chapitre 25 _ Polynômes.pdf"

anki_deck = AnkiDeck()
hbk = Hibiki()
path = Path(file_path)
file_name = path.stem

if input('Generate new entries ? y/n: ').lower() == 'y':
    hbk = Hibiki()
    file = hbk.upload_file(file_path)
    chat = hbk.model.start_chat()
    result = hbk.chat_prompt(chat=chat, files=[file], json=False)
    for _ in range(MANUAL_REQUEST_LIMIT-1):
        result = hbk.chat_prompt(
            chat=chat,
            files=[file],
            prompt=(
                "Continue extracting while verifying "
                "that no properties are missing."
                "Return an empty dict when finished."
            ),
            json=False
        )

# Replace with the dicts given by gemini !
output_dict = {
    "data":
    [
        {"front": "front of card 1", "back": "back of card 1"},
        # ...
    ]
}
entry_list = hbk.remove_duplicates(output_dict.get("data"))
anki_deck.create(entry_list, file_name)
