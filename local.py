from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base, Session
import csv

from sqlalchemy import create_engine
#connection string: string inside of crate_engine 
#connection string is like a url. 
#there are different kinds of connection strings. For every ORM it works a little different.
#url has different components and they'll tell you how to connect to the database. 
#they will say where it is, which username and password should i use to connect to the db. which db inside of the db server should i connect to or should i open, what port should i connect to. should i use ssl to connect. 
#create_engine is lazy. I tell it everything it would need to know to connect. But it doesnt until it finds something where i will connect. 
#echo true => it tells it to print the queries into the terminal

print("Starting the process")
#@db => db is the name of the service as it's defined in docker compose on the docker network.

#

#         session.commit()
    
#this is extremly fast.
with open('data/2017-07_sds011sof.csv', newline='') as csvfile:
    air_metric_reader = csv.reader(csvfile)
    sds011_array = []
    for i, row in enumerate(air_metric_reader):
        id,sensor_id,location,lat,lon,timestamp, p1, p2= row
        # skipping header row
        if (location == 'location'):
            continue
        try:
            id = int(id)
            sensor_id = int(sensor_id)
            location = int(location)
            lat = float(lat)
            lon = float(lon)
#some of p1 and p2 are empty strings. 
            p1 = float(p1) if p1 != '' else 0.0
            p2 = float(p2) if p2 != '' else 0.0
            
        except:
            print('this didnt work somehow...', i, row)

        # sds011 = Sds011(id = id, sensor_id= sensor_id, location= location, lat=lat, lon=lon, p1=p1, p2=p2, timestamp= timestamp)
        # sds011_array.append(sds011)
    
    