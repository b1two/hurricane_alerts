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


def main():
    """ Retrieving data from huricane center """
    session_hurricane = requests.Session()
    response_hurricane = session_hurricane.get("https://www.nhc.noaa.gov/gtwo.php?basin=atlc&fdays=5")
    matches_hurricane = re.search(r"For the North Atlantic\.\.\.Caribbean Sea and the Gulf of Mexico:\n\n([ -~\s]*)\n\n\$\$",
                        response_hurricane.content.decode('utf-8'))
    infos_hurricane = matches_hurricane.groups()[0]
    hurricane = infos_hurricane != "Tropical cyclone formation is not expected during the next 5 days."

    """ Retrieving data for Kick'em Jenny """
    session_volcano = requests.Session()
    response_volcano = session_volcano.get(r"https://www.volcanodiscovery.com/kick-em-jenny/news/70958/Kick-em-Jenny-volcano-West-Indies-Grenada-activity-update-Elevated-seismicity.html")
    matches_volcano = re.search(r"\(([0-9]) out of 5\)",
                                response_volcano.content.decode('utf-8'))
    status_volcano = matches_volcano.groups()[0]

    """ Sending info """
    if DEBUG:
        print("hurricane : ", hurricane)
        print("Alert level : ", status_volcano)

        if not hurricane:
            print("client.send(\"Pas de cyclone prévu dans les 5 prochains jours. Echelle " + status_volcano + "/5 Kick'em Jenny.\", " + str(RECIPIENTS) + ")")
        else:
            print("client.send(\"Attention, il peut y avoir un cyclone de prévu dans les 5 prochains jours. Echelle " + status_volcano + "/5 Kick'em Jenny.\", " + str(RECIPIENTS) + ")")
    else:
        client = BouyguesClient(MY_NAME, MY_PHONE_NUMBER, MY_PASSWORD)

        if not hurricane:
            client.send("Pas de cyclone prévu dans les 5 prochains jours. Echelle " + status_volcano + "/5 Kick'em Jenny.", RECIPIENTS)
        else:
            client.send("Attention, il peut y avoir un cyclone de prévu dans les 5 prochains jours. Echelle " + status_volcano + "/5 Kick'em Jenny.", RECIPIENTS)


if __name__ == "__main__":
    main()

