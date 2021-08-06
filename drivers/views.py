from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Driver, DriverTwitterMetrics


def index(request):
    drivers = Driver.objects.order_by("position")
    return JsonResponse(serialize("json", drivers), safe=False)


def detail(request, driver_id):
    driver = get_object_or_404(Driver, pk=driver_id)
    return JsonResponse(serialize("json", [driver]), safe=False)


def all_driver_metrics(request):
    drivers = DriverTwitterMetrics.objects.order_by("time", "followers_count")
    return JsonResponse(serialize("json", drivers), safe=False)


def driver_metrics(request, driver_id):
    driver = get_list_or_404(DriverTwitterMetrics, driver_id=driver_id)
    data = serialize("json", driver)
    return JsonResponse({"data": data, "metadata": {"count": len(driver)}}, safe=False)
