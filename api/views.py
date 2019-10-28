from api.models import Request
from api.serializers import RequestSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import subprocess
from api.parsers import PlainTextParser

from django.utils.decorators import method_decorator
from api.decorators import require_login_or_401

from api.renderers import RequestListRenderer
from rest_framework.renderers import JSONRenderer


class RequestList(APIView):
    """View recent system info.
    Response Shape:
        - requests([Request]): the 10 most recent requests
        - cpu_info(String): output of command: `cat /proc/cpuinfo`
        - date(String): output of command: `date`
    """

    renderer_classes = [JSONRenderer, RequestListRenderer]

    @method_decorator(require_login_or_401)
    def get(self, request, format=None):
        new_request = Request(request_type=request.method)
        new_request.save()
        requests = Request.objects.all()[:10]
        serializer = RequestSerializer(requests, many=True)
        cpu_info = subprocess.check_output(
            ['cat', '/proc/cpuinfo']).decode('utf-8')
        date = subprocess.check_output(['date']).decode('utf-8')
        return Response({'requests': serializer.data, 'cpu_info': cpu_info, 'date': date})


class RequestDetails(APIView):
    """Retrieve, delete, or add comment to a request.
    """
    parser_classes = [PlainTextParser]

    @method_decorator(require_login_or_401)
    def get(self, request, pk):
        r = get_object_or_404(Request, pk=pk)
        serializer = RequestSerializer(r)
        return Response(serializer.data)

    @method_decorator(require_login_or_401)
    def post(self, request, pk):
        try:
            r = Request.objects.get(pk=pk)
        except Request.DoesNotExist:
            return Response({'detail': "Request with id: {} does not exist".format(pk)}, status=400)
        comment_text = request.data.decode('utf-8')
        serializer = RequestSerializer(
            r, data={'comment': comment_text}, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.save()
        return Response(serializer.data)

    @method_decorator(require_login_or_401)
    def delete(self, request, pk):
        deletion_count, _ = Request.objects.filter(pk=pk).delete()
        if deletion_count == 0:
            return Response({'detail': "Cannot delete non-existent request with id: {}.".format(pk)}, status=400)
        return Response(status=200)
