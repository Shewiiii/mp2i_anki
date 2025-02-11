Only manual import works for now, since Gemini-flash Thinking does not support JSON response mime type yet.

# MP2I Anki
A simple script to create Anki flashcards from a PDF or text file of a lesson.  
This repo has been created to help me reviewing my lessons. ( ^^) _旦~~

## Draft setup guide:

### Requirements
- Python 3.xx.
- A valid [Gemini API key](https://ai.google.dev/gemini-api/docs/api-key).

### Installation
- Download the project, extract the zip content in a folder.
- cd in the folder.
- Create the virtual env.
```bash
python -m venv venv
```
- Activate the venv
- Install the depedencies.
```bash
pip install -r requirements.txt
```
- Create a .env file from the template, pass your Gemini API Key.
- Change the file_path variable in main.py
- Run main.py
```bash 
python main.py
```