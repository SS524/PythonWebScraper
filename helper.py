from collections import defaultdict
from customLogger import custom_logger_class

custom_logger_obj = custom_logger_class("helperFunction.log", __name__)
custom_logger = custom_logger_obj.create_custom_logger()


class helper_class:

    def list_of_dictionaries_to_dictionary(self, data):
        try:
            data_default_dict = defaultdict(list)
            for item in data:
                for key in item:
                    data_default_dict[key].append(item[key])
            data_dict = dict(data_default_dict)
            custom_logger.info("List of dictionaries got converted into a dictionary")
            return data_dict
        except Exception as e:
            custom_logger.error(str(e))
    
    def find_key_of_dictionary_by_value(self, value, dictionary):
        try:
            key = "".join([k for k,v in dictionary.items() if v == value])
            custom_logger.info("Key is found in dictionary based on the value")
            return key
        except Exception as e:
            custom_logger.error(str(e))
