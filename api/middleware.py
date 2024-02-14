from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.http import HttpResponse
import jwt
from django.conf import settings

class CustomMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.code = None
        
    def process_request(self, request):
        if request.path == '/api/generate-code':
            response = self.get_response(request)
            return response

        token = request.headers.get("Authorization")
        if not token:
            return HttpResponse('{"status":0,"message":"Token is missing"}', content_type='application/json', status=401)

        encoded_jwt = token.split(" ")[1]
        decoded = jwt.decode(encoded_jwt, settings.JWT_SECRET, algorithms=["HS256"])
        user_code = decoded["user"][-3:]

        self.code = user_code

        stream_seq_key = f'stream_seq_{user_code}'
        
        key = f'rate_limit_{user_code}'
        request_count = cache.get(key, 0)
        if request_count > 3:
            return HttpResponse('{"status":0,"message":"Rate Limit Exceeded"}', status=429, content_type='application/json')

        request.user = user_code
        request.rate = 3 - request_count
        request.stream_seq = cache.get(stream_seq_key, 0)


        response = self.get_response(request)
        return response

    def process_response(self, request, response):
        if response.status_code == 200 or response.status_code == 400:
            user_code = self.code
            stream = request.GET.get('stream', 'false')
            stream_seq_key = f'stream_seq_{user_code}'

            if stream == "true":
                count = cache.get(stream_seq_key, 0)
                cache.set(stream_seq_key, count+1, timeout=360)
            
            key = f'rate_limit_{user_code}'
            request_count = cache.get(key, 0)
            cache.set(key, request_count + 1, timeout=60)

        return response
