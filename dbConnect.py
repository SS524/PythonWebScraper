import os
import uuid
from astrapy.rest import create_client, http_methods
from customLogger import custom_logger_class
from helper import helper_class

custom_logger_obj = custom_logger_class("dbConnection.log", __name__)
custom_logger = custom_logger_obj.create_custom_logger()


class connect_with_db:
    def __init__(self,db_id, db_region, db_token):
        try:
            self.db_id = db_id
            self.db_region = db_region
            self.db_token = db_token
            custom_logger.info("Database variables have been initialized")
        except Exception as e:
            custom_logger.error(str(e))

    def createJSONAstra(self, db_keyspace, db_collection, data):
        try:
            doc_uuid = uuid.uuid4()
            custom_logger.info("We are going to create database client")
            db_client = create_client(astra_database_id = self.db_id, 
                                      astra_database_region = self.db_region, 
                                      astra_application_token = self.db_token)
            custom_logger.info("Database client is created")
            custom_logger.info("We are now going to insert record into the database")
            db_client.request(method = http_methods.PUT,
                              path = f"/api/rest/v2/namespaces/{db_keyspace}/collections/{db_collection}/{doc_uuid}",
                              json_data = helper_class().list_of_dictionaries_to_dictionary(data))
            custom_logger.info("Record is now inserted")
        except Exception as e:
            custom_logger.error(str(e))

