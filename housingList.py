#!/usr/bin/env python3

import pandas as pd
from collections import Counter

filename = 'NYCHA_Residential_Addresses.csv'

df = pd.read_csv(filename)

addresses = [f"{row['ADDRESS']} {row['ZIP CODE']}" for ind, row in df.iterrows()]
developments = Counter([row['DEVELOPMENT'] for ind, row in df.iterrows()])
dev_zip = [f"{row['DEVELOPMENT']} {row['ZIP CODE']}" for ind, row in df.iterrows()]
unique_dev_zip = sorted(set(dev_zip))


def main():
    # print(f'addresses with zipcodes = {len(addresses)}')
    # print(f'developments = {len(set(developments))}')
    # print(f'developments with zipcodes unique = {len(unique_dev_zip)}')
    [print(val) for val in unique_dev_zip]

if __name__ == '__main__':
    main()
