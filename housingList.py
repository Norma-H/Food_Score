#!/usr/bin/env python3

import pandas as pd
from collections import Counter

filename = 'NYCHA_Residential_Addresses.csv'

df = pd.read_csv(filename)

addresses = [f"{row['ADDRESS']} {row['ZIP CODE']}" for ind, row in df.iterrows()]
developments = Counter([row['DEVELOPMENT'] for ind, row in df.iterrows()])
dev_zip = [f"{row['DEVELOPMENT']} {row['ZIP CODE']}" for ind, row in df.iterrows()]
unique_dev_zip = sorted(set(dev_zip))
tds = {f"{row['TDS #']}" for ind, row in df.iterrows()}
# TDS (Tenant Data System) #:
# The number used by numerous computer applications to identify NYCHA Developments.
# https://www1.nyc.gov/assets/nycha/downloads/pdf/pdb2020.pdf


# create a dictionary. each key is a TDS (not consolidated) with a list value of all the addresses.
address_by_tds = {one: [] for one in tds}
for one_tds in address_by_tds:
    nested_add = df.loc[df['TDS #'] == int(one_tds)][['ADDRESS', 'ZIP CODE']].values.tolist()
    address_by_tds[one_tds] = [f'{x[0]} {repr(x[1])}' for x in nested_add]

# create a list of just the first addresses of each value list --> will be used in the food score program
one_tds_address = [val[0] for val in address_by_tds.values()]


def main():
    # print(f'addresses with zipcodes = {len(addresses)}')
    # print(f'developments = {len(set(developments))}')
    # print(f'developments with zipcodes unique = {len(unique_dev_zip)}')
    print(f'number of tds #s: {len(tds)}')
    # [print(val) for val in unique_dev_zip]


if __name__ == '__main__':
    main()
