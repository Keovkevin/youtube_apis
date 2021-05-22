from . import models

from django.http import JsonResponse
from django.core.paginator import Paginator


def get_all(request, **kwargs):
    page = request.GET.get("page", 1)
    query_result = models.YVideoData.objects.all().order_by("-publishing_datetime")
    paginator = Paginator(query_result, 10)
    paginator_response = paginator.page(page)
    result_response = {
        "page_info": {
            "total_page": paginator.num_pages,
            "current_page": page,
            "result_count": paginator_response.object_list.count()
        },
        "result": list(paginator_response.object_list.values()),
    }
    return JsonResponse(result_response)


def search(request, **kwargs):
    title = request.GET.get("title")
    description = request.GET.get("description")
    result = list(
        models.YVideoData.objects.filter(title=title, description=description)
        .order_by("-publishing_datetime")
        .values()
    )
    return JsonResponse({"result": result})