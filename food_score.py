import googlemaps
from datetime import datetime


class Store:
    def __init__(self, name, address, rating, coordinates):
        self.name = name
        self.address = address
        self.rating = rating
        self.location = coordinates
        self.distance = 0

    def get_distance(self, starting_loc):
        dist = gmaps.distance_matrix(starting_loc, self.location)
        dist = dist['rows'][0]['elements'][0]['distance']['text'].split(' ')
        dist = float(dist[0])
        self.distance = dist * 0.621371  # converting distance from km to miles
        return self.distance


gmaps = googlemaps.Client(key='json_key')


def get_store_results(lookup_address):
    # Geocoding an address
    geocode_result = gmaps.geocode(lookup_address)

    # getting the coordinates for the address
    coordinates = [float(val) for val in geocode_result[0]['geometry']['bounds']['northeast'].values()]

    # Request directions via public transit
    # now = datetime.now() # time and date at this moment

    # directions_result = gmaps.directions("Sydney Town Hall",
    #                                      "Parramatta, NSW",
    #                                      mode="transit",
    #                                      departure_time=now)

    # look up 'market' places within 1 mile of address coordinates (1,609.34 meters = 1 mile)
    # TODO: figure out why the radius is not working
    places_result = gmaps.places(type='grocery_or_supermarket', location=coordinates, radius=1609)
    return places_result


def main():
    lookup_address = '223 Corlies 07711'  # input("Enter the lookup location: ").strip()
    places_result = get_store_results(lookup_address)
    # create list of all the instantiated store classes from the results
    stores = []
    for one_store in places_result['results']:
        #print(one_store, end='\n\n')
        name = one_store['name']
        address = one_store['formatted_address']
        rating = one_store['rating']
        coordinates = tuple([val for val in one_store['geometry']['location'].values()]) # list of the lat and long
        store = Store(name, address, rating, coordinates)
        stores.append(store)
        distance = store.get_distance(lookup_address)
        print(f'{distance=}', end='\n\n')
        # TODO: order the list by distance
    # find the score of the lookup_address
    score = len(stores)
    print(f'Your food score: {score}')


if __name__ == '__main__':
    main()

