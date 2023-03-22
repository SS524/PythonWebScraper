import requests
from bs4 import BeautifulSoup
from customLogger import custom_logger_class


custom_logger_obj = custom_logger_class("airportScraping.log", __name__)
custom_logger=custom_logger_obj.create_custom_logger()


class airports_extract_class:

    def __init__(self):
        try:
            self.url = "https://www.prokerala.com/travel/airports/india/#K"
            custom_logger.info("The URL to scrape the airports data, has been set")
        except Exception as e:
            custom_logger.error(str(e))
            
    def fetch_list_of_airports(self):
        try:
            page = requests.get(self.url)
            custom_logger.info("Connection established")
        except Exception as e:
            custom_logger.error(str(e))
        try:
            soup = BeautifulSoup(page.content,"html.parser")
            custom_logger.info("Scraping process is now going to be started")
            tables = soup.find_all("table",class_="table f-sans-serif")
            table_trs = []
            for table in tables:
                table_trs.append(table.find_all("tr")[2:])
            airport_code_name_dict = {}
            for trs in table_trs:
                for tr in trs:
                    airport_code_name_dict[tr.find_all("td")[2].text] = tr.find("span").text
            airport_code_name_dict["DEL"] = "Delhi"
            custom_logger.info("Scraping is now completed")
            return airport_code_name_dict
        except Exception as e:
            custom_logger.error(str(e))
    






