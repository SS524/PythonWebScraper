from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from customLogger import custom_logger_class


custom_logger_obj = custom_logger_class("flightScraping.log", __name__)
custom_logger = custom_logger_obj.create_custom_logger()


class flight_extract_class:

    def __init__(self, source, destination, date):
        try:
            self.url = ("https://www.kayak.co.in/flights/"
                       +source
                       +"-"
                       +destination
                       +"/"
                       +date
                       +"?sort=bestflight_a")
            self.source = source
            self.destination = destination
            self.date = date
            custom_logger.info("Variables are initialized to scrape the flight details")
        except Exception as e:
            custom_logger.error(str(e))

    def fetch_list_of_flights(self):
        try:
            # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
            # chrome_options = Options()
            # chrome_options.add_argument(f"user-agent={user_agent}")
            # chrome_options.add_argument("--no-sandbox")
            # chrome_options.add_argument("--headless")
            # chrome_options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome()
            driver.get(self.url)
            sleep(8)
            custom_logger.info("Connection is established")
        except Exception as e:
            custom_logger.error(str(e))
        try:
            custom_logger.info("Scraping process is now going to be started")
            flight_rows = driver.find_elements(By.CLASS_NAME,"nrc6")
        except Exception as e:
            custom_logger.error(str(e))
        try:
            list_of_flights = []
            for WebElement in flight_rows:
                flight_dictionary = {}
                elementHTML = WebElement.get_attribute("outerHTML")
                elementSoup = BeautifulSoup(elementHTML,"html.parser")
            
                price_text = elementSoup.find("div", class_ = "f8F1-price-text").text[2:].replace(",","")
                flight_dictionary["Price"] = price_text
            
                class_text = elementSoup.find("div", class_ = "aC3z-name").text
                flight_dictionary["Class"] = class_text
            
                airlines_text = elementSoup.find("div", class_ = "J0g6-operator-text").text
                flight_dictionary["Airlines"] = airlines_text
            
                dep_arrival_text = elementSoup.find("div", class_ = "vmXl vmXl-mod-variant-large")
                dep_text = dep_arrival_text.find_all("span")[0].text
                flight_dictionary["Departure"] = dep_text
                arr_text = dep_arrival_text.find_all("span")[2].text
                flight_dictionary["Arrival"] = arr_text
            
                duration_text = elementSoup.find("div", class_ = "xdW8 xdW8-mod-full-airport").text
                flight_dictionary["Duration"] = duration_text
            
                routes_text = elementSoup.find("span", class_ = "JWEO-stops-text").text
                if routes_text != "direct":
                    layover_text = elementSoup.find_all("div", class_ = "c_cgF c_cgF-mod-variant-full-airport")[1].text
                    flight_dictionary["Route"] = str(routes_text
                                                    +" "
                                                    +layover_text)
                else:
                    flight_dictionary["Route"] = routes_text
                list_of_flights.append(flight_dictionary)
            custom_logger.info("Scraping process is now completed")
            return list_of_flights
        except Exception as e:
            custom_logger.error(str(e))
    





