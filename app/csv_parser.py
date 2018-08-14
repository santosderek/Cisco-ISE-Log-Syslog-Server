import re
import json
import csv
from collections import defaultdict
from . import LOGGER


step_codes = defaultdict(list)

def parse_csv(file_name):
    global step_codes
    with open(file_name, 'r', encoding='utf-8') as current_file:
    # open file, read it
        data = current_file.read()
        # Split the data by endlines
        data = data.split('\n')
        for line in data:
            # for each line split those lines by their ','
            items = line.split(',')
            for desc in items:
                if not items[0] == desc:
                    step_codes[items[0]].append(desc)

    return True;
