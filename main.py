from gemini_utils import Hibiki
from anki_utils import AnkiDeck
from pathlib import Path
import logging
import asyncio

# GEMINI FLASH THINKING DOES NOT SUPPORT JSON OUTPUT YET
# THE FOLLOWING WILL NOT WORK


# Your document path here:
file_path = "cours/Chapitre 25 _ Polynômes.pdf"

anki_deck = AnkiDeck()
hbk = Hibiki()
path = Path(file_path)
file_name = path.stem


def app():
    # Extract data from the PDF
    try:
        logging.info(
            f"Extracting data from {file_name}. This can take a while.")
        entry_list = hbk.extract_data(path)
    except Exception as e:
        logging.error(f"Error extracting data: {e}")
        return
    logging.info(f"Data extraction successful")

    # Create an Anki deck from the extracted data
    try:
        deck_path = anki_deck.create(
            entry_list,
            deck_name=file_name
        )
    except Exception as e:
        logging.error(f"Error creating Anki deck: {e}")
        return


if __name__ == "__main__":
    app()
