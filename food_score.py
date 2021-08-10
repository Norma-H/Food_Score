#!/usr/bin/env python3

import googlemaps
from housingList import unique_dev_zip
import pandas as pd


class Store:
    def __init__(self, name, address, rating, coordinates, starting_loc):
        self.name = name
        self.address = address
        self.rating = rating
        self.location = coordinates
        self.distance = self.get_distance(starting_loc)

    def get_distance(self, starting_loc):
        """
        takes in the center location
        retrieves the distance in km and calculates it to miles
        returns the distance (float) in miles
        """
        dist = gmaps.distance_matrix(starting_loc, self.location)
        dist = dist['rows'][0]['elements'][0]['distance']['text'].split(' ')
        dist = float(dist[0])
        self.distance = dist * 0.621371  # converting distance from km to miles
        return self.distance


key_file = pd.read_csv('key.csv', header=None)
key_code = key_file[0].values[0]
gmaps = googlemaps.Client(key=key_code)


def get_store_results(lookup_address):
    # Geocoding an address
    geocode_result = gmaps.geocode(lookup_address)
    # TODO: does not have "bounds" in the results so my hard code below of 'bounds' index does not work
    # print(geocode_result)
    try:
        # getting the coordinates for the address
        coordinates = [float(val) for val in geocode_result[0]['geometry']['bounds']['northeast'].values()]

        # TODO: figure out why the radius is not working
        places_result = gmaps.places(type='grocery_or_supermarket', location=coordinates, radius=1609)  # 1609 is 1 mile
        return places_result
    except KeyError:
        coordinates = [float(val) for val in geocode_result[0]['geometry']['location'].values()]
        # TODO: figure out why the radius is not working
        places_result = gmaps.places(type='grocery_or_supermarket', location=coordinates, radius=1609)  # 1609 is 1 mile
        return places_result


def instantiate_stores(places_result, lookup_address):
    """
    take in the result of the search (all the stores) and the original address
    create list of all the instantiated store classes from the search results
    return the list of the instances
    """
    stores = []
    for one_store in places_result['results']:
        name = one_store['name']
        address = one_store['formatted_address']
        # TODO: not all stores have a rating... fix the error
        rating = one_store['rating']
        coordinates = tuple([val for val in one_store['geometry']['location'].values()])  # list of the lat and long
        store = Store(name, address, rating, coordinates, lookup_address)
        stores.append(store)
    return stores


def main():
    # TODO: get the address that the program ended up using from the user input, and print the used address
    for lookup_address in unique_dev_zip:
        places_result = get_store_results(lookup_address)
        stores = instantiate_stores(places_result, lookup_address)
        limited_dist_stores = [store for store in stores if store.distance <= 1]  # manually filter to 1 mile radius
        limited_dist_stores.sort(key=lambda x: x.distance)  # sort the list by distance in ascending order
        score = len(limited_dist_stores)  # the score is the number of stores within 1 mile
        print(f'Food score for {lookup_address}: {score}')
    # lookup_address = '245 East 93rd 10128'  # input("Enter the lookup location: ").strip()
    # [print(f'{store.name}, {store.distance}') for store in limited_dist_stores]


if __name__ == '__main__':
    main()


