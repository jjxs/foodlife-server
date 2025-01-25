import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyBmXEEWM1Be4japAKwhd23piFRukY-irpM')

# Geocoding an address
from_geocode = gmaps.geocode('東京都台東区上野4丁目4-5 ')
from_location = from_geocode[0]['geometry']['location']
print(from_location)
exit

to_geocode = gmaps.geocode('日本東京都御徒町駅')
to_location = to_geocode[0]['geometry']['location']

result = gmaps.directions(from_location, to_location)

distance = result[0]['legs'][0]['distance']
print(distance['value'])
