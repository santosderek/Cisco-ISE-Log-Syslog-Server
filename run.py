from app.udp_server import initialize_udp_server, LOG_FILE
from app import website, LOGGER, ENABLE_LOGGING_DEBUG
from argparse import ArgumentParser
from app.csv_parser import parse_csv, step_codes
import threading
from os.path import isfile


def parse_args():
    parser = ArgumentParser(description='ISE')
    parser.add_argument('--debug', '-d', action='store_true',
                        help='Enables debugging output.')
    parser.add_argument('--ip', metavar='IP', default='0.0.0.0',
                        help='Specify IP address of host.')
    parser.add_argument('--port', metavar='PORT', default=80,
                        help='Specify port.')

    return parser.parse_args()


if __name__ == '__main__':
    arguments = parse_args()

    if arguments.debug == True:
        ENABLE_LOGGING_DEBUG()

    #read csv step_codes
    parse_csv("app/static/Cisco_Identity_Services_Engine_Log_Messages_20.csv")
    LOGGER.debug(step_codes['3000'])

    # Start UDP Server
    if not isfile(LOG_FILE):
        with open(LOG_FILE, 'a') as current_file:
            current_file.write('')

    udp_thread = threading.Thread(target=initialize_udp_server,
                                  args=(0.5,
                                        '0.0.0.0',
                                        8514),
                                  daemon=True)

    udp_thread.start()

    website.run(host=arguments.ip,
                port=arguments.port,
                debug=arguments.debug)
