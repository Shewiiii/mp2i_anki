import genanki
from random import randint
from pathlib import Path
import logging

from config import OUTPUT_DIR
from theme import fields, qfmt, afmt, css


class AnkiDeck:
    def __init__(self, output_dir: Path = Path(OUTPUT_DIR)) -> None:
        self.model_id = randint(1000000000, 9999999999)
        self.model = genanki.Model(
            model_id=self.model_id,
            name="Simple Model with LaTeX",
            fields=fields,
            templates=[
                {
                    "name": "Card 1",
                    "qfmt": qfmt,
                    "afmt": afmt,
                },
            ],
            css=css,
        )
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create(self, entry_list: list[dict], deck_name: str = "Generated Deck") -> Path:
        deck_id = randint(1000000000, 9999999999)
        deck = genanki.Deck(deck_id, deck_name)
        if not entry_list:
            logging.error("No formula has been found")
            return

        tags = input("Add a tag: ")
        reference = input("Add a reference: ")
        for entry_dict in entry_list:
            logging.info(
                f"Adding note - Front: {entry_dict['front']}, Back: {entry_dict['back']}"
            )

            front = entry_dict["front"]
            back = entry_dict["back"]

            # Create the note
            note = genanki.Note(model=self.model, fields=[front, back, tags, reference])
            deck.add_note(note)

        output_file = f"{deck_id}.apkg"
        output_path = self.output_dir / output_file
        genanki.Package(deck).write_to_file(output_path)
        logging.info(f"Deck saved to {output_path}")
        return output_path
