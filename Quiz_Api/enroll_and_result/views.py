from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import QuizEnrolmentSerializer
from ..models import QuizEnrollment
from drf_yasg.utils import swagger_auto_schema
import logging
error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')
warning_logger = logging.getLogger('warning')


class POSTQuizEnrollment(APIView):
    success_message = "Enrolled Successfully."
    success_response = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING, example="Success"),
            'data': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        # description=message,
                        example=success_message
                    ),
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                }
            )
        }
    )

    @swagger_auto_schema(request_body=QuizEnrolmentSerializer(), responses={200: success_response})
    def post(self, request, *args, **kwargs):
        serializer = QuizEnrolmentSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            info_logger.info('User Enrolled Successfully in a Quiz.')
            return Response({
                'status': 'Success',
                'data': {'message': self.success_message, "user_id": obj.id}
            })
        warning_logger.warning("Error occured while enroll in a quiz")
        return Response({
            'status': 'Failed',
            'data': serializer.errors
        })



