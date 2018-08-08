from flask import Flask
import logging
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


""" Setting up logging """
LOGGER = logging.getLogger('app')
LOGGER.setLevel(logging.DEBUG)


FORMATTER = logging.Formatter('[%(levelname)s] %(asctime)s: %(message)s',
                              datefmt='%I:%M:%S %p')

# Stream Handler for logging
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(logging.INFO)
STREAM_HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(STREAM_HANDLER)


# Initialize Flask server
website = Flask(__name__, static_url_path="/static")


def ENABLE_LOGGING_DEBUG():
    global STREAM_HANDLER
    STREAM_HANDLER.setLevel(logging.DEBUG)


from app import views
