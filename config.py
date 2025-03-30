import logging
import sys

# The model MUST support both image and text input.
OPENAI_MODEL = "gpt-4o-mini-2024-07-18"
LANGUAGE = "French"
OUTPUT_DIR = "./generated"
ARTIFACTS_DIR = "./artifacts"
MANUAL_REQUEST_LIMIT = 3

# Logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
)
