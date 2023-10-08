# import zoneinfo
# from django.utils import timezone

# class TimezoneMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         tzname = request.session.get("django_timezone")
#         if tzname:
#             timezone.activate(zoneinfo.ZoneInfo(tzname))
#         else:
#             timezone.deactivate()
#         return self.get_response(request)

#จัดการ Cache หลังจาก logout
class DisableBrowserCachingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = "no-cache, no-store, must-revalidate"
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response