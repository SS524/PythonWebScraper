import json
from flask import Flask, render_template, request
from flask_cors import CORS,cross_origin
from airportExtract import airports_extract_class
from flightExtract import flight_extract_class
from customLogger import custom_logger_class
from dbConnect import connect_with_db
from helper import helper_class



custom_logger_obj = custom_logger_class("serverActivity.log", __name__)
custom_logger = custom_logger_obj.create_custom_logger()

application = Flask(__name__)
app=application


@app.route("/", methods=["GET"])
@cross_origin()
def index():
    try:
        airport_extract_obj = airports_extract_class()
        airport_dictionary = airport_extract_obj.fetch_list_of_airports()
        custom_logger.info("Airport data has been scraped from the website")
        list_of_airports = list(airport_dictionary.values())
        custom_logger.info("The home page is going to be rendered now")
        return render_template("index.html",
                               list_of_airports=list_of_airports)
    except Exception as e:
        custom_logger.error(str(e))


@app.route("/search",methods=["POST","GET"])
@cross_origin()
def flight_search():
    if request.method=="POST":
        try:
            flag = 1
            source = request.form['source']
            destination = request.form['destination']
            date = request.form['date']
            custom_logger.info("Form inputs are received")
        except Exception as e:
            custom_logger.error(str(e))
        try:
            airport_extract_obj = airports_extract_class()
            airport_dictionary = airport_extract_obj.fetch_list_of_airports()
            list_of_airports = list(airport_dictionary.values())
            custom_logger.info("Airport data has been scraped")
        except Exception as e:
            custom_logger.error(str(e))
        try:
            if source == destination:
                flag = 0
                custom_logger.info("Source and destination are same")
                return render_template("index.html",
                                        list_of_airports=list_of_airports,
                                        flag=flag)
            else:
                flag = 1
                custom_logger.info("Source and destination are different")
                source_airport_code = helper_class().find_key_of_dictionary_by_value(source,airport_dictionary)
                destination_airport_code = helper_class().find_key_of_dictionary_by_value(destination,airport_dictionary)
                custom_logger.info("Source and destination airport codes have been identified")
                custom_logger.info("We are now going to scrape all the flights between source and destination")
                flight_extract_obj = flight_extract_class(source_airport_code,destination_airport_code,date)
                list_of_flights = flight_extract_obj.fetch_list_of_flights()
                custom_logger.info("All the flight details have been fetched")
                if len(list_of_flights) != 0:
                    custom_logger.info("We are now going save this data to a cloud database, which is Datastax DB")
                    f = open("dbDetails.json")
                    data = json.load(f)
                    db_client = connect_with_db(data["ASTRA_DB_ID"],
                                                data["ASTRA_DB_REGION"],
                                                data["ASTRA_DB_APPLICATION_TOKEN"])
                
                    db_client.createJSONAstra(data["ASTRA_DB_KEYSPACE"],
                                              data["ASTRA_DB_COLLECTION"],
                                              list_of_flights)
                    custom_logger.info("Record is now inserted to the database table")

                custom_logger.info("We are now going to render all the flight details to our website")
                return render_template("result.html",
                                        list_of_flights=list_of_flights,
                                        source=source,
                                        destination=destination)
        except Exception as e:
            custom_logger.error(str(e))
    else:
        try:
            return render_template("index.html",
                                   list_of_airports=list_of_airports)
        except Exception as e:
            custom_logger.error(str(e))

    

if __name__ == "__main__":
    app.run(port=8000,debug=True)




