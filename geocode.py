import urllib.parse
import urllib.request
import json
from pathlib import Path
import sys

# Test Variables

# Forward Geo Local
#path = Path('/Users/ethanarroyo/Documents/project3/BrenHall.json')
##path = Path('BrenHall.json')
#path = Path('/Users/ethanarroyo/Documents/project3/get_aqi.py')

# Forward Geo API
# , ('addressdetails','1')
##
##query_params = [('q','Puente Hills Preserve Trail Parking'), ('format','json'),('Referer','https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/erarroyo')]
##query = urllib.parse.urlencode(query_params)
##url_base = 'https://nominatim.openstreetmap.org/search?'
##url = url_base + query
##
# Reverse Geo Local
##
# Reverse Geo API
##bren_lat = 33.6432477
##bren_lon = -117.84186526398847
##
##r_query_params = [('lat', bren_lat), ('lon', bren_lon), ('format','json'),('Referer','https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/erarroyo')]
# r_query = urllib.parse.urlencode(r_query_params) #encoding: utf?
##r_url_base = 'https://nominatim.openstreetmap.org/reverse?'
##r_url = r_url_base + r_query


class ForwardGeoLocal:
    def __init__(self, path: Path):
        self._path = path

    def get_lat_lon(self) -> (float, float):
        'Returns latitude and logitude of location based on path'
        try:
            with self._path.open() as file:
                try:
                    location_info = json.load(file)[0]
                    return float(location_info['lat']), float(location_info['lon'])
                except json.decoder.JSONDecodeError:
                    print('FAILED')
                    print(self._path)
                    print('FORMAT')
                    sys.exit()
        except FileNotFoundError:
            print('FAILED')
            print(self._path)
            print('MISSING')
            sys.exit()


class ForwardGeoAPI:
    def __init__(self, url: str):
        self._url = url

    def get_lat_lon(self) -> (float, float):
        'Returns latitude and logitude of location based on url'
        response = None
        try:
            request = urllib.request.Request(self._url)
            response = urllib.request.urlopen(request)
            location_info = json.load(response)[0]
            if response != None:
                response.close()
            return float(location_info['lat']), float(location_info['lon'])

        except HTTPError as e:
            print('FAILED')
            print(e.code, self._url)
            print('NOT 200')
            close_quit(response)

        except URLError as e:
            print('FAILED')
            print(self._url)
            print('NETWORK')
            close_quit(response)

        except json.decoder.JSONDecodeError:
            print('FAILED')
            print('200', self._url)
            print('FORMAT')
            close_quit(response)


class ReverseGeoLocal:
    def __init__(self, path: Path):
        self._path = path

    def get_info(self) -> (str, str, str):
        'Returns latitude, longitude, and display_name based on path.'
        try:
            with self._path.open() as file:
                location_info = json.load(file)
                return location_info['lat'], location_info['lon'], location_info['display_name']

        except FileNotFoundError:
            print('FAILED')
            print(self._path)
            print('MISSING')
            sys.exit()

        except json.decoder.JSONDecodeError:
            print('FAILED')
            print(self._path)
            print('FORMAT')
            sys.exit()


class ReverseGeoAPI:
    def __init__(self, url: str):
        self._url = url

    def get_info(self) -> (str, str, str):
        'Returns latitude, longitude, and display_name based on url.'
        response = None
        try:
            request = urllib.request.Request(self._url)
            response = urllib.request.urlopen(request)
            location_info = json.load(response)
            if response != None:
                response.close()
            return location_info['lat'], location_info['lon'], location_info['display_name']

        except HTTPError as e:
            print('FAILED')
            print(e.code, self._url)
            print('NOT 200')
            close_quit(response)

        except URLError as e:
            print('FAILED')
            print(self._url)
            print('NETWORK')
            close_quit(response)

        except json.decoder.JSONDecodeError:
            print('FAILED')
            print('200', self._url)
            print('FORMAT')
            close_quit(response)


def search_url(description: str) -> str:
    'Returns formatted url for searching Nominatim.'
    param_list = [('q', description), ('format', 'json'), ('Referer',
                                                           'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/erarroyo')]
    params = urllib.parse.urlencode(param_list)
    url = 'https://nominatim.openstreetmap.org/search?' + params
    return url


def reverse_url(lat: float, lon: float) -> str:
    'Returns formatted url for reverse searching Nominatim.'
    param_list = [('lat', lat), ('lon', lon), ('format', 'json'), ('Referer',
                                                                   'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/erarroyo')]
    params = urllib.parse.urlencode(param_list)
    url = 'https://nominatim.openstreetmap.org/reverse?' + params
    return url


def close_quit(response):
    'Quits response if open and quits program.'
    if response != None:
        response.close()
    sys.quit()


# ForwardGeo Tests
##
##ForwardGeoLocal_test = ForwardGeoLocal(path)
# print(ForwardGeoLocal_test.get_lat_lon())
##
##ForwardGeoAPI_test = ForwardGeoAPI(url)
# print(ForwardGeoAPI_test.get_lat_lon())


# ReverseGeo Tests
##
##ReverseGeoAPI_test = ReverseGeoAPI(r_url)
# print(ReverseGeoAPI_test.get_info())
