import time
import json
from django.utils.deprecation import MiddlewareMixin

class ResquestResponselog(MiddlewareMixin):
    def process_request(self,request):
        if request.method in ['POST','PUT','PATCH']:
            request.req_body = request.body
        if str(request.get_full_path()):
            request.start_time = time.time()

    def extract_log_info(self,request,response=None,exception=None):
        log_data = {
            'request method' : request.method,
            'request_path' : request.get_full_path()
        }
        if request.method in ['POST','PUT','PATCH']:
            log_data['request_body'] = json.loads(str(request.req_body,'UTF-8'))
            if response:
                if response['content-type'] == 'application/json':
                    response_body = response.content
                    log_data['response_body'] = response_body

        return log_data

    def process_response(self,request,response):
        if request.method != 'GET':
            if str(request.get_full_path()):
                log_data = self.extract_log_info(request,response)

            return response

    def process_exception(self,request,exception):
        try:
            raise exception
        except Exception:
            request.logger.exception(message="exception occured")
        return exception