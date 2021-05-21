import logging

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from videosapp.utilities.query_utility import QueryUtility

log = logging.getLogger(__name__)


@authentication_classes([])
@permission_classes([])
@method_decorator(csrf_exempt, name='dispatch')
class StoredVideoView(APIView):

    def get(self, request):
        import ipdb;
        ipdb.set_trace()
        data = request.data
        filters = {
            'limit': int(data.get('limit')) if data.get('limit') else 20,
            'page': int(data.get('page')) if data.get('page') else 1,
        }
        filters['offset'] = filters['limit'] * (filters['page'] - 1)
        result = StoredVideoView.get_all_videos(filters)
        return Response({'data': result})

    @staticmethod
    def get_all_videos(filters):
        query = """select yvd.id,yvd.title,yvd.description,yvd.publishing_datetime,yvd.thumbnail_url
        from yvideo_data as yvd
        """
        params = []
        query += ' order by u.publishing_datetime desc'
        query += ' limit %s offset %s'
        params += [filters.get('limit'), filters.get('offset')]
        result = QueryUtility.execute_query(query, params)
        return result