import logging
import sys

# The model MUST support both image and text input.
OPENAI_MODEL = "o4-mini-2025-04-16"
LANGUAGE = "English"
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
