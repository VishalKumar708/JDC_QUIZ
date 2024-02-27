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