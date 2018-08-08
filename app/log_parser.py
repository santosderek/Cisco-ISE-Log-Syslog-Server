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
#log_template = '<181>Jul 24 13:36:09 dahouck-ise CISE_RADIUS_Accounting 0000008174 1 0 2018-07-24 13:36:09.866 -04:00 0000106784 3002 NOTICE Radius-Accounting: RADIUS Accounting watchdog update, ConfigVersionId=74, Device IP Address=10.118.113.194, RequestLatency=8, NetworkDeviceName=homeswitch, User-Name=isetest, NAS-IP-Address=10.118.113.194, Service-Type=Framed, Acct-Status-Type=Interim-Update, Acct-Delay-Time=0, Acct-Session-Id=00000000, Acct-Authentic=RADIUS, AcsSessionID=dahouck-ise/321208428/4380, SelectedAccessService=Default Network Access, Step=11004, Step=11017, Step=11117, Step=15049, Step=15008, Step=15048, Step=15048, Step=22094, Step=11005, NetworkDeviceGroups=IPSEC#Is IPSEC Device#No, NetworkDeviceGroups=Location#All Locations, NetworkDeviceGroups=Device Type#All Device Types, CPMSessionID=0a7a6d90J8ZQ4Q0Wj8O6yGEBwbw87i0wurpQFN25LsVzqaxV_So, Model Name=3560-CG, Network Device Profile=Cisco, Location=Location#All Locations, Device Type=Device Type#All Device Types, IPSEC=IPSEC#Is IPSEC Device#No,'


    if re.search('(Radius-Accounting: RADIUS Accounting)', log):

        # TODO : depending on 'CISE_System_Statistics' or 'Radius-Accounting' split using ',' or ';'
        result = {}
        ret_val = {}
        # Regular expression to find 'information'='information' lines within commas
        # TIME STAMP REGEX : \w{3}\s\d{2}\s\d{2}:\d{2}:\d{2}

        search = log.split(',')

        timestamp = re.findall('[\w{3}|\d{2}]\s\d{2}\s\d{2}:\d{2}:\d{2}', search[0])
        exact_time = re.findall('\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3}', search[0])
        print(search[0])
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
                    count+=1

                result[item[0] + '_' + str(count)] = item[1]

            elif item:
                if item[0] == 'Step' and item[1] in step_codes:
                    LOGGER.debug('STEP: '+ item[0] + '_' + item[1])
                    LOGGER.debug('CODE: '+ step_codes[item[1]][1] + ' - ' + step_codes[item[1]][2])
                    result[item[0] + '_' + item[1]] = step_codes[item[1]][1] + ' - ' + step_codes[item[1]][2]
                    last_step = item[0] + ' ' + item[1] +' - ' + step_codes[item[1]][1] + ' - ' + step_codes[item[1]][2]
                    ret_val['Last Step'] = last_step
                    #+ ',' + step_codes[item[1]][3]
                elif item[0] == 'Step':
                    LOGGER.debug('UNKNOWN STEP: '+ item[0] + '_' + item[1])
                    result[item[0] + '_' + item[1]] = 'UNKNOWN'
                    last_step = item[0] + ' ' + item[1] + '- UNKNOWN'
                    ret_val['Last Step'] = last_step
                else:
                    LOGGER.debug('NORMAL: '+ item[0] + ' : ' + item[1])
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
