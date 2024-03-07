
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from utils.get_id_by_token import get_user_id_from_token_view

from .serializer import *
from masterApi.models import MstProfession
import logging
error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')


class POSTProfession(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            get_user_id = get_user_id_from_token_view(request)
            serializer = CREATEProfessionSerializer(data=request.data, context={'user_id_by_token': get_user_id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': {'message': 'Record Added Successfully.'}
                }
                info_logger.info('Profession Created Successfully.')
                return Response(response_data)
            response_data = {
                'status': 400,
                'statusCode': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=400)
        except Exception as e:
            error_logger.error(f'An Exception occured while creating new Profession {e}')
            response_data = {
                'status': 500,
                'statusCode': 'failed',
                'data': str(e)
            }
            return Response(response_data, status=500)


class PUTProfessionById(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id, *args, **kwargs):
        try:
            int(id)
            obj = MstProfession.objects.get(id=id)
            get_user_id = get_user_id_from_token_view(request)
            serializer = UPDATEProfessionSerializer(data=request.data, instance=obj, partial=True, context={'user_id_by_token': get_user_id, 'id':id})
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': {'message': 'Record Updated Successfully.'}
                }
                info_logger.info('Profession Updated Successfully.')
                return Response(response_data)
            response_data = {
                'status': 400,
                'statusCode': 'failed',
                'data': serializer.errors
            }
            return Response(response_data, status=400)
        except MstProfession.DoesNotExist:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': 'Invalid Id'}
            }
            error_logger.error(f'Invalid Profession Id. While updating record.')
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'status': 400,
                'statusCode': 'failed',
                'data': f" 'id' excepted a number but got '{id}'."
            }
            return Response(response_data, status=400)
        except Exception as e:
            error_logger.error(f'An Exception occured while updating "Profession" Record. {e}')
            response_data = {
                'status': 500,
                'statusCode': 'failed',
                'data': str(e)

            }
            return Response(response_data, status=500)


class GETProfessionDetailById(APIView):

    def get(self, request, id, *args, **kwargs):
        try:
            int(id)
            obj = MstProfession.objects.get(id=id)
            serializer = GETProfessionDetailsByIdSerializer(obj)
            response_data = {
                'status': 200,
                'statusCode': 'success',
                'data': serializer.data
            }
            return Response(response_data)
        except MstProfession.DoesNotExist:
            response_data = {
                'status': 404,
                'statusCode': 'failed',
                'data': {'message': 'Invalid Id'}
            }
            error_logger.error(f'Invalid MaritalStatus Id. While fetching record.')
            return Response(response_data, status=404)
        except ValueError:
            response_data = {
                'status': 400,
                'statusCode': 'failed',
                'data': f" 'id' excepted a number but got '{id}'."
            }
            return Response(response_data, status=400)
        except Exception as e:
            error_logger.error(f'An Exception occured while fetching data from MaritalStatus. {e}')
            response_data = {
                'status': 500,
                'statusCode': 'failed',
                'data': str(e)

            }
            return Response(response_data, status=500)


class GETAllProfessionForAdmin(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            status = request.GET.get('status')

            if status is None or status.strip().lower() == 'active':
                queryset = MstProfession.objects.filter(isActive=True).order_by('order')
            elif status.strip().lower() == 'inactive':
                queryset = MstProfession.objects.filter(isActive=False).order_by('order')
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
                    'data': {"message": "No Record Found."}
                }
                return Response(response_data)
            serializer = GETAllProfessionSerializer(queryset, many=True)
            response_data = {
                'status': 200,
                'statusCode': 'success',
                'data': serializer.data
            }
            return Response(response_data)
        except Exception as e:
            error_logger.error(f'An Exception occured while fetching all Profession names from MstProfession table. {e}')
            response_data = {
                'status': 500,
                'statusCode': 'failed',
                'data': str(e)
            }
            return Response(response_data, status=500)


class GETAllProfessionForDropDown(APIView):

    def get(self, request, *args, **kwargs):
        try:
            query_set = MstProfession.objects.filter(isActive=True).order_by('order')
            if len(query_set) < 1:
                response_data = {
                    'status': 200,
                    'statusCode': 'success',
                    'data': {"message": ["No Record Found."]}
                }
                return Response(response_data)
            # print(query_set[0].bloodGroupName)
            serializer = GETAllProfessionForDropDownSerializer(query_set, many=True)
            response_data = {
                'status': 200,
                'statusCode': 'success',
                'data': serializer.data
            }
            return Response(response_data)
        except Exception as e:
            error_logger.error(f'An Exception occured while fetching all Profession names from MstProfession table. {e}')
            response_data = {
                'status': 500,
                'statusCode': 'failed',
                'data': str(e)
            }
            return Response(response_data, status=500)

