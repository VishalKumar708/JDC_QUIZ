from drf_yasg import openapi

# post_question_schema = openapi.Schema(
#     type=openapi.TYPE_OBJECT,
#     properties={
#         'quizId': openapi.Schema(type=openapi.TYPE_INTEGER, description="Required a valid 'quiz id'.", example=1),
#         'question': openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'text': openapi.Schema(type=openapi.TYPE_STRING, description="Enter the question text.", example="Can you speak English?"),
#                 'type': openapi.Schema(type=openapi.TYPE_STRING, description="Means checkbox or radio", example="radio", default=None),
#                 'level': openapi.Schema(type=openapi.TYPE_STRING, description="Means Easy, Medium, or Hard", example="Easy", default=None),
#             },
#             required=['text', 'type']
#
#         ),
#         'options': openapi.Schema(type=openapi.TYPE_ARRAY, description="Enter the options.", items = openapi.Schema(type=openapi.TYPE_STRING), example=["Yes", "No"]),
#         'correct_answer': openapi.Schema(type=openapi.TYPE_ARRAY, description="Enter the correct option(s) index value", items=openapi.Schema(type=openapi.TYPE_INTEGER), example=[0])
#     },
#     required=['quizId', 'question', 'options', 'correct_answer']
# )

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
                    'options': openapi.Schema(
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
                    "options": [
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
                name='options__isActive',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description="Boolean value indicating whether to filter based on the 'isActive' field in answers.",
                example=False,
                required=False
            ),

        ]


put_question_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'status': openapi.Schema(type=openapi.TYPE_STRING, example="Success"),
        'data': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, example="Record Updated Successfully."),
                'questionId': openapi.Schema(type=openapi.TYPE_INTEGER, example=1)
            }
        )
    }
)

put_question_requested_data_schema = [
    openapi.Parameter(
        name='questionId',
        in_=openapi.IN_PATH,
        type=openapi.TYPE_INTEGER,
        description="ID of the quiz (integer)"
    ),
]

requested_data_for_put_option_schema =[
openapi.Parameter(
                name='optionId',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="ID of the answer (integer)"
            ),
]



# Define the schema
# GETAllQuestionsByQuizIdAndUserId view
get_questions_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'status': openapi.Schema(type=openapi.TYPE_STRING, example="Success"),
        'data': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'correct_answers': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                'incorrect_answers': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                'unattempted_questions': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'question': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=23),
                                    'text': openapi.Schema(type=openapi.TYPE_STRING, example="Six summer available according health conference model. Alone item smile current activity."),
                                    'type': openapi.Schema(type=openapi.TYPE_STRING, example="Checkbox"),
                                    'isActive': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                    'level': openapi.Schema(type=openapi.TYPE_STRING, example="Easy"),
                                },
                            ),
                            'options': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=77),
                                        'option': openapi.Schema(type=openapi.TYPE_STRING, example="Justin Flores"),
                                        'correctOption': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                        'isActive': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                    },
                                ),
                            ),
                            'correct_answer': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_INTEGER, example=[77, 78]),
                            ),
                            'selected_option': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_INTEGER),
                            ),
                        },
                    ),
                ),
                'attempted_questions': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'question': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=21),
                                    'text': openapi.Schema(type=openapi.TYPE_STRING, example="Movie care prove beat.\nShare industry approach nature. Close once prove view though spring. Perhaps almost least according third hotel. Artist cup we window shake."),
                                    'type': openapi.Schema(type=openapi.TYPE_STRING, example="Radio"),
                                    'isActive': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                    'level': openapi.Schema(type=openapi.TYPE_STRING, example="Easy"),
                                },
                            ),
                            'options': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=72),
                                        'option': openapi.Schema(type=openapi.TYPE_STRING, example="Nicholas Garza"),
                                        'correctOption': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                        'isActive': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                    },
                                ),
                            ),
                            'correct_answer': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_INTEGER, example=[72]),
                            ),
                            'selected_option': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_INTEGER, example=[72]),
                            ),
                        },
                    ),
                ),
            },
        ),
    },
    example={
        'status': "Success",
        'data': {
            'correct_answers': 1,
            'incorrect_answers': 1,
            'unattempted_questions': [
                {
                    'question': {
                        'id': 23,
                        'text': "Six summer available according health conference model. Alone item smile current activity.",
                        'type': "Checkbox",
                        'isActive': True,
                        'level': "Easy",
                    },
                    'options': [
                        {
                            'id': 77,
                            'option': "Justin Flores",
                            'correctOption': True,
                            'isActive': True,
                        },
                        {
                            'id': 78,
                            'option': "George Fuentes",
                            'correctOption': True,
                            'isActive': True,
                        }
                    ],
                    'correct_answer': [77, 78],
                    'selected_option': []
                }
            ],
            'attempted_questions': [
                {
                    'question': {
                        'id': 21,
                        'text': "Movie care prove beat.\nShare industry approach nature. Close once prove view though spring. Perhaps almost least according third hotel. Artist cup we window shake.",
                        'type': "Radio",
                        'isActive': True,
                        'level': "Easy",
                    },
                    'options': [
                        {
                            'id': 72,
                            'option': "Nicholas Garza",
                            'correctOption': True,
                            'isActive': True,
                        },
                        {
                            'id': 73,
                            'option': "Victoria Hicks",
                            'correctOption': False,
                            'isActive': True,
                        }
                    ],
                    'correct_answer': [72],
                    'selected_option': [72]
                }
            ]
        }
    }
)
