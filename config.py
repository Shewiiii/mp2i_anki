import logging

GEMINI_MODEL = 'gemini-1.5-pro'
GEMINI_UTILS_MODEL = 'gemini-1.5-flash'
LANGUAGE = 'French'
# Logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)
