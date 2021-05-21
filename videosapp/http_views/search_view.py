import logging

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from videosapp.models import YVideoData
from django.http import JsonResponse


log = logging.getLogger(__name__)


@authentication_classes([])
@permission_classes([])
@method_decorator(csrf_exempt, name='dispatch')
class SearchView(APIView):

    def get(self, request):
        title = request.GET.get("title")
        description = request.GET.get("description")
        result = list(YVideoData.objects.filter(title = title, description = description).order_by("-publishing_datetime").values())
        return JsonResponse({"result":result})