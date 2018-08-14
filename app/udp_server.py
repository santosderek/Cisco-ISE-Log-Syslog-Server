import logging
import socketserver

# Might want to change this to a better multithreading library
import json
from .log_parser import parse_data
from app import LOGGER
""" Start Logging """

# Creating the UDP Logging object
UDP_LOGGER = logging.getLogger('udp_server')
UDP_LOGGER.setLevel(logging.INFO)

# TODO: Change this line to be /usr/var/cisco_logs/ciscosys.log or something
LOG_FILE = 'app/static/logs/ciscosys.log'

# Formatters for UDP Logging
UDP_FILE_FORMATTER = logging.Formatter('%(message)s', datefmt='')
UDP_STDOUT_FORMATTER = logging.Formatter('[UDP_Server] %(asctime)s: %(message)s',
                                         datefmt='%I:%M:%S %p')

# File handlder for UDP Logging
FILEHANDLER = logging.FileHandler(LOG_FILE, mode='a')
FILEHANDLER.setFormatter(UDP_FILE_FORMATTER)

# Stream Handler for UDP logging
UDP_STREAM_HANDLER = logging.StreamHandler()
UDP_STREAM_HANDLER.setLevel(logging.INFO)
UDP_STREAM_HANDLER.setFormatter(UDP_STDOUT_FORMATTER)

UDP_LOGGER.addHandler(FILEHANDLER)
UDP_LOGGER.addHandler(UDP_STREAM_HANDLER)


class SyslogUDPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # Bytes.decode => Decode a give list of bytes
        # str()        => converts anything inside into a string
        # self.request[0] => Information recieved
        # .strip() => Gets rid of \x0\x5
        data = str(bytes.decode(self.request[0].strip()))
        #LOGGER.info('LOG NATURAL: ' + data)

        # TODO: UNCOMMENT THIS
        result = parse_data(data)

        # File Logger
        #UDP_LOGGER.info(data + '\n')
        UDP_LOGGER.info(json.dumps(result, indent=4) + ',')


def initialize_udp_server(polling_interval=0.5, host_ip='0.0.0.0', port=8514):
    try:
        # Create the UDP server
        LOGGER.info('UDP server Created.')
        udp_server = socketserver.UDPServer((host_ip, port), SyslogUDPHandler)

        # Poll for events
        LOGGER.info('UDP server polling for events.')
        udp_server.serve_forever(poll_interval=polling_interval)
        LOGGER.info('UDP server natrual exit.')

    except (IOError, SystemExit, OSError) as e:
        LOGGER.info(
            'IOError, SystemExit, OSError Error: Shutting down UDP Server.')
        LOGGER.info(e)

    except KeyboardInterrupt:
        LOGGER.info('Shutting down UDP Server.')
