import pandas as pd
import numpy
import geocoder


R = 6371000

#pass to radians
def radians(c):
    return pi/180 * c

#distance in meters
def distancia(hospital, persona):
    lat1 = radians(float(hospital[0]))
    long1 = radians(float(hospital[1]))
    lat2 = radians(float(persona[0]))
    long2 = radians(float(persona[1]))
    lat = abs(lat2-lat1)
    long = abs(long2-long1)
    a = sin(lat/2)**2+cos(lat1)*cos(lat2)*sin(long/2)**2
    c = 2*atan2(sqrt(a),sqrt(1-a))
    return R*c

#get lat and longitud of an address
def getLatLong (address):
    g = geocoder.mapquest(address, key='SBCjXsQ99VWjbfwSFYh1UDv3QhzYfyGj')
    lat = g.lat
    lon = g.lng
    return [lat,lon]



name_csv = input('Enter the name of the csv from which you wanna extract the lat and long of the hospitals\n')
hospitals = pd.read_csv(name_csv).values

list = []
print("Lat")
for hospital in hospitals:
    address = hospital[6]
    if not pd.isnull(address):
        l = getLatLong(address)
        print(l[0])

print('Long')
for hospital in hospitals:
    address = hospital[6]
    if not pd.isnull(address):
        l = getLatLong(address)
        print(l[1])