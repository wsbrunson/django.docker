from xml.etree import ElementTree

from celery import shared_task
import requests

from .models import Driver


def convert_driver_xml_to_models(xml_string):
    root = ElementTree.fromstring(xml_string)
    for driver in root[0][0]:
        driver_data = {
            "position": driver.attrib["position"],
            "points": driver.attrib["points"],
            "wins": driver.attrib["wins"],
            "id": driver[0].attrib["driverId"],
            "code": driver[0].attrib["code"],
            "driver_number": driver[0][0].text,
            "given_name": driver[0][1].text,
            "family_name": driver[0][2].text,
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
