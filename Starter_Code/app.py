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
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/station<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/tstats/&lt;start date&gt;</br>"
        "/api/v1.0/tstats/&lt;start date&gt;/&lt;end date&gt;<br/>"
        "Date Format: YYYY-MM-DD"
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

@app.route("/api/v1.0/tstats/<start>")
@app.route("/api/v1.0/tstats/<start>/<end>")
def get_tstats(start, end=dt.date(dt.MAXYEAR, 12, 31)):

    minimum, maximum, average = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).first()

    temp_list = {
        "TMIN": minimum,
        "TMAX": maximum,
        "TAVG": average,
    }    
    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)
