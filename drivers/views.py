from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from .models import Driver
from .tasks import populate_driver_data, log_driver_twitter_metric


def index(request):
    drivers = Driver.objects.order_by("position")
    return JsonResponse(serialize("json", drivers), safe=False)


def detail(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    return JsonResponse(serialize("json", [driver]), safe=False)


def populate_drivers(request):
    populate_driver_data.delay()
    return HttpResponse("ok")


def populate_driver_twitter_metrics(request):
    log_driver_twitter_metric.delay()
    return HttpResponse("ok")


def remove_all_drivers(request):
    Driver.objects.all().delete()
    return HttpResponse("ok")
