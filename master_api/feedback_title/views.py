from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from utils.get_id_by_token import get_user_id_from_token_view
from masterApi.models import MstFeedbackTitle
from .serializer import *
import logging
error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')


class POSTNewFeedbackTitle(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATEFeedbackTitleSerializer(data=request.data, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': {'message': 'Record Added Successfully.'}
                }
                info_logger.info('FeedbackTitle Created Successfully.')
                return Response(response_data)
            response_data = {
                'status': 400,
                'statusCode': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=400)
        except Exception as e:
            error_logger.error(f'An Exception occured while creating new Feedback Title {e}')
            response_data = {
                'status': 500,
                'statusCode': 'failed',
                'data': str(e)
            }
            return Response(response_data, status=500)


class PUTFeedbackTitleById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id, *args, **kwargs):
        try:
            int(id)
            obj = MstFeedbackTitle.objects.get(id=id)
            get_user_id = get_user_id_from_token_view(request)
            serializer = UPDATEFeedbackTitleSerializer(data=request.data, instance=obj, partial=True, context={'user_id_by_token': get_user_id, 'id':id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': {'message': 'Record Updated Successfully.'}
                }
                info_logger.info('Feedback Title Updated Successfully.')
                return Response(response_data)
            response_data = {
                'status': 400,
                'statusCode': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=400)
        except MstFeedbackTitle.DoesNotExist:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': 'Invalid Id'}
            }
            error_logger.error(f'Invalid FeedbackTitle Id. While updating record.')
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'status': 400,
                'statusCode': 'failed',
                'data': f" 'id' excepted a number but got '{id}'."
            }
            return Response(response_data, status=400)
        except Exception as e:
            error_logger.error(f'An Exception occured while updating FeedbackTitle Record. {e}')
            response_data = {
                'status': 500,
                'statusCode': 'failed',
                'data': str(e)

            }
            return Response(response_data, status=500)


class GETFeedbackTitleDetailById(APIView):

    def get(self, request, id, *args, **kwargs):
        try:
            int(id)
            obj = MstFeedbackTitle.objects.get(id=id)
            serializer = GETFeedbackTitleByIdSerializer(obj)
            response_data = {
                'status': 200,
                'statusCode': 'success',
                'data': serializer.data
            }
            info_logger.info('Feedback Title Updated Successfully.')
            return Response(response_data)
        except MstFeedbackTitle.DoesNotExist:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': 'Invalid Id'}
            }
            error_logger.error(f'Invalid FeedbackTitle Id. While fetching record.')
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'status': 400,
                'statusCode': 'failed',
                'data': f" 'id' excepted a number but got '{id}'."
            }
            return Response(response_data, status=400)
        except Exception as e:
            error_logger.error(f'An Exception occured while fetching data from FeedbackTitle. {e}')
            response_data = {
                'status': 500,
                'statusCode': 'failed',
                'data': str(e)

            }
            return Response(response_data, status=500)


class GETAllFeedbackTitleForAdmin(APIView):

    def get(self, request, *args, **kwargs):
        try:

            status = request.GET.get('status')

            if status is None or status.strip().lower() == 'active':
                queryset = MstFeedbackTitle.objects.filter(isActive=True).order_by('order')
            elif status.strip().lower() == 'inactive':
                queryset = MstFeedbackTitle.objects.filter(isActive=False).order_by('order')
            else:
                response_data = {
                    'status': 400,
                    'statusCode': 'failed',
                    'data': {'message': f"'status' expected 'active' or 'inactive' value, but got '{status}'."}
                }
                return Response(response_data, status=400)

            if len(queryset) < 1:
                response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': {"message": ["No Record Found."]}
                }
                return Response(response_data)
            serializer = GETAllFeedbackTitleSerializer(queryset, many=True)
            response_data = {
                'status': 200,
                'statusCode': 'success',
                'data': serializer.data
            }
            return Response(response_data)
        except Exception as e:
            error_logger.error(f'An Exception occured while fetching all FeedbackTitle names from FeedbackTitle table. {e}')
            response_data = {
                'status': 500,
                'statusCode': 'failed',
                'data': str(e)
            }
            return Response(response_data, status=500)


class GETAllFeedbackTitleForDropDown(APIView):

    def get(self, request, *args, **kwargs):
        try:
            query_set = MstFeedbackTitle.objects.filter(isActive=True)
            if len(query_set) < 1:
                response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': {"message": ["No Record Found."]}
                }
                return Response(response_data)
            # print(query_set[0].bloodGroupName)
            serializer = GETAllFeedbackTitleForDropDownSerializer(query_set, many=True)
            response_data = {
                'status': 200,
                'statusCode': 'success',
                'data': serializer.data
            }
            return Response(response_data)
        except Exception as e:
            error_logger.error(f'An Exception occured while fetching all feedback titles from feedbackTitle table. {e}')
            response_data = {
                'status': 500,
                'statusCode': 'failed',
                'data': str(e)
            }
            return Response(response_data, status=500)

