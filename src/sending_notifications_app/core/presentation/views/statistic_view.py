from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods

from core.business.services import get_detailed_message_statistics_service, get_mailing_statistics_service


@method_decorator(require_http_methods(["GET"]), name="dispatch")
class MailingStatisticsView(View):
    def get(self, request, mailing_id):
        statistics = get_mailing_statistics_service(mailing_id)
        return JsonResponse(statistics)

@method_decorator(require_http_methods(["GET"]), name="dispatch")
class DetailedMessageStatisticsView(View):
    def get(self, request, mailing_id):
        detailed_statistics = get_detailed_message_statistics_service(mailing_id)
        return JsonResponse(detailed_statistics, safe=False)
