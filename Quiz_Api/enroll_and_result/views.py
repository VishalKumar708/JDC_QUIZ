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

    @swagger_auto_schema(request_body=QuizEnrolmentSerializer())
    def post(self, request, *args, **kwargs):
        serializer = QuizEnrolmentSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            return Response({
                'status': 'Success',
                'data': {'message': "Record Added Successfully.", "quizEnrolId": obj.id}
            })
        return Response({
            'status': 'Failed',
            'data': serializer.errors
        })



