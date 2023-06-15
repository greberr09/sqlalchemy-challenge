##############################
# Import the dependencies.
##############################

# Flask and numpy
from flask import Flask, jsonify
import numpy as np
import datetime 

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

###############################################
# Functino to check validity of user input dates
################################################

def string_to_date(date_str): 
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"Date '{date_str}' is not a valid date in the format 'yyyy-mm-dd'")

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
            f"Welcome to the Weather Stations API<br/><br/>"
            f"Available Routes:<br/><br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end><br/><br/>"            
            f"For the stats queries, the start date and optional "
            f"end date should be entered in the format yyyy-mm-dd "
            f"and appended after the URL.<br/>  Examples: <br/>"
            f"Stats for a given start date to the last date in the database:  /api/v1.0/2016-01-01<br/>" 
            F"Stats for all dates within an (inclusive) begin-end range: /api/v1.0/2017-01-01/2017-02-28<br/>"         
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

    if results:
        precip_dict = [{'date': result[0], 'precipitation': result[1]} for result in results]
    else:
         return jsonify("No results found", 404)
   
    # Return the JSON representation of the dictionary.

    # The fields will not necessarily be returned in the order 
    # they were added to the dictionary.  Jsonify does not
    # provide a way to order the returned fields and the 
    # specification does not require a particular default order.
    # Different implementations also may return the fields in different orders.

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

    if results:
        stations_list = [{'station': result[0], 'name': result[1], 'latitude': result[2], 'longitude': result[3], 'elevation': result[4]} for result in results]
    else:
        return jsonify('no results found', 404)
    
    # Return a JSON list of stations.  The fields will not
    # necessarily be returned in the order added or in any particular order.

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
  
    if results:
         active_station_temps= [{'date': result[0], 'temperature': result[1]} for result in results]
    else:
        return jsonify('no results found', 404)

    # Return the JSON representation of the dictionary.   Jsonify 
    # does not provide the fields in any partiular order.

    return jsonify(active_station_temps)


################################################################
# Temperature calcs with user-entered start or start-stop dates
#  /api/v1.0/<start> and /api/v1.0/<start>/<end>
################################################################


# /api/v1.0/<start> 
# Define what to do when a user hits the /api/v1.0/<start> route
################################################################

@app.route("/api/v1.0/<start>")
def get_temps_start(start):

    # Create session (link) from Python to the hawaii database
    session = Session(engine)

    # Check the validity of the format and the date the user provided

    try:
        begin_dt = string_to_date(start) 
    except Exception as e:
        return ("Exception occurred for date entered: " + repr(e))


    # Query the dates and temperature observations beginning with the given start date
    # Calculate the minimum, maximum, and average temperature for this date range
    
    results= session.query(func.min(measurement.tobs),
                           func.max(measurement.tobs),
                           func.avg(measurement.tobs)).\
                    filter(measurement.date >= start).all()
    
    session.close()

    # Convert the query results from the temperature observations to a dictionary 
    # so json user has the field names available to query, not just the data.
  
    
    if results: 
        start_dates = [{'start_date': start, 'min_temp': result[0], 'max_temp': result[1], 'avg_temp': result[2]} for result in results]
    else:
         return jsonify('no results found', 404)


    # Return the JSON representation of the dictionary.

    # The fields will not necessarily be returned in the order 
    # they were added to dictionary.  Jsonify specification does not
    # require a particular order

    return jsonify(start_dates)


#####################################################################
# Temperatures with user-entered start and stop dates
# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# define what to do when a user hits the /api/v1.0/<start><end> route
#
#####################################################################
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


@app.route("/api/v1.0/<start>/<end>")
def get_temp_range(start, end):

    # Create session (link) from Python to the hawaii database

    session = Session(engine)

    # check the validity of the start date the user entered
    try:
        date_entered = string_to_date(start) 
    except Exception as e:
        return ("Exception occurred for start date entered: " + repr(e))
    
    # check the validity of the end date provided
    try:
        date_entered = string_to_date(end) 
    except Exception as e:
        return ("Exception occurred for end date entered: " + repr(e))

    # Query the dates and temperature observations beginning with the given start date
    # Calculate the minimum, maximum, and average temperature for this date range
    
    results= session.query(func.min(measurement.tobs),
                           func.max(measurement.tobs),
                           func.avg(measurement.tobs)).\
                    filter(and_ (measurement.date >= start),
                            (measurement.date <= end)).all()

    session.close()

    # Convert the query results to a dictionary so the json user
    # has the field names available to query, not just the data.
  
    if results: 
        start_end_dates = [{'start_date': start,  'end_date': end, 'min_temp': result[0], 'max_temp': result[1], 'avg_temp': result[2]} for result in results]
    else:
         return jsonify('no results found', 404)

    # Return the JSON representation of the dictionary.

    # The fields will not necessarily be returned in the order 
    # they were added to the dictionary.  Jsonify does not
    # provide a way to order the returned fields.

    return jsonify(start_end_dates)


###################################################
# Main driver function:  call flask run() on local server
##################################################

if __name__ == "__main__":
    app.run(debug=True)

