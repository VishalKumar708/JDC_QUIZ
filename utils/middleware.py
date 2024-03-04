

import json
from django.http import JsonResponse
from django.urls import resolve
from rest_framework import status
import logging


error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')


class ValidateURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # check url is valid or not
        print('middleware calling')
        try:
            resolve(request.path_info)
        except Exception as e:
            response_data = {
                'status_code': status.HTTP_404_NOT_FOUND,
                'status': 'failed',
                'data': {'message': f'Requested resource not found.'},
            }
            error_logger.error('Invalid URL.')
            return JsonResponse(response_data, status=404)

        return self.get_response(request)

    def process_exception(self, request, exception):
        # print('exception method called on middleware')
        print('calling process_exception method')
        print('exceptions ==> ', exception)
        if exception:
            response_data = {
                'statusCode': 500,
                'status': 'failed',
                'data': {'message': 'Internal Server Error'},

            }
            error_logger.error(str(exception))
            print(exception)
            return JsonResponse(response_data, status=response_data['statusCode'])
        return None


class JSONCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ['POST', 'PUT']:
            content_type = request.content_type

            if content_type == 'application/json':
                try:
                    json.loads(request.body.decode('utf-8'))
                except json.JSONDecodeError as e:
                    response_data = {
                        'statusCode': 400,
                        'status': 'Failed',
                        'data': {'message': 'Invalid JSON data', 'details': str(e)}
                    }
                    error_logger.error(f'Invalid JSON data. {str(e)}')
                    return JsonResponse(response_data, status=400)
            elif content_type in ('application/x-www-form-urlencoded', 'multipart/form-data'):
                pass
            else:
                response_data = {
                    'statusCode': 400,
                    'status': 'Failed',
                    'data': {'message': f"excepted JSON Data but got '{content_type}'", }
                }
                error_logger.error(f'Invalid JSON data')
                return JsonResponse(response_data, status=400)
        return self.get_response(request)


class InternalServerErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        # print('exception method called on middleware')
        print('calling process_exception method')
        print('exceptions ==> ', exception)
        if exception:
            response_data = {
                'statusCode': 500,
                'status': 'failed',
                'data': {'message': 'Internal Server Error'},

            }
            error_logger.error(str(exception))
            print(exception)
            return JsonResponse(response_data, status=response_data['statusCode'])
        return self.get_response(request)


class CustomizeResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # if hasattr(response, 'status_code'):
        #     return self.process_response(response)
        return response

    def get_status(self, status_code):
        if status_code == 200:
            return 'Success'
        elif status_code == 500:
            return 'Internal Server Error'
        else:
            return 'Failed'

    def process_response(self, response):
        print('process response method called')
        formatted_data = {
            'statusCode': response.status_code,
            'status': self.get_status(response.status_code),
            'data': response.data if hasattr(response, 'data') else None
        }
        return JsonResponse(formatted_data, status=response.status_code)

