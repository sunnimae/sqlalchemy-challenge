# Import the dependencies
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np

from datetime import datetime, date, timedelta
import datetime as dt

#################################################
# Database Setup
#################################################


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
Base.classes.keys

# Save references to each table
hawaii_station = Base.classes.station
measurement = Base.classes.measurement


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/start date</br>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start date/end date<br/>"
        f"Date Format: YYYY-MM-DD"
        )
    

@app.route("/api/v1.0/precipitation")
def precipitation():
        
        results = session.query(measurement.date, measurement.prcp).\
            filter(measurement.date<='2017-08-23').\
            filter(measurement.date>='2016-08-23').\
            order_by(measurement.date.desc()).all()
        
        precipitation = list(np.ravel(results))
        return jsonify(precipitation)

@app.route("/api/v1.0/station")
def places():
    
    results1 = session.query(hawaii_station.id, hawaii_station.station, hawaii_station.name, hawaii_station.latitude, hawaii_station.longitude, hawaii_station.elevation).all()
    
    places = []
    for id, station, name, latitude, longitude, elevation in results1:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        places.append(station_dict)
    return jsonify(places)

@app.route("/api/v1.0/tobs")
def hawaii_tobs():

    results2 = session.query(measurement.id, measurement.date, measurement.station, measurement.prcp, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date<='2017-08-23').\
        filter(measurement.date>='2016-08-23').order_by(measurement.id).all()
   
    station_tobs = []
    for id, date, station, precipitation, tobs in results2:
        tobs_dict = {}
        tobs_dict["id"]=id
        tobs_dict["date"]=date
        tobs_dict["station"]=station
        tobs_dict["precipitation"]=precipitation
        tobs_dict["tobs"]=tobs
        station_tobs.append(tobs_dict)
    return jsonify(station_tobs)

@app.route("/api/v1.0/<start>", methods=["GET"])
def get_temperatures_start(start):

    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()

    temperatures = []
    for minimum, maximum, average in results:
        temp_dict = {}
        temp_dict["minimum"]= minimum
        temp_dict["maximum"]= maximum
        temp_dict["average"]= average
        temperatures.append(temp_dict)
    return jsonify(temperatures)


@app.route("/api/v1.0/<start>/<end>", methods=["GET"])
def get_tobs(start, end):
   
    results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()

    temp_stats = []
    for minimum, maximum, average in results:
        temp_dict = {}
        temp_dict["minimum"] = minimum
        temp_dict["maximum"] = maximum
        temp_dict["average"] = average
        temp_stats.append(temp_dict)
    return jsonify(temp_stats)

session.close()

if __name__ == '__main__':
    app.run(debug=True)
