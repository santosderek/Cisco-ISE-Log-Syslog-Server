import json
import re


class Device_Group():
    """ This class creates a list of devices and
        can manipulate the list of devices for
        easier management.
    """

    def __init__(self):
        self.list_of_devices = []


    def add_log(self, log):

        for current_device in self.list_of_devices:
            """ Go through current list"""

            if log['Device IP Address'] == current_device.ip_address:
                """ If ip addresss already in list add it to the already made device """
                current_device.add_log(log)

                """ Return since it was found """
                return


        """ If now found then append the device """
        new_device = Device(ip_address=log['Device IP Address'],
                            position_in_list=str(len(self.list_of_devices))
                            )
        new_device.add_log(log)
        self.list_of_devices.append(new_device)


class Device():
    def __init__(self, mac_address=None, logs=[], ip_address=None, position_in_list=0):
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.logs = logs
        self.position_in_list = position_in_list

    def add_log(self, log):


        for prelog in self.logs:
            if prelog['Exact Time'] == log['Exact Time']:
                return
        log['position_in_list'] = len(self.logs)
        self.logs.append(log)


def return_json(file_path):

    with open(file_path, 'r') as current_file:
        json_result = json.loads(current_file.read())

    return json_result
