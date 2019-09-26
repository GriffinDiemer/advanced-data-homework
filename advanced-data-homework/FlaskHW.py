# 1. import Flask
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start  :Input your own start date(yyyy-mm-dd).<br/>"
        f"/api/v1.0/start/end   :Input your own start and end dates(yyyy-mm-dd)."

    )

# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'About' page...")
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    precipitation = []
    for date, prcp in results:
        prcp_dict = {date : prcp}
        precipitation.append(prcp_dict)
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'About' page...")
    session = Session(engine)
    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    station = []
    for name in results:
        station.append(name)
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'About' page...")
    session = Session(engine)

    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    date = [recent_date.date for date in recent_date] 

    new_date=dt.datetime.strptime(date[0],'%Y-%m-%d')
    year_ago = new_date - dt.timedelta(days=366)

    past_year = session.query(Measurement.date, Measurement.tobs).\
    order_by(Measurement.date.desc()).\
    filter(Measurement.date > year_ago).all()

    session.close()

    # Convert list of tuples into normal list
    temp = []
    for date, tobs in past_year:
        tobs_dict = {date : tobs}
        temp.append(tobs_dict)
    return jsonify(temp)

@app.route("/api/v1.0/<start>")
def dates(start):

    session = Session(engine)
    answer =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start)

    session.close()

    your_temp = []

    for min, avg, max in answer:
        temp_dict = {}
        temp_dict["min"] = min
        temp_dict["avg"] = avg
        temp_dict["max"] = max
        your_temp.append(temp_dict)
    return jsonify(your_temp)

@app.route("/api/v1.0/<start>/<end>")
def dates_extended(start,end):

    session = Session(engine)
    answer =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    your_temp = []

    for min, avg, max in answer:
        temp_dict = {}
        temp_dict["min"] = min
        temp_dict["avg"] = avg
        temp_dict["max"] = max
        your_temp.append(temp_dict)
    return jsonify(your_temp)


if __name__ == "__main__":
    app.run(debug=False)