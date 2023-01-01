from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base, Session
import csv

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
        return f"User(id={self.id!r}, sensor_id={self.sensor_id!r}, location={self.location!r}) log"


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

print("Starting the process")

engine = create_engine('postgresql+pg8000://postgres:dontwanttostudy@db', echo=True)

print('opening csv to read data into the database.')
with open('2017-07_bme280sof.csv', newline='') as csvfile:
    print('Do you get inside of here?')
    air_metric_reader = csv.reader(csvfile)
    bme280_array = []

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
        bme280_array.append(bme280)
    
    # batch architecture 
    # line below connects to the database
    with Session(engine) as session:
        Base.metadata.create_all(engine)
        session.commit()
        bme280_small_list = []
        #the below code was too slow. 
        for item in bme280_array:
            # line below: adding a row from the csv file. 
            bme280_small_list.append(item)
            if len(bme280_small_list) >= 1000:
                session.bulk_save_objects(bme280_small_list)
                session.commit()
                bme280_small_list = []
                print('Do you even lift?')

        session.bulk_save_objects(bme280_small_list)
        session.commit()
    
with open('2017-07_sds011sof.csv', newline='') as csvfile1:
    print('Inside of sds011?')

    air_metric_reader = csv.reader(csvfile1)
    sds011_array = []
    for row in air_metric_reader:
        id,sensor_id,location,lat,lon,timestamp, p1, p2= row
        # skipping header row
        if (location == 'location'):
            continue

        id = int(id)
        sensor_id = int(sensor_id)
        location = int(location)
        lat = float(lat)
        lon = float(lon)
        #some of p1 and p2 are empty strings. 
        p1 = float(p1) if p1 != '' else 0.0
        p2 = float(p2) if p2 != '' else 0.0

        sds011 = Sds011(id = id, sensor_id= sensor_id, location= location, lat=lat, lon=lon, p1=p1, p2=p2, timestamp= timestamp)
        sds011_array.append(sds011)
    
    # batch architecture 
    # line below connects to the database
    with Session(engine) as session:
        # line below: it creates all the database.
        Base.metadata.create_all(engine)
        session.commit()
        small_list = []
        for item in sds011_array:
            small_list.append(item)
            if len(small_list) >= 1000:
                session.bulk_save_objects(small_list)
                session.commit()
                small_list = []
        session.bulk_save_objects(small_list)
        session.commit()
