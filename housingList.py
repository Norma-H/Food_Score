#!/usr/bin/env python3

import pandas as pd

filename = 'NYCHA_Residential_Addresses.csv'

df = pd.read_csv(filename)

addresses = [f"{row['ADDRESS']} {row['ZIP CODE']}" for ind, row in df.iterrows()]
