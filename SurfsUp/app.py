# Import the dependencies.

# import Flask
from flask import Flask, jsonify




#################################################
# Database Setup
#################################################


# reflect an existing database into a new model

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################

# Create an app,  pass __name__
app = Flask(__name__)


# Create a dictionary to hold a key, value pair.
stations_dict = {"Hello": "World!"}

#################################################
# Flask Routes
#################################################


# /

    ## Start at the homepage.

    ## List all the available routes.

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
        
#/api/v1.0/precipitation

# Define what to do when a user hits the /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    name = "Rain"
    location = "Endless River"
    return f"My name is {name}, and I live in {location}."


    # Convert the query results from your precipitation analysis (i.e. retrieve only the 
# last 12 months of data) to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.



# /api/v1.0/stations
# Define what to do when a user hits the /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def get_stations():
    return jsonify(stations_dict)

    # Return a JSON list of stations from the dataset.



#/api/v1.0/tobs
# Define what to do when a user hits the /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def get_temps():
    return "Welcome to my 'tobs' page!"

    #Query the dates and temperature observations of the most-active station for the previous year of data.

    #Return a JSON list of temperature observations for the previous year.



# /api/v1.0/<start> and /api/v1.0/<start>/<end>

# Define what to do when a user hits the /api/v1.0/<start> route
@app.route("/api/v1.0/start")
def get_temps_start(start='2016-08-23',):
    return "Start temp: {start}"

# define what to do when a user hits the /api/v1.0/<start><end> route
@app.route("/api/v1.0/start-end")
def get_temp_range(start='2016-08-23', end='2017-08-23'):
    # Route logic
    return f"Start: {start}, End: {end}"

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


if __name__ == "__main__":
    app.run(debug=True)

