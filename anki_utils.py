# anki_utils.py

import genanki
from random import randint
from pathlib import Path
from typing import Dict
import logging


class AnkiDeck:
    def __init__(
        self,
        output_dir: Path = Path('./generated')
    ) -> None:
        self.model_id = randint(1000000000, 9999999999)
        self.model = genanki.Model(
            model_id=self.model_id,
            name="Simple Model with LaTeX",
            fields=[
                {"name": "Question"},
                {"name": "Answer"},
            ],
            templates=[
                {
                    "name": "Card 1",
                    "qfmt": "{{Question}}",
                    "afmt": "{{FrontSide}}<hr id='answer'>{{Answer}}",
                },
            ],
            css="""
            .card {
                font-family: Arial;
                font-size: 20px;
                text-align: left;
                color: black;
                background-color: white;
            }
            """
        )
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create(
        self,
        formulas_dict: Dict[str, list],
        deck_name: str = "Generated Deck"
    ) -> Path:
        deck_id = randint(1000000000, 9999999999)
        deck = genanki.Deck(deck_id, deck_name)
        formulas = formulas_dict.get('data')
        if not formulas:
            logging.error('No formula has been found')
            return

        for formula_dict in formulas:
            # Debug: logging.info each formula and answer
            logging.info(
                f"Adding note - Name: {formula_dict['name']}, Value: {formula_dict['value']}")

            name_latex = formula_dict['name']
            value_latex = formula_dict['value']

            # Create the note
            note = genanki.Note(
                model=self.model,
                fields=[name_latex, value_latex]
            )
            deck.add_note(note)

        output_file = f"{deck_id}.apkg"
        output_path = self.output_dir / output_file
        genanki.Package(deck).write_to_file(output_path)
        logging.info(f"Deck saved to {output_path}")
        return output_path
