from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class Bme280(Base):
    __tablename__ = "bme280"

    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer)
    location = Column(Integer)
    lat = Column(Float)
    lon = Column(Float)
    timestamp = Column(String)
    pressure = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    
    def __repr__(self):
        return f"User(id={self.id!r}, sensor_id={self.sensor_id!r}, location={self.location!r})"


class Sds011(Base):
    __tablename__ = "sds011"
    
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer)
    location = Column(Integer)
    lat = Column(Float)
    lon = Column(Float)
    timestamp = Column(String)
    p1 = Column(Float)
    p2 = Column(Float)

    def __repr__(self):
        return f"Sds011(id={self.id!r}, sensor_id={self.sensor_id!r})"


from sqlalchemy import create_engine
#connection string: string inside of crate_engine 
#connection string is like a url. 
#there are different kinds of connection strings. For every ORM it works a little different.
#url has different components and they'll tell you how to connect to the database. 
#they will say where it is, which username and password should i use to connect to the db. which db inside of the db server should i connect to or should i open, what port should i connect to. should i use ssl to connect. 
#create_engine is lazy. I tell it everything it would need to know to connect. But it doesnt until it finds something where i will connect. 
#echo true => it tells it to print the queries into the terminal
engine = create_engine('postgresql+pg8000://postgres:postgrespw@localhost:49154', echo=True)


import csv
with open('2017-07_bme280sof.csv', newline='') as csvfile:
    air_metric_reader = csv.reader(csvfile)
    super_array_man = []


    for row in air_metric_reader:
        id,sensor_id,location,lat,lon,timestamp,pressure,temperature,humidity = row
        # skipping header row
        if (location == 'location'):
            continue

        id = int(id)
        sensor_id = int(sensor_id)
        location = int(location)
        lat = float(lat)
        lon = float(lon)
        pressure = float(pressure)
        temperature = float(temperature)
        humidity = float(humidity)

        bme280 = Bme280(id = id, sensor_id= sensor_id, location= location, lat=lat, lon=lon, pressure=pressure, temperature=temperature, timestamp= timestamp, humidity=humidity)
        super_array_man.append(bme280)
    
    # batch architecture 
    # line below connects to the database
    with Session(engine) as session:
        # line below: it creates all the database.
        Base.metadata.create_all(engine)
        session.commit()
        session.bulk_save_objects(super_array_man)
        #the below code was too slow. 
        # for index, item in enumerate(super_array_man):
            # line below: adding a row from the csv file. 
            # session.add(item)
            # if index % 1000 == 0:
                #it will commit everything that was added up to this point. 
                # session.commit()
        #line below: in case the number of rows is not exactly divisible by 1000
        session.commit()
    

with open('2017-07_sds011sof.csv', newline='') as csvfile:
    air_metric_reader = csv.reader(csvfile)
    sds011_array = []


    for row in air_metric_reader:
        id,sensor_id,location,lat,lon,timestamp= row
        # skipping header row
        if (location == 'location'):
            continue

        id = int(id)
        sensor_id = int(sensor_id)
        location = int(location)
        lat = float(lat)
        lon = float(lon)
        p1 = float(temperature)
        p2 = float(humidity)

        sds011 = Sds011(id = id, sensor_id= sensor_id, location= location, lat=lat, lon=lon, pressure=pressure, temperature=temperature, timestamp= timestamp, humidity=humidity)
        super_array_man.append(bme280)
    
    # batch architecture 
    # line below connects to the database
    with Session(engine) as session:
        # line below: it creates all the database.
        Base.metadata.create_all(engine)
        session.commit()
        session.bulk_save_objects(sds011_array)
        small_list = []
for item in super_array:
    small_list.append(item)
    if len(small_list) >= 1000:
        session.bulk_save_objects(small_list)
        session.commit()
        small_list = []
session.bulk_save_objects(small_list)
session.commit()
        #the below code was too slow. 
        # for index, item in enumerate(super_array_man):
            # line below: adding a row from the csv file. 
            # session.add(item)
            # if index % 1000 == 0:
                #it will commit everything that was added up to this point. 
                # session.commit()
        #line below: in case the number of rows is not exactly divisible by 1000
        session.commit()

    #todo: do the same thing for the other table