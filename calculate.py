import math

def calc_aqi(concentration: float) -> int:
    'Calculates AQI given pm concentration'
    if 0.0 <= concentration < 12.1:
        return int((concentration/12)*50+0.5)
    elif 12.1 <= concentration < 35.5:
        return int(51+(concentration-12.1)*49/(35.4-12.1)+0.5)
    elif 35.5 <= concentration < 55.5:
        return int(101+(concentration-35.5)*49/(55.4-35.5)+0.5)
    elif 55.5 <= concentration < 150.5:
        return int(151+(concentration-55.5)*49/(150.4-55.5)+0.5)
    elif 150.5 <= concentration < 250.5:
##        print((concentration-150.5)*99/(250.4-150.5)+0.5)
        return int(201+(concentration-150.5)*99/(250.4-150.5)+0.5)
    elif 250.5 <= concentration < 350.5:
        return int(301+(concentration-250.5)*99/(350.4-250.5)+0.5)
    elif 350.5 <= concentration < 500.5:
        return int(401+(concentration-350.5)*99/(500.4-350.5)+0.5)
    elif 500.5 <= concentration:
        return 501

#print(calc_aqi(89.3))

def calc_dist(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    'Returns distance between two sets of latitude and longitude.'
    dlat = math.pi/180*(lat1-lat2)
    dlon = math.pi/180*(lon1-lon2)
    alat = math.pi/180*(lat1+lat2)/2
    radius = 3958.8
    x = dlon * math.cos(alat)
    return math.sqrt(x**2 + dlat**2) * radius

##print(calc_dist(1,1,1,1))


##def calc_dist(lat1: float, lon1: float, lat2: float, lon2: float) -> int:
##    dlat = math.radians(lat1)-math.radians(lat2)
##    dlon = math.radians(lon1)-math.radians(lon2)
##    alat = (math.radians(lat1)+math.radians(lat2))/2
##    radius = 3958.8
##    x = dlon * math.cos(alat)
##    return math.sqrt(x*x + dlat*dlat) * radius
