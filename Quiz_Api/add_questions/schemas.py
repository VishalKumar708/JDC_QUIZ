from drf_yasg import openapi

post_question_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'quizId': openapi.Schema(type=openapi.TYPE_INTEGER, description="Required a valid 'quiz id'.", example=1),
        'question': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'text': openapi.Schema(type=openapi.TYPE_STRING, description="Enter the question text.", example="Can you speak English?"),
                'type': openapi.Schema(type=openapi.TYPE_STRING, description="Means checkbox or radio", example="checkbox", default=None),
                'level': openapi.Schema(type=openapi.TYPE_STRING, description="Means Easy, Medium, or Hard", example="Easy", default=None),
            },
            required=['text', 'type']

        ),
        'options': openapi.Schema(type=openapi.TYPE_ARRAY, description="Enter the options.", items = openapi.Schema(type=openapi.TYPE_STRING), example=["Yes", "No"]),
        'correct_answer': openapi.Schema(type=openapi.TYPE_ARRAY, description="Enter the correct option(s) index value", items=openapi.Schema(type=openapi.TYPE_INTEGER), example=[0])
    },
    required=['quizId', 'question', 'options', 'correct_answer']
)

get_question_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'status': openapi.Schema(type=openapi.TYPE_STRING, example="Success"),
        'data': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'question': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=12),
                            'text': openapi.Schema(type=openapi.TYPE_STRING, example="this is my question"),
                            'type': openapi.Schema(type=openapi.TYPE_STRING, example="checkbox"),
                            'isActive': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                            'level': openapi.Schema(type=openapi.TYPE_STRING, example="Easy"),
                        },
                    ),
                    'answers': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=23),
                                'option': openapi.Schema(type=openapi.TYPE_STRING, example="Yes"),
                                'correctOption': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                'isActive': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                            },
                        ),
                        example=[
                            {
                                "id": 23,
                                "option": "Yes",
                                "correctOption": True,
                                "isActive": False
                            },
                            {
                                "id": 24,
                                "option": "No",
                                "correctOption": False,
                                "isActive": False
                            }
                        ]
                    ),
                },
            ),
            example=[
                {
                    "question": {
                        "id": 12,
                        "text": "this is my question",
                        "type": "checkbox",
                        "isActive": True,
                        "level": "Easy"
                    },
                    "answers": [
                        {
                            "id": 23,
                            "option": "Yes",
                            "correctOption": True,
                            "isActive": False
                        },
                        {
                            "id": 24,
                            "option": "No",
                            "correctOption": False,
                            "isActive": False
                        }
                    ]
                }
            ]
        ),
    },
)


requested_data_for_question_schema = [
            openapi.Parameter(
                name='quizId',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="ID of the quiz (integer)"
            ),
            openapi.Parameter(
                name='questions__isActive',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description="Boolean value indicating whether to filter based on the 'isActive' field in answers.",
                example=True,
                required=False
            ),
            openapi.Parameter(
                name='answers__isActive',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description="Boolean value indicating whether to filter based on the 'isActive' field in answers.",
                example=False,
                required=False
            ),

        ]