
from drf_yasg import openapi


# Schema for POST request where all fields are required
post_quiz_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, default='HTML QUIZ'),
        'startDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, default='24 February, 2024'),
        'endDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, default='24 February, 2024'),
        'resultDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, default='24 February, 2024'),
        'prize': openapi.Schema(type=openapi.TYPE_STRING, default='100 JCoins'),
        'duration': openapi.Schema(type=openapi.TYPE_STRING, default='10 minutes'),
        # 'totalQuestions': openapi.Schema(type=openapi.TYPE_INTEGER, default=10),
        'organization_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Organization ID", default=None),
        'order': openapi.Schema(type=openapi.TYPE_INTEGER, default=1, description="Order of the Quiz"),

    },
    required=['title', 'startDate', 'endDate', 'resultDate', 'prize', 'duration', 'order'],

)


# Schema for PUT request where only specific fields are required
put_quiz_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        'title': openapi.Schema(type=openapi.TYPE_STRING, default='HTML QUIZ'),
        'startDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, default='24 February, 2024'),
        'endDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, default='24 February, 2024'),
        'resultDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, default='24 February, 2024'),
        'prize': openapi.Schema(type=openapi.TYPE_STRING, default='100 JCoins'),
        'duration': openapi.Schema(type=openapi.TYPE_STRING, default='10 minutes'),
        # 'totalQuestions': openapi.Schema(type=openapi.TYPE_INTEGER, default=10),
        'organization_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Organization ID"),
        'order': openapi.Schema(type=openapi.TYPE_INTEGER, default=1, description="Order of the Quiz"),
        'isActive': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=True),
        'isVerified': openapi.Schema(type=openapi.TYPE_BOOLEAN, default=False),
    }
)

# get method data response schema
data_item_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        'title': openapi.Schema(type=openapi.TYPE_STRING),
        'startDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, example='24 February, 2024'),
        'endDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, example='24 February, 2024'),
        'resultDate': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE, example='24 February, 2024'),
        'prize': openapi.Schema(type=openapi.TYPE_STRING, example='100 JCoins'),
        'duration': openapi.Schema(type=openapi.TYPE_STRING, example='10 minutes'),
        'totalQuestions': openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
        'organization_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Organization ID"),
        'order': openapi.Schema(type=openapi.TYPE_INTEGER, example=1, description="Order of the Quiz"),
        'isActive': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        'isVerified': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
    }

)


get_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'count': openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
        'next': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, example="http://127.0.0.1:8000/quizApi/GETAllQuiz/?page=3&page_size=5"),
        'previous': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, example="http://127.0.0.1:8000/quizApi/GETAllQuiz/?page_size=5"),
        'data': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=data_item_schema,
        ),
    }
)






