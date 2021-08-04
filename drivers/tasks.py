import json
from xml.etree import ElementTree

from celery import shared_task
import requests

from .models import Driver, DriverTwitterMetrics
from .twitter import main as twitter_user_lookup


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
        [driver_obj, created] = Driver.objects.update_or_create(**driver_data)

        if created:
            print("{} was created".format(driver_obj))
        else:
            print("{} was updated".format(driver_obj))


@shared_task
def populate_driver_data():
    r = requests.get("http://ergast.com/api/f1/current/driverStandings")
    convert_driver_xml_to_models(r.text)


@shared_task
def log_driver_twitter_metric():
    driver_twitter_usernames_to_id = {}

    for driver in Driver.objects.all():
        driver_twitter_usernames_to_id[driver.twitter_username] = driver.id

    driver_twitter_usernames = driver_twitter_usernames_to_id.keys()

    twitter_data = twitter_user_lookup(driver_twitter_usernames)

    for data in twitter_data:
        driver_id = driver_twitter_usernames_to_id[data["username"]]
        driver = Driver.objects.get(id=driver_id)
        public_metrics = data["public_metrics"]
        dtm = DriverTwitterMetrics(driver_id=driver, **public_metrics)
        dtm.save()
