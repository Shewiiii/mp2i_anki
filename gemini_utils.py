import os
import google.generativeai as genai
import json
from typing import TypedDict
from dotenv import load_dotenv
from pathlib import Path
import logging
from config import GEMINI_MODEL, LANGUAGE, REQUEST_LIMIT


load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
global_model = genai.GenerativeModel(
    model_name=GEMINI_MODEL
)
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")


# Gemini structured output
class GeminiDataSchema(TypedDict):
    front: str
    back: str


class GeminiData(TypedDict):
    data: list[GeminiDataSchema]


extract_data_string = '''
- write in {LANGUAGE}
- Extract all formulas or properties to remember from the text of ALL pages.
- Use *MathJax equation code in TeX format* if it's a mathematical formula.
  Always wrap these expressions in \\[...\\].
- Provide the output as a json:
{{"data":
    [
        {{
            "front": A short phrase with name of the property/formula 
            you create,
            "back": The exact formula itself/description from the file
        }},
        etc
    ]
}}
- Output the same language as the input
- The back must be guessable from the front if possible
- The property must ALWAYS be complete.
'''.format(LANGUAGE=LANGUAGE)


class Hibiki:
    def __init__(self) -> None:
        self.prompts = {
            'extract_data': extract_data_string
        }
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=self.prompts['extract_data'],
        )

    @staticmethod
    def remove_duplicates(data: list) -> list:
        seen_fronts = set()
        unique_data = []

        for item in data:
            front = item.get('front')
            if front and front not in seen_fronts:
                unique_data.append(item)
                seen_fronts.add(front)

        return unique_data

    def normalize_data(self, dicts: list[dict]) -> list:
        """List all entries and remove duplicates"""
        entry_list = []
        for json_string in dicts:
            try:
                parsed_dict = json.loads(json_string)
                entry_list.extend(parsed_dict.get('data', []))
            except json.JSONDecodeError:
                logging.error(f"Invalid JSON string skipped: {json_string}")
        entry_list = self.remove_duplicates(entry_list)
        return entry_list

    def upload_file(self, file_path: Path) -> genai.types.File:
        file = genai.upload_file(file_path)
        return file

    def chat_prompt(
        self,
        chat: genai.ChatSession,
        prompt: str = "",
        files: list[genai.types.File] = [],
        response_schema=GeminiData,
        json: bool = True
    ) -> genai.types.GenerateContentResponse:
        prompt_contents = [prompt] + files
        message = chat.send_message(
            prompt_contents,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                temperature=0.3,
                response_schema=response_schema,
                response_mime_type="application/json" if json else None
            ),
            stream=True
        )
        for chunk in message:
            print(chunk.text, end='')
        print()
        return message

    def extract_data(self, file_path: Path) -> list[dict]:
        file = self.upload_file(file_path)
        chat = self.model.start_chat()
        parts = []
        result = self.chat_prompt(chat=chat, files=[file])
        parts.append(json.loads(result.text))
        for _ in range(REQUEST_LIMIT-1):
            result = self.chat_prompt(
                chat=chat,
                files=[file],
                prompt=(
                    "Continue extracting while verifying "
                    "that no properties are missing."
                    "Return an empty dict when finished."
                )
            )

            parts.append(result.text)
            js: dict = json.loads(result.text)
            if not js.get('data'):
                break

        entry_list = self.normalize_data(parts)
        return entry_list
