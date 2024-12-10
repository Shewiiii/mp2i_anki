
from gemini_utils import Hibiki
from anki_utils import AnkiDeck
from pathlib import Path
import logging
import asyncio

# Your document path here:
file_path = "cours/chapM3-energie_mecanique.pdf"

async def app():
    hibiki = Hibiki()
    path = Path(file_path)
    file_name = path.stem

    # Extract data from the PDF
    try:
        logging.info(
            f"Extracting data from {file_name}. This can take a while.")
        formulas_dict = await hibiki.extract_data(path)
    except Exception as e:
        logging.error(f"Error extracting data: {e}")
        return
    logging.info(f"Data extraction successful")

    # Create an Anki deck from the extracted data
    anki_deck = AnkiDeck()
    try:
        deck_path = anki_deck.create(
            formulas_dict,
            deck_name=file_name
        )
    except Exception as e:
        logging.error(f"Error creating Anki deck: {e}")
        return

if __name__ == "__main__":
    asyncio.run(app())
