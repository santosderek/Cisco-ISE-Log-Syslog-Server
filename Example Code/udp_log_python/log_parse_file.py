import re
import json
from pprint import pprint


def parse_data(log):
    """
        Parse single log

        Both 'Radius-Accounting' and 'CISE_System_Statistics' have simular log
        syles so they can be used in the same regular expression.
    """

    if re.search('(Radius-Accounting|CISE_System_Statistics)', log):
        result = []

        # Regular expression to find 'information'='information' lines within commas
        search = re.findall(
            r'[A-z0-9\-\:\.\s\/#\%]+=[A-z0-9\-\:\.\s\/#\%]+', log)

        # Go through each found item in search and split them using the '='
        for item in search:
            # Remove any spaces in the beginning of the line
            if item[0] == ' ':
                item = item[1:]

            # Split each item by the '=' symbol
            item = item.split('=')

            # First element in list is key, Second element in list is data
            result.append({item[0]: item[1]})

        # Return the list of results
        return result


def parse_multiple_logs(log: str):
    """ Parse logs separated by a newline '\n' """
    complete_list = []

    for item in log.split('\n'):
        result = parse_data(item)
        if result:
            complete_list.append(result)

    return complete_list


def parse_log_file(filename: str):
    """ Open file and parse logs within """
    with open(filename, 'r') as current_file:
        data = current_file.read()

    return parse_multiple_logs(data)


if __name__ == '__main__':
    pprint(parse_log_file('logs.logs'))
