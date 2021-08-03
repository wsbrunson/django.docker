from xml.etree import ElementTree

from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
import requests

from .models import Driver

# r = requests.get('http://ergast.com/api/f1/current/driverStandings')

def populate_driver_data(xml_string):
    root = ElementTree.fromstring(xml_string)
    for driver in root[0][0]:
        driver_data = {
            'position' : driver.attrib['position'],
            'points' : driver.attrib['points'],
            'wins' : driver.attrib['wins'],
            'id' : driver[0].attrib['driverId'],
            'code' : driver[0].attrib['code'],
            'driver_number' : driver[0][0].text,
            'given_name' : driver[0][1].text,
            'family_name' : driver[0][2].text,
        }
        d = Driver(**driver_data)
        d.save()


def index(request):
    drivers = Driver.objects.order_by('position')
    return JsonResponse(serialize('json', drivers), safe=False)
    

def detail(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    return JsonResponse(serialize('json', [driver]), safe=False)