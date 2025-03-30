import asyncio
from dotenv import load_dotenv
import json
import logging
import os
from openai import OpenAI
from openai.types.responses import Response
from openai.types.file_object import FileObject
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from typing import List

from config import OPENAI_MODEL, LANGUAGE, ARTIFACTS_DIR


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# Define the extraction prompt
extract_data_string = f"""
- Write in {LANGUAGE}.
- Extract all formulas or properties to remember from the text of all the pages.
- Never use Mathjax or LaTeX, always write in plain text
- Provide the output as a JSON:
{{
    "data": [
        {{
            "front": "A short phrase with the name of the property/formula you create",
            "back": "The exact formula itself/description from the file"
        }},
        ...
    ]
}}
- DON'T change the text whatsoever.
- The back must be guessable from the front if possible.
- The property must ALWAYS be complete.
- Don't forget the back.
- Make short sentences.
"""
text_schema = {
    "format": {
        "type": "json_schema",
        "name": "flashcards",
        "schema": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "description": "A list of flashcard objects.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "front": {
                                "type": "string",
                                "description": "The question or prompt on the front of the flashcard.",
                            },
                            "back": {
                                "type": "string",
                                "description": "The answer or information on the back of the flashcard.",
                            },
                        },
                        "required": ["front", "back"],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["data"],
            "additionalProperties": False,
        },
        "strict": False,
    }
}


class Hibiki:
    def __init__(self) -> None:
        self.prompts = {"extract_data": extract_data_string}
        self.model = OPENAI_MODEL
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

        self.system_message = {
            "role": "system",
            "content": self.prompts["extract_data"],
        }
        self.seen_fronts = set()

    def remove_duplicates(self, data: List[dict]) -> List[dict]:
        unique_data = []

        for item in data:
            front = item.get("front")
            if front and front not in self.seen_fronts:
                unique_data.append(item)
                self.seen_fronts.add(front)

        return unique_data

    def normalize_data(self, parts: List[dict]) -> List[dict]:
        """List all entries and remove duplicates."""
        entry_list = []
        for part in parts:
            entry_list.extend(part.get("data", []))
        entry_list = self.remove_duplicates(entry_list)
        return entry_list

    async def read_file(self, file_path: Path) -> List[FileObject]:
        """Read the content of a file and return a list of FileObjects"""
        logging.info(f"File extension: {file_path.suffix}")
        # PDF
        files = []
        if isinstance(file_path, Path) and file_path.suffix == ".pdf":
            paths = self.fragment_pdf(file_path)
            tasks = [
                asyncio.to_thread(
                    self.client.files.create, file=open(path, "rb"), purpose="user_data"
                )
                for path in paths
            ]
            files = await asyncio.gather(*tasks)
        else:
            logging.warning("Many flashcards may be missing with long documents")
            file: FileObject = await asyncio.to_thread(
                self.client.files.create,
                file=open(file_path, "rb"),
                purpose="user_data",
            )
            files.append(file)

        return files

    def fragment_pdf(self, file_path: Path) -> list:
        """Fragment a pdf into multiple files."""
        paths = []
        if not isinstance(file_path, Path) or not file_path.suffix == ".pdf":
            ValueError("Not a PDF.")

        reader = PdfReader(file_path)
        while True:
            try:
                start = int(
                    input("PDF detected: please enter the first page to consider: ")
                )
                end = int(input("Please enter the last page to consider: "))
                if start <= 0:
                    raise ValueError
                if end > len(reader.pages):
                    end = len(reader.pages)
                break
            except ValueError:
                print("Enter a valid value.")

        for i in range(start - 1, end, 3):
            writer = PdfWriter()
            fragment = reader.pages[i : min(i + 3, end)]
            for page in fragment:
                writer.add_page(page)

            output_path = Path(f"{ARTIFACTS_DIR}/{i}.pdf")
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            paths.append(output_path)

        logging.info(f"Fragmented {file_path} into {len(paths)} pages")

        return paths

    async def prompt(self, prompt: FileObject) -> dict:
        """Send a prompt to OpenAI's API and return the response dict."""
        input_ = [
            self.system_message,
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "file_id": prompt.id,
                    }
                ],
            },
        ]
        response: Response = await asyncio.to_thread(
            self.client.responses.create,
            model=self.model,
            input=input_,
            text=text_schema,
        )
        js: dict = json.loads(response.output_text)
        for card in js.get("data", []):
            logging.info(f"response, front: {card.get('front')}")
        return js

    async def extract_data(self, file_path: Path) -> List[dict]:
        files = await self.read_file(file_path)
        tasks = [self.prompt(file) for file in files]
        parts = await asyncio.gather(*tasks)
        entry_list = self.normalize_data(parts)
        return entry_list
