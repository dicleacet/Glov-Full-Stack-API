from django.http import HttpResponse,JsonResponse
import jwt
import random
import time

from django.conf import settings

def index(request):
    return HttpResponse(f'{{"status":1,"message":"Hello user#{request.user}","user":{request.user},"group":{int(request.user) % 10},"rate":{request.rate},"stream_seq":{request.stream_seq}}}', content_type='application/json')


def generateCode(request):
    code = str(random.randint(100, 999))
    encoded_jwt = jwt.encode({"user": f'USER{code}'}, settings.JWT_SECRET, algorithm="HS256")
    return HttpResponse(f'{{"status":1,"stream":{encoded_jwt}}}', content_type='application/json')


def stream(request):
    stream = request.GET.get('stream')
    if stream != "true" and stream != "false":
        return HttpResponse(f'{{"status":0,"stream":{stream}}}', content_type='application/json', status=400)

    if stream == "true":
        for i in range(5):
            data = {
                "message": "stream is true",
                "stream_seq": i + 1
            }
            response = JsonResponse(data)
            time.sleep(1)
        return response
    else:
        data = {
            "message": "stream is false",
            "stream_seq": 0
        }
        return JsonResponse(data)
