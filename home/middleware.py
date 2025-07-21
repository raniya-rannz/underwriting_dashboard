import datetime
from django.core.cache import cache
from .functions import traffic_accidents_db_save,rainfall_data_db_save

class TrafficDataFetchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Fetch data only once a day
        last_fetch = cache.get('last_traffic_sync')
        if not last_fetch or (datetime.datetime.now() - last_fetch).days >= 1:
            traffic_accidents_db_save()
            cache.set('last_traffic_sync', datetime.datetime.now(), 86400)

        response = self.get_response(request)
        return response


class RainfallDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Run only once per day
        last_fetch = cache.get('last_rainfall_sync')
        now = datetime.datetime.now()

        if not last_fetch or (now - last_fetch).days >= 1:
            try:
                rainfall_data_db_save()
                cache.set('last_rainfall_sync', now, 86400)  # cache for 1 day
            except Exception as e:
                print(f"[RainfallDataMiddleware] Error fetching rainfall data: {e}")

        response = self.get_response(request)
        return response