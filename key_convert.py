#!/usr/bin/env python3

import pandas as pd
import json

key_file = pd.read_csv('key.csv', header=None)
key_code = key_file[0].values[0]

dict = {'key': key_code}
jsonStr = json.dumps(dict)  # this is a json string now?
jsonFile = open('key.json', 'w')
jsonFile.write(jsonStr)
jsonFile.close()