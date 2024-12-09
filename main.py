
from gemini_utils import Hibiki
from anki_utils import AnkiDeck
from pathlib import Path
import logging


async def app():
    hibiki = Hibiki()
    pdf_path = Path('cours/Chapitre 18 _ Arithmétique dans Z.pdf')
    pdf_name = pdf_path.stem

    # Extract data from the PDF
    try:
        logging.info(
            f"Extracting data from {pdf_name}. This can take a while.")
        formulas_dict = await hibiki.extract_data(pdf_path)
    except Exception as e:
        logging.error(f"Error extracting data: {e}")
        return
    logging.info(f"Data extraction successful")

    # Create an Anki deck from the extracted data
    anki_deck = AnkiDeck()
    try:
        deck_path = anki_deck.create(
            formulas_dict,
            deck_name=pdf_name
        )
    except Exception as e:
        logging.error(f"Error creating Anki deck: {e}")
        return

if __name__ == "__main__":
    # asyncio.run(app())
    await app()
