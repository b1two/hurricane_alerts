#!/usr/bin/python3
"""
Send messages daily about hurricane and volcano.
"""

from bouygues_pysms.bouygues_pysms import BouyguesClient
import logging
import re
import requests

# Config
try:
    from pass_config import *
except ImportError:
    print("Please create your config file like specified in pass_config.example.py.")
    exit(1)

if not all(k in globals() for k in ('DEBUG', 'MY_NAME', 'MY_PASSWORD', 'MY_PHONE_NUMBER')):
    print("Please correctly complete the config file.")
    exit(1)


logging.basicConfig()
logging.root.setLevel(logging.WARNING)
logger = logging.getLogger("bouygues_pysms")
logger.setLevel(logging.WARNING)


class hurricane_api:

    def __init__(self):
        self.session = requests.Session()

        #self.url_hurricane = "https://www.nhc.noaa.gov/gtwo.php?basin=atlc&fdays=5"
        self.url_hurricane = "https://web.archive.org/web/20190903123638/https://www.nhc.noaa.gov/gtwo.php?basin=atlc&fdays=5"
        self.url_jenny = "https://www.volcanodiscovery.com/kick-em-jenny/news/70958/Kick-em-Jenny-volcano-West-Indies-Grenada-activity-update-Elevated-seismicity.html"

        self.data_hurricane = ""
        self.data_jenny = ""

        self.data_clean_hurricane = ""

    def __clean_data_hurricane(self):
        replacements = {
            "$$": "",
            "\n": " ",
        }
        temp = self.data_hurricane
        for pattern, new_val in replacements.items():
            temp = temp.replace(pattern, new_val)

        temp = re.sub(r"\s+", " ", temp).strip()
        self.data_clean_hurricane = temp

    def update_forecast(self):
        """ Retrieving data from huricane center """
        hurricane_raw = self.session.get(self.url_hurricane)
        # We cannot use [.\s] as . is considered litteral in []
        self.data_hurricane = re.search(r"For the North Atlantic\.\.\.Caribbean Sea and the Gulf of Mexico:\n\n([ -~\s]*)\s*Forecaster",
                                        hurricane_raw.content.decode('utf-8')).group(1)

        """ Retrieving data for Kick'em Jenny """
        jenny_raw = self.session.get(self.url_jenny)
        self.data_jenny = re.search(r"\(([0-9]) out of 5\)",
                                    jenny_raw.content.decode('utf-8')).group(1)

    def is_there_hurricane(self):
        return "Tropical cyclone formation is not expected during the next 5 days." not in self.data_hurricane

    def get_forecast_short(self):
        if self.is_there_hurricane():
            return "Attention, il peut y avoir un cyclone de prévu dans les 5 prochains jours. Echelle " + self.data_jenny + "/5 Kick'em Jenny."
        else:
            return "Pas de cyclone prévu dans les 5 prochains jours. Echelle " + self.data_jenny + "/5 Kick'em Jenny."

    def get_forecast_full(self):
        if self.is_there_hurricane():
            self.__clean_data_hurricane()
            return self.data_clean_hurricane + ". Echelle " + self.data_jenny + "/5 Kick'em Jenny."
        else:
            return "Pas de cyclone prévu dans les 5 prochains jours. Echelle " + self.data_jenny + "/5 Kick'em Jenny."



def main():
    """ Retrieving data """
    hurricane_center = hurricane_api()
    hurricane_center.update_forecast()

    if DEBUG:
        print("Full forecast :")
        print(hurricane_center.get_forecast_full())
        print(len(hurricane_center.get_forecast_full()))
        print("\nShort forecast :")
        print(hurricane_center.get_forecast_short())

    else:
        """ Sending SMSs """
        client = BouyguesClient(MY_NAME, MY_PHONE_NUMBER, MY_PASSWORD)
        client.send(hurricane_center.get_forecast_short, RECIPIENTS)

if __name__ == "__main__":
    main()

