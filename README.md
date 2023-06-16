
This challenge analyzes data from weather stations in Hawaii in order to assit with planning a long vacation
to Honolulu.   In particular, the project examines temperature and precipitation data collected from the various weather stations, over a period of at least the previous year, and conducts various statistical analyses on that data.

The challenge uses the sqlalchemy ORM in two ways, in a jupyter notebook, "hawaii-climate.ipynb," and in a flask API, which is run in a Python script, "app.py," creates an app on the server listening on localhost port 5000.  The home route for that app displays a list of routes (URLs) that can be called to query the database.

The data are stored in a sqllite database, "hawaii.sqllite," in the "Resources" subfolder in the project direcory.  That folder also contains .csv files of the data from the database tables.   Both Python scripts should be run from the directory where they are stored, so the relative path to the database files is correct.   

A separate folder of screen_shots of the flask API running is also included.

The jupyter notebook script uses Pandas, numpy, and matplotlib to perform some of the analyses on 
the data set and to plot the results.  A bar plot of the precipitation data, and a histogram of the temperature data, are produced.

The sqlalchemy automapper is used to reflect the database tables into classes, and the database queries are all
done using sqlalchemy classes rather than using raw sql selects, which sqlalchemy also supports.  

Once thet initial data analysis was complete, and the most active weather station, as well as the dates for the most recent twelve months of readings were determined in the juptyer notebook, the flask API was created to display some related information from the weather station data, in three static routes showing precipitation and temperature data for the most recent twelve months.  All of the API queries build a dictionary from the database results, and then return that dictionary as a json object using "jsonify()".   

The API also has two dynamic routes that allow querying of precipitation data for other time periods, given either a start date or a start and end date.  The method of entering the date parameters follows the project requirements of adding them to the end of the route URL in the form /yyyy-mm-dd/ or /yyyy-mm-dd/yyyy-mm-dd/ for the start and end dates to be queried.  The home page of the API explains how these parameters should be entered.   It would be easier and more intuititve for the user, and more flexible, and also would allow having one single route for the start or start/end queries, if keywords were used such as "?start_dt=yyyy-mm-dd&end_dt=yyyy-mm-dd," but the project requirements are to use the "/<<tart>/ and /<start>/<end>/ routes.

The app script does some error checking of whether the dates were properly formatted, and also checks if query results were returned from the database.  A function is used to perform all input checking,  and to raise any errors to the calling route, which can then return a json that displays the error.  While this is more error checkign and try-catch blocks than was done in previous challenges, and is not part of the explicit project requirements, a production environment would need far more error checking before it could be made publiclly avaialable on the internet.
__________________________________________

I have permission from my instructor to hand this project in late due to illness.
__________________________________________
