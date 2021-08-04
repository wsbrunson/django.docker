import logging
import json
from xml.etree import ElementTree

from celery import shared_task
import requests

from .models import Driver, DriverTwitterMetrics
from .twitter import main as twitter_user_lookup
from djangodocker.celery import app


def convert_driver_xml_to_models(xml_string):
    root = ElementTree.fromstring(xml_string)

    with open("/code/drivers/driver_id_to_twitter_profile.json") as f:
        driver_id_to_twitter_profile = json.load(f)

    for driver in root[0][0]:
        driver_id = driver[0].attrib["driverId"]
        driver_data = {
            "position": driver.attrib["position"],
            "points": driver.attrib["points"],
            "wins": driver.attrib["wins"],
            "id": driver_id,
            "code": driver[0].attrib["code"],
            "driver_number": driver[0][0].text,
            "given_name": driver[0][1].text,
            "family_name": driver[0][2].text,
            "twitter_username": driver_id_to_twitter_profile[driver_id],
        }

        Driver.objects.update_or_create(**driver_data)


@shared_task
def populate_driver_data():
    logging.info("starting pull for populating driver data")
    try:
        r = requests.get("http://ergast.com/api/f1/current/driverStandings")
        logging.info("successfully fetched driver data")
    except:
        logging.error("failed to fetch driver data")

    try:
        convert_driver_xml_to_models(r.text)
        logging.error("successfully stored driver data")
    except:
        logging.error("failed to store driver data")


def get_driver_twitter_usernames():
    id_by_username = {}

    for driver in Driver.objects.all():
        id_by_username[driver.twitter_username] = driver.id

    all_usernames = id_by_username.keys()

    return all_usernames, id_by_username


@shared_task
def log_driver_twitter_metric():
    logging.info("starting pull for populating driver metric data from twitter")
    all_usernames, id_by_username = get_driver_twitter_usernames()

    try:
        twitter_data = twitter_user_lookup(all_usernames)
        logging.info("successfully fetched data from twitter")
    except:
        logging.error("failed to fetch data from twitter")

    try:
        for data in twitter_data:
            driver_id = id_by_username[data["username"]]
            driver = Driver.objects.get(id=driver_id)
            public_metrics = data["public_metrics"]
            dtm = DriverTwitterMetrics(driver_id=driver, **public_metrics)
            dtm.save()

        logging.info("successfully saved driver metrics from twitter")
    except:
        logging.error("failed to save driver metrics from twitter")
