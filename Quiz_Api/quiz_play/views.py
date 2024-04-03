from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import CreateQuizPlaySerializer
from ..models import QuizEnrollment, QuizPlay, QuizQuestions

from drf_yasg.utils import swagger_auto_schema
import logging
error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')
warning_logger = logging.getLogger('warning')


class POSTQuizPlay(APIView):
    description = """
        <p>This API <strong>records</strong> user <strong>input</strong> as they <strong>play</strong> the
         <strong>quiz</strong>, <strong>storing</strong> inputs for each <strong>question</strong> as users
          <strong>progress</strong> through the <strong>quiz</strong>.</p>

    """
    success_message = "Answer submitted successfully."
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
                    # 'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                }
            )
        }
    )

    @swagger_auto_schema(
        tags=["Quiz Enrollment And Play APIs"],
        request_body=CreateQuizPlaySerializer(),
        responses={200: success_response})
    def post(self, request, *args, **kwargs):
        # print("request=> ", request.headers)
        # print("timezone==> ", request.headers.get('Timezone'))
        # print("type(request)=> ",type(request.data))
        serializer = CreateQuizPlaySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            info_logger.info('User played quiz successfully.')
            return Response({
                'status': 'Success',
                'data': {'message': self.success_message}
            })
        warning_logger.warning("Error occured while playing a quiz")
        return Response({
            'status': 'Failed',
            'data': serializer.errors
        })
