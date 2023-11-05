import logging
import os
from directories import LOGS_DIRECTORY  # Import logs directory from configuration module

LOG_FILE_PATH = os.path.join(LOGS_DIRECTORY, "device_discovery.log")

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler()
    ]
)
