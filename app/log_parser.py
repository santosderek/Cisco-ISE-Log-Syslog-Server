import re
import json

from . import LOGGER
from .csv_parser import step_codes


def parse_data(log):
    """
        Parse single log

        Both 'Radius-Accounting' and 'CISE_System_Statistics' have simular log
        syles so they can be used in the same regular expression.
    """


    if re.search('(Radius-Accounting: RADIUS Accounting)', log):

        result = {}
        ret_val = {}

        search = log.split(',')

        timestamp = re.findall(
            '[\w{3}|\d{2}]\s\d{2}\s\d{2}:\d{2}:\d{2}', search[0])
        exact_time = re.findall(
            '\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3}', search[0])
        result['Time'] = timestamp[0]
        result['Exact Time'] = exact_time[0]
        # Go through each found item in search and split them using the '='
        for item in search[1:]:
            # Remove any spaces in the beginning of the line
            if item and item[0] == ' ':
                item = item[1:]

            # Split each item by the '=' symbol
            if item.find('=') != -1:
                item = item.split('=')

            elif item.find(':') != -1:
                item = item.split(':')

            # First element in list is key, Second element in list is data
            # TODO: REMOVE ALL BLANK ITEMS

            if item and item[0] in result:
                count = 2
                # Count until key is not found then insert it into that spot
                while item[0] + '_' + str(count) in result:
                    count += 1

                result[item[0] + '_' + str(count)] = item[1]

            elif item:
                if item[0] == 'Step' and item[1] in step_codes:
                    #print steps prior to saving them
                    LOGGER.debug('STEP: ' + item[0] + '_' + item[1])
                    LOGGER.debug(
                        'CODE: ' + step_codes[item[1]][1] + ' - ' + step_codes[item[1]][2])
                    result[item[0] + '_' + item[1]] = step_codes[item[1]
                                                                 ][1] + ' - ' + step_codes[item[1]][2]
                    Final_Step = item[0] + ' ' + item[1] + ' - ' + \
                        step_codes[item[1]][1] + ' - ' + step_codes[item[1]][2]
                    #saving final step to appear first
                    ret_val['Final Step'] = Final_Step

                elif item[0] == 'Step':
                	#check for unknown step values
                    LOGGER.debug('UNKNOWN STEP: ' + item[0] + '_' + item[1])
                    result[item[0] + '_' + item[1]] = 'UNKNOWN'
                    Final_Step = item[0] + ' ' + item[1] + '- UNKNOWN'
                    ret_val['Final Step'] = Final_Step
                else:
                	#saving all other logs
                    LOGGER.debug('NORMAL: ' + item[0] + ' : ' + item[1])
                    result[item[0]] = item[1]

        # Return the dictionary of results
        ret_val.update(result)
        # Return the dictionary of results
        return ret_val


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
