import os
import google.generativeai as genai
import json
from typing import TypedDict, List, Dict
from dotenv import load_dotenv
from pathlib import Path
from config import GEMINI_UTILS_MODEL, LANGUAGE
import asyncio
from typing import Optional
import logging


load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
global_model = genai.GenerativeModel(
    model_name=GEMINI_UTILS_MODEL
)
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")


class DataSchema(TypedDict):
    name: str
    value: str


class Data(TypedDict):
    data: list[DataSchema]


extract_data_string = '''
- Extract all formulas or properties to remember from the text of ALL pages.
- Use *MathJax equation code in TeX format* if it's a mathematical formula.
  Always wrap these expressions in \\[...\\].
- Provide the output as a json:
[{{"data":
    [
        {{
            "name": Precise name of the property/formula with a
            short sentence you create in {LANGUAGE},
            "value": The exact formula itself/description from the file
        }},
        ...
    ]
}}
- Output the same language as the input
- Always return a valid json text, remove the last entry if truncated
- The property must ALWAYS be complete.
'''.format(LANGUAGE=LANGUAGE)


class Hibiki:
    def __init__(self) -> None:
        self.prompts = {
            'extract_data': extract_data_string
        }
        self.model = genai.GenerativeModel(
            model_name=GEMINI_UTILS_MODEL,
            system_instruction=self.prompts['extract_data'],
        )

    @staticmethod
    def remove_duplicates(data: list) -> list:
        seen_names = set()
        unique_data = []

        for item in data:
            name = item.get('name')
            if name and name not in seen_names:
                unique_data.append(item)
                seen_names.add(name)

        return unique_data

    def normalize_data(self, dicts: list[dict]) -> dict:
        """Combine data dicts and remove duplicates"""
        combined_dict = {'data': []}
        for json_string in dicts:
            try:
                parsed_dict = json.loads(json_string)
                combined_dict['data'].extend(
                    parsed_dict.get('data', []))
            except json.JSONDecodeError:
                logging.error(f"Invalid JSON string skipped: {json_string}")
        combined_dict['data'] = self.remove_duplicates(combined_dict['data'])
        return combined_dict

    async def upload_file(self, file_path: Path) -> genai.types.File:
        file = await asyncio.to_thread(genai.upload_file, file_path)
        return file

    async def chat_prompt(
        self,
        chat: genai.ChatSession,
        prompt: str = "",
        files: list[genai.types.File] = [],
        response_schema=Data
    ) -> genai.types.AsyncGenerateContentResponse:
        prompt_contents = [prompt] + files
        result = await chat.send_message_async(
            prompt_contents,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                temperature=0.3,
                response_mime_type="application/json",
                response_schema=response_schema
            )
        )
        return result

    async def extract_data(self, file_path: Path) -> dict[str, str]:
        file = await self.upload_file(file_path)
        chat = self.model.start_chat()
        parts = []
        result = await self.chat_prompt(chat=chat, files=[file])
        parts.append(result.text)
        for _ in range(10):
            result = await self.chat_prompt(
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

        combined_dict = self.normalize_data(parts)
        return combined_dict
