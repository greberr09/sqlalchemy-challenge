##############################
# Import the dependencies.
##############################

# Flask and numpy
from flask import Flask, jsonify
import numpy as np

# path for the db files
import os
from pathlib import Path
import sys
sys.path.append("../")

# sqlalchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, and_

#################################################
# Database Setup
#################################################

# Path to the database
curr_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(curr_dir, 'Resources/hawaii.sqlite')
engine = create_engine(f"sqlite:///{db_path}")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
station = Base.classes.station
measurement = Base.classes.measurement


#################################################
# Flask Setup
#################################################

# Create an app,  pass __name__
app = Flask(__name__)

# global search variables (determined in part 1 of analysis using jupyter notebook)

most_active_station = 'USC00519281'
last_precip_date = '2017-08-23'
prior_year_date = '2016-08-23'


#################################################
# Flask Routes  
#################################################


##############################################################
# Home page
# /
# Define home page action of listing menu of available routes

##############################################################

@app.route("/")
def home():
        return (
            f"Welcome to the Weather Stations API<br/>"
            f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start><end><br/>"
        )

######################################################################
# Preciptation amounts     
#/api/v1.0/precipitation
# Define what to do when a user hits the /api/v1.0/precipitation route

######################################################################

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create and close the db session with each API route call.  This
    # may be a little slower in user response, but ensures that the server
    # does not get swamped with unused sessions as someone sits on
    # a web page result, and also ensures that the session is
    # valid and has not timed out or gotten disconnected or corrupted 
    # while it was open and unused, possibly for a long period of time.
    # Each route has the same code to open and close, so this detailed
    # comment as to why it is not just at the beginning and end of
    # the Python file is only included once here.

    # Create session (link) from Python to the hawaii database
    session = Session(engine)

    # Query the measurement data for the last twelve months

    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= prior_year_date).\
        order_by(measurement.date).all()

    session.close()

    # Convert the query results from the precipitation analysis to a dictionary 
    # using date as the key and prcp as the value.
  
    #precip_list = list(np.ravel(results))

    precip_dict = [{'date': result[0], 'precipitation': result[1]} for result in results]

   
    # Return the JSON representation of the dictionary.

    return jsonify(precip_dict)

###################################################################
# Stations list
# /api/v1.0/stations
# Define what to do when a user hits the /api/v1.0/stations route

###################################################################

@app.route("/api/v1.0/stations")
def get_stations():

     # Create the session (link) from Python to the hawaii database
    session = Session(engine)

    # Query the station table in the database
    results = session.query(station.station, station.name, station.latitude, station.longitude, station.elevation).all()

    session.close()

    # Create a stations dictionary so the end user of the json 
    # has the field names to work with, not just the data.

    stations_list = [{'station': result[0], 'name': result[1], 'latitude': result[2], 'longitude': result[3], 'elevation': result[4]} for result in results]
   
    # Return a JSON list of stations 
    return jsonify(stations_list)

##########################################################
# Temperature observations
# /api/v1.0/tobs
# Define what to do when a user hits the /api/v1.0/tobs route

##########################################################

@app.route("/api/v1.0/tobs")
def get_temps():

    # Create session (link) from Python to the hawaii database
    session = Session(engine)

    # Query the dates and temperature observations of the most-active station for the previous year
    
    results= session.query(measurement.date, measurement.tobs).\
                    filter(and_(measurement.station == most_active_station,
                                measurement.date >= prior_year_date)).\
                    order_by(measurement.date).all()

    session.close()

    # Convert the query results from the temperature observations to a dictionary 
    # so json user has the field names available to query, not just the data.
  
    #precip_list = list(np.ravel(results))

    active_station_temps= [{'date': result[0], 'precipitation': result[1]} for result in results]


    # Return the JSON representation of the dictionary.

    return jsonify(active_station_temps)

    active_station_temps = [{'date': result[0], 'temperature': result[1]} for result in results]

    #Return a JSON list of temperature observations for the previous year.

    return jsonify(active_station_temps)


################################################################
# Temperatures with user-entered start or start-stop dates
# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# Define what to do when a user hits the /api/v1.0/<start> route
#
################################################################

@app.route("/api/v1.0/start")
def get_temps_start(start='2016-08-23'):
    return "Start temp: {start}"

#####################################################################
# Temperatures with user-entered  start and stop dates
# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# define what to do when a user hits the /api/v1.0/<start><end> route
#
#####################################################################

@app.route("/api/v1.0/start-end")
def get_temp_range(start='2016-08-23', end='2017-08-23'):
    # Route logic
 

    #Return a JSON list of the minimum temperature, the average temperature, and the 
    #maximum temperature for a specified start or start-end range.

    #For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than 
    # or equal to the start date.

    #For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the 
    # dates from the start date to the end date, inclusive.


    #Return a JSON list of the minimum temperature, the average temperature, and the 
    #maximum temperature for a specified start or start-end range.

    #For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than 
    # or equal to the start date.

    #For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the 
    # dates from the start date to the end date, inclusive.



    # hints
    # Join the station and measurement tables for some of the queries.

    # Use the Flask jsonify function to convert your API data to a valid JSON response object.

    return f"Start: {start}, End: {end}"

###################################################
# Main processing
##################################################

if __name__ == "__main__":
    app.run(debug=True)

