from pathlib import Path
import json
import urllib.request
import urllib.parse
from calculate import calc_aqi
import sys
from urllib.error import HTTPError
from urllib.error import URLError

##path = Path('/Users/ethanarroyo/Documents/project3/purpleair.com:data.json')
##path = Path('/Users/ethanarroyo/Documents/project3/get_aqi.py')

class SensorsLocal:
    def __init__(self, path: Path):
        try:
            with path.open() as file:
                try:
                    self.sensors = json.load(file)
                    self.fields = self.sensors['fields']
                    self.data = self.sensors['data']
                except json.decoder.JSONDecodeError:
                    print('FAILED')
                    print(path)
                    print('FORMAT')
                    sys.exit()
        except FileNotFoundError:
            print('FAILED')
            print(path)
            print('MISSING')
            sys.exit()
            

    def get_filtered_sensors(self, threshold: int):
        'Returns ordered list of sensors above given AQI threshold through filter_sensor().'
        return filter_sensors(self.data, self.fields, threshold)


class SensorsAPI:
    def __init__(self, url: str):
        response = None
        try:
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            self.sensors = json.load(response)
            self.fields = self.sensors['fields']
            self.data = self.sensors['data']

        except HTTPError as e:
            print('FAILED')
            print(e.code, url)
            print('NOT 200')
            close_quit(response)

        except URLError as e:
            print('FAILED')
            print(url)
            print('NETWORK')
            close_quit(response)

        except json.decoder.JSONDecodeError:
            print('FAILED')
            print('200', url)
            print('FORMAT')
            close_quit(response)

        
        finally:
            if response != None:
                response.close()

    def get_filtered_sensors(self, threshold: int) -> list[list[float]]:
        'Returns ordered list of sensors above given AQI threshold through filter_sensor().'
        return filter_sensors(self.data, self.fields, threshold)


def filter_sensors(sensor_data: list[list[int]], sensor_fields: list[int], threshold: int) -> list[list[int]]:
    'Returns ordered list of sensors above given AQI threshold'
    pm_ind = sensor_fields.index('pm')
    age_ind = sensor_fields.index('age')
    type_ind = sensor_fields.index('Type')
    #lat_ind = self.fields.index('Lat')
    #lon_ind = self.fields.index('Lon')
    #ind_list = [pm_ind,age_ind,type_ind,lat_ind,lon_ind]
    
    sensor_list = list()
    for entry in sensor_data:
        try:
            if calc_aqi(entry[pm_ind]) >= threshold and entry[age_ind] < 3600 and entry[type_ind] == 0:
                sensor_list.append(entry)
        except TypeError:
            pass
    sorted_sensors = sorted(sensor_list, key = lambda x: x[pm_ind], reverse = True)
    return sorted_sensors


def close_quit(response) -> None:
    'Quits response if open and quits program.'
    if response != None:
        response.close()
    sys.quit()




if __name__ == '__main__':
##    sensors = SensorsLocal(path)
##    sensor_list = sensors.get_filtered_sensors(150)
##    print(len(sensor_list))
    
    
##    li = [[1,4,7],[3,6,9],[2,1,8]]
##    sorted_li = sorted(li, key = lambda x: x[2], reverse = True)
##    print(sorted_li)


    url = 'https://www.purpleair.com/data.json'
    sensors = SensorsAPI(url)
    print(len(sensors.get_filtered_sensors(200)))



