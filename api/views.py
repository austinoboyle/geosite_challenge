from api.models import Request
from api.serializers import RequestSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import subprocess


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
    def get(self, request, pk):
        r = get_object_or_404(Request, pk=pk)
        serializer = RequestSerializer(r)
        return Response(serializer.data)
