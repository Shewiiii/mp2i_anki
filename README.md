# MP2I Anki

A simple script to create Anki flashcards from a PDF or text file of a lesson.  
This repo has been created to help me reviewing my lessons. ( ^^) \_旦~~

# Limitations

- Works best with PDFs: All generative AI models I've tried struggle to extract text from all the pages with a long document. PDFs on the other hand are fragmented before extraction.
- The model can hallucinate, you may want to create a deck multiple times until you get satisfying results.
- Only supports plain text for now: really weird things happen when I ask to generate Mathjax or LaTex code.

## Draft setup guide:

### Requirements

- Python 3.xx.
- A valid [OpenAi API key](https://platform.openai.com/api-keys).

### Installation

- Download the project, extract the zip content in a folder.
- cd in the folder.
- Create the virtual env.

```bash
python -m venv venv
```

(Try python3 instead of python if python is not found)

- Activate the venv
  Windows:

```bash
./venv/Scripts/activate.bat
```

Linux:

```bash
source venv/bin/activate
```

- Install the depedencies.

```bash
pip install -r requirements.txt
```

- Create a .env file from the template, pass your OpenAi API Key.
- Change the file_path variable in main.py
- Run main.py

```bash
python main.py
```
