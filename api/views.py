from api.models import Request
from api.serializers import RequestSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import subprocess
from api.parsers import PlainTextParser


class RequestList(APIView):
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

    parser_classes = [PlainTextParser]

    def get(self, request, pk):
        r = get_object_or_404(Request, pk=pk)
        serializer = RequestSerializer(r)
        return Response(serializer.data)

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

    def delete(self, request, pk):
        deletion_count, _ = Request.objects.filter(pk=pk).delete()
        if deletion_count == 0:
            return Response(status=400)
        return Response(status=200)
