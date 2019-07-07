
import math
import geocoder

R = 6371000
pi = 3.14159

def radians(c):
    return pi/180 * c

#distance in meters
def distancia(hospital, persona):
    lat1 = radians(float(hospital[0]))
    long1 = radians(float(hospital[1]))
    lat2 = radians(float(persona[0]))
    long2 = radians(float(persona[1]))
    lat = abs(lat2-lat1)
    long = abs(long2 - long1)
    a = math.sin(lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(long/2) **2
    c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
    return R*c


def getLatLong (address):
    g = geocoder.mapquest(address, key='SBCjXsQ99VWjbfwSFYh1UDv3QhzYfyGj')
    lat = g.lat
    lon = g.lng
    return [lat,lon]


def computeLatsAndLongs(hospitals_information):
    for i in range(0,len(hospitals_information)):
        list = getLatLong(hospitals_information[i][2])
        hospitals_information[i][3] = list[0]
        hospitals_information[i][4] = list[1]


