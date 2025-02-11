import logging

# Please use chain-of-thought based models
GEMINI_MODEL = "gemini-2.0-flash-thinking-exp" # Not available yet, exp version does not support JSON mime type
LANGUAGE = "French"
OUTPUT_DIR = "./generated"
REQUEST_LIMIT = 10 # The max number of Gemini API calls per deck
MANUAL_REQUEST_LIMIT = 3
# Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)
