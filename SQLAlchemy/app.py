import datetime as datetime
import numpy as np 
import pandas as pd 

import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#DataBase setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
#Setup complete



app = Flask(__name__)



@app.route("/")
def index():
    return("Available Routes:<br />"
        "/api/v1.0/precipitation<br />"
        "/api/v1.0/stations<br />"
        "/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_perc = []

    for date, prcp in results:
        perc_dict = {}
        perc_dict[date] = prcp
        
        all_perc.append(perc_dict)
    
    return jsonify(all_perc)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
        
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/<start>")
def calc_temps(start):
    session = Session(engine)
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()
    all_calc = []

    for date, tmin, tavg, tmax in results:
        calc_dict = {}
        calc_dict[date] = tmin, tavg, tmax

        all_calc.append(calc_dict)
    
    return jsonify(all_calc)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps2(start, end):
    session = Session(engine)
    results = ession.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    all_calc2 = []

    for date, tmin, tavg, tmax in results:
        calc_dict2 = {}
        calc_dict2[date] = tmin, tavg, tmax

        all_calc2.append(calc_dict2)

if __name__ == "__main__":
    app.run(debug=True)