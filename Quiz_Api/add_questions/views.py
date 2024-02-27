
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import CreateQuestionSerializer
from drf_yasg.utils import swagger_auto_schema
from .schemas import *


class POSTQuestions(APIView):
    message = "Record Added Successfully."
    success_response = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'data': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        # description=message,
                        example=message
                    ),
                    'question_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                }
            )
        }
    )

    @swagger_auto_schema(tags=['Question API'], request_body=post_question_schema, responses={200: success_response})
    def post(self, request, *args, **kwargs):
        serializer = CreateQuestionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            # print('data==> ', data)
            return Response(data={
                'status': 'Success',
                'data': {"message": self.message, "question_id": data.id}
            })
        return Response(data={
            'status': 'Failed',
            'data': serializer.errors
        }, status=400)

