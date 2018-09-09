import os

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apiserver.settings import MEDIA_ROOT


@api_view(['GET'])
def get_file(_, path):
    file_path = os.path.join(MEDIA_ROOT, path)
    if not file_path.endswith('.wav') or not os.path.exists(file_path):
        return Response("Go fuck your self", status=400)
    file = open(file_path, 'rb')
    response = HttpResponse()
    response.write(file.read())
    response['Content-Type'] = 'audio/wav'
    response['Content-Length'] = os.path.getsize(filename=file_path)
    return response