import asyncio
from anki_utils import AnkiDeck
from hibiki import Hibiki
from pathlib import Path
import logging

from config import OUTPUT_DIR, ARTIFACTS_DIR


# Your document path here:
file_path = "cours/Chapitre 29 _ Applications linéaires.pdf"

anki_deck = AnkiDeck()
hbk = Hibiki()
path = Path(file_path)
file_name = path.stem


async def app():
    # Create the paths
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    Path(ARTIFACTS_DIR).mkdir(exist_ok=True)

    # Extract data from the PDF
    logging.info(f"Extracting data from {file_name}. This can take a while.")
    entry_list = await hbk.extract_data(path)
    logging.info("Data extraction successful")

    # Create an Anki deck from the extracted data
    anki_deck.create(entry_list, deck_name=file_name)


if __name__ == "__main__":
    asyncio.run(app())
