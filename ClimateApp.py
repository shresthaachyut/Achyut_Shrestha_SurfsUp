import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date - Replace start_date with your own date in yyyy-mm-dd format <br/>" 
        f"/api/v1.0/start_date/end_date - Replace start_date and end_date with your own date in yyyy-mm-dd format<br/>"
        f"Note: start_date cannot be less than  '2010-01-01' <br/>"
        f"Note: end_date cannot be greater than  '2017-08-23' <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # An empty list
    date_prep = []

    # Query all date and Precipitation
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.prcp).all()

    for result in results:
            date_prep_temp = {"date": result[0], "precp": result[1]}
            date_prep.append(date_prep_temp)
    
    return jsonify(date_prep)

@app.route("/api/v1.0/stations")
def station_names():
    # An empty list
    stations = []

    # Query all Stations
    session = Session(engine)
    results = session.query(Station.station,Station.name).all()
    for result in results:
        stations_temp = {"StationId": results[0][0], 
                         "StationName": result[1]}
        stations.append(stations_temp)
    
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def temperature():
    date_temperature = []

    # Query all Stations
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.tobs).all()
    for result in results:
        date_temp = {"date": result[0],"Temperature": result[1]}
        date_temperature.append(date_temp)
    
    return jsonify(date_temperature)

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    date_temp_details = []

    # Query TMIN, TAVG, and TMAX
    session = Session(engine)
    results = session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >=start_date).group_by(Measurement.date)
    for result in results:
        date_temp_det = {"date": result[0],
                    "min_temperature": result[1],
                    "max_temperature": result[2],
                    "average_temperature": result[3]}
        date_temp_details.append(date_temp_det)
    if start_date < '2010-01-01' or start_date > '2017-08-23' :
        return('Please enter valid start_date')
    else:
        return jsonify(date_temp_details)


@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end_date(start_date,end_date):
    date_temp_details = []

    # Query TMIN, TAVG, and TMAX
    session = Session(engine)
    results = session.query(Measurement.date,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >=start_date).filter(Measurement.date <= end_date).group_by(Measurement.date)
    for result in results:
        date_temp_det = {"date": result[0],
                    "min_temperature": result[1],
                    "max_temperature": result[2],
                    "average_temperature": result[3]}
        date_temp_details.append(date_temp_det)
    
    if start_date < '2010-01-01' or start_date > '2017-08-23' or end_date > '2017-08-23' or end_date < '2010-01-01':
        return('Please enter valid start_date and end_date')
    elif start_date > end_date:
        return("End date cannot be lesser than Start date")
    else:    
        return jsonify(date_temp_details)

if __name__ == '__main__':
    app.run(debug=True)
