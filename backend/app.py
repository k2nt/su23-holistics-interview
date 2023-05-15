from flask import Flask
from dotenv import load_dotenv, dotenv_values

import backend_logging
import backend_logging as be_logging


def configure():
    # Load environment variables
    load_dotenv()
    # Configure logging module
    backend_logging.configure(sv_name="backend", is_debug=False)


def start():
    be_logging.info("backend")
    while True:
        pass


if __name__ == "__main__":
    configure()
    start()
