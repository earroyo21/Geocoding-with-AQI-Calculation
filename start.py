# Ethan Arroyo 40315485

from geocode import *
from get_aqi import *
from calculate import *
from pathlib import Path


def main():
    'Main function that runs through overall code'
    center_input = input().split(' ')
    dist_max = int(input().split(' ')[1])
    pm_min = int(input().split(' ')[1])
    entry_max = int(input().split(' ')[1])
    data_input = input().split(' ')
    reverse_input = input().split(' ')

    center = get_center(center_input)
    print('CENTER', display_lat_lon(center[0], center[1]))

    valid_sensors = get_valid_sensors(data_input, pm_min)

    nearby_sensors = range_filtered_sensors(
        valid_sensors, center, dist_max, entry_max)

    n = 0
    for sensor in nearby_sensors:
        print('AQI ' + str(calc_aqi(sensor[1])))
        print(display_lat_lon(sensor[27], sensor[28]))
        if reverse_input[1] == 'FILES':
            path_str = reverse_input[2+n]
            print_sensor(path_str, reverse_input)
            n += 1
        if reverse_input[1] == 'NOMINATIM':
            url = reverse_url(sensor[27], sensor[28])
            print_sensor(url, reverse_input)


def get_center(center_in: list[str]) -> (float, float):
    'Gets center input then returns latitutde and longitutde'
    if center_in[1] == 'FILE':
        path = Path(center_in[2])
        center = ForwardGeoLocal(path)
    if center_in[1] == 'NOMINATIM':
        description = ' '.join(center_in[2:])
        center = ForwardGeoAPI(search_url(description))
    return center.get_lat_lon()


def get_valid_sensors(data_input: list[str], threshold: int) -> list[list[float]]:
    'Returns ordered list of sensors above given AQI threshold.'
    sensors = None
    if data_input[1] == 'FILE':
        path = Path(data_input[2])
        sensors = SensorsLocal(path)
    if data_input[1] == 'PURPLEAIR':
        sensors = SensorsAPI('https://www.purpleair.com/data.json')
    return sensors.get_filtered_sensors(threshold)


def range_filtered_sensors(valid_sensors: list[list[int]], center: (float, float), dist_max: int, entry_max: int) -> list[list[float]]:
    'Returns list of sensors filtered for range, capped at given max.'
    filtered_sensors = list()
    for sensor in valid_sensors:
        # print(sensor[27],sensor[28])
        try:
            dist = calc_dist(center[0], center[1], sensor[27], sensor[28])
            if dist <= dist_max:
                filtered_sensors.append(sensor)
        except TypeError:
            pass
        finally:
            if len(filtered_sensors) == entry_max:
                break
    return filtered_sensors


def print_sensor(info: str, reverse_input: list[str]) -> None:
    'Prints description of given location'
    if reverse_input[1] == 'FILES':
        path = Path(info)
        location = ReverseGeoLocal(path)
    if reverse_input[1] == 'NOMINATIM':
        location = ReverseGeoAPI(info)
    location_info = location.get_info()
    print(location_info[2])


def display_lat_lon(lat: float, lon: float) -> str:
    'Returns string of correctly formatted latitude and longitutde'
    lat_lon = ''
    if lat > 0:
        lat_lon += str(lat) + '/N '
    else:
        lat_lon += str(abs(lon)) + '/S '
    if lon > 0:
        lat_lon += str(lon) + '/E'
    else:
        lat_lon += str(abs(lon)) + '/W'
    return lat_lon


if __name__ == '__main__':
    main()
