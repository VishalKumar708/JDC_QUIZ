
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q, Case, When, Value, CharField
from drf_yasg.utils import swagger_auto_schema
from .schemas import *
from ..models import QuizQuestions, QuizOptions, QuizPlay, QuizEnrollment
from .serializers.get import GETAllQuizQuestionsSerializer, GETAllQuizQuestionsByQuizIdAndUserIdSerializer
from .serializers.create import CreateQuestionSerializer, CREATEOptionSerializer
from .serializers.update import UPDATEQuestionSerializer, UPDATEOptionSerializer

from django.db.models import Prefetch, Subquery, OuterRef, Exists, F
from django.db.models import Aggregate

from utils.utils import convert_str_to_bool
import logging
error_logger = logging.getLogger('error')
info_logger = logging.getLogger('info')
warning_logger = logging.getLogger('warning')


class POSTQuestions(APIView):
    description = """
    <p>This API facilitates the creation of questions individually, enabling the specification of options and correct answers. Questions can be of two types:</p>
    <ul>
        <li><strong>Radio type:</strong> Users can select only one correct option.</li>
        <li><strong>Checkbox type:</strong> Users can select <strong>at least two or more correct options</strong>.</li>
    </ul>
    <p><strong>Important Points:</strong></p>
    <ul>
        <li><p>It is mandatory for users to provide a minimum of <strong>two options</strong> for each question.</p></li>
        <li><p>You cannot add more questions within a quiz if the <strong>quiz's start date or end date is earlier than or the same as today's date</strong>.</p></li>
    </ul>
    """
    message = "Record Added Successfully."
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
                        example=message
                    ),
                    'question_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                }
            )
        }
    )

    @swagger_auto_schema(tags=['Question APIs'], request_body=CreateQuestionSerializer(), responses={200: success_response})
    def post(self, request, *args, **kwargs):
        print('question method call....')
        serializer = CreateQuestionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            info_logger.info("Question and options are added successfully.")
            return Response(data={
                'status': 'Success',
                'data': {"message": self.message, "question_id": data.id}
            })
        warning_logger.warning("Error occured while creating questions.")
        return Response(data={
            'status': 'Failed',
            'data': serializer.errors
        }, status=400)


class GETAllQuestionsByQuizId(APIView):
    description ="""
        <p>This API returns all questions associated with the provided quiz ID.<br><br>
         Users have the ability to filter records based on the status of questions (<strong>active</strong>/<strong>inactive</strong>) and 
         the status of options within questions (<strong>active</strong>/<strong>inactive</strong>).<br><br>
         This API is intended for administrative purposes to enable the viewing of all records.</p>
    """

    def filter_queryset(self, request, quizId):
        options_isActive = request.GET.get('options__isActive')
        questions_isActive = request.GET.get('questions__isActive')
        try:
            options_isActive = convert_str_to_bool(options_isActive)
        except Exception:
            error_logger.error(f'str(e)')
            options_isActive =None

        try:
            questions_isActive = convert_str_to_bool(questions_isActive)
        except Exception as e:
            error_logger.error(f'str(e)')
            questions_isActive = None
        if options_isActive is not None and questions_isActive is not None:
            return (QuizQuestions.objects.select_related('quiz_id').filter(quiz_id=quizId, isActive=questions_isActive)
            .prefetch_related(
                Prefetch('options', queryset=QuizOptions.objects.filter(isActive=options_isActive).order_by('order'))
            ))
        elif options_isActive is not None:
            return QuizQuestions.objects.select_related('quiz_id').filter(quiz_id=quizId).prefetch_related(
                Prefetch('options', queryset=QuizOptions.objects.filter(isActive=options_isActive).order_by('order'))
            )
        elif questions_isActive is not None:
            return QuizQuestions.objects.filter(quiz_id=quizId, isActive=questions_isActive).prefetch_related(
                Prefetch('options', queryset=QuizOptions.objects.all().order_by('order'))
            )
        else:
            return QuizQuestions.objects.filter(quiz_id=quizId).prefetch_related(
                Prefetch('options', queryset=QuizOptions.objects.all().order_by('order'))
            )

    @swagger_auto_schema(tags=['Question APIs'], manual_parameters=requested_data_for_question_schema, responses={200: get_question_response_schema})
    def get(self, request, quizId, *args, **kwargs):
        try:
            filter_queryset = self.filter_queryset(request=request, quizId=quizId)

            if len(filter_queryset) < 1:
                info_logger.info("Not any question added yet inside this quiz.")
                return Response(
                    data={
                        'status': 'Success',
                        'data': {'message': "No Record Found."}
                    },
                    status=200
                )

            serializer = GETAllQuizQuestionsSerializer(filter_queryset, many=True)

            info_logger.info("Return all questions with option Successfully.")
            return Response(data={
                'status': 'Success',
                'data': serializer.data
            }, status=200)
        except ValueError:
            warning_logger.warning("Quiz Id type error.")
            return Response(data={
                'status': 'Failed',
                'data': {"message": f"Excepted a number but got '{quizId}'"}
            }, status=404)


class PUTQuestionById(APIView):
    description = """
        <p>This API facilitates the updating of questions based on the provided question ID. <br><br>
        Users can also toggle the status of a question between <strong>active</strong> and <strong>inactive</strong>
         by specifying a value in the <strong>isActive</strong> field, along with updating other fields.</p>
        <p><strong>Important Points:</strong></p> 
        <ul>
            <li><p>You cannot update any question details of a quiz if the <strong>quiz's start date or end date is earlier than or the same as today's date</strong>.</p></li>
        </ul>
    """

    @swagger_auto_schema(tags=['Question APIs'], request_body=UPDATEQuestionSerializer,
                         responses={200: put_question_response_schema}, manual_parameters=put_question_requested_data_schema)
    def put(self, request, questionId, *args, **kwargs):
        try:
            instance = QuizQuestions.objects.get(id=questionId)
            serializer = UPDATEQuestionSerializer(instance=instance, data=request.data, partial=True, context={"quiz_id": instance.quiz_id, "question_id":questionId, "question_instance":instance})
            if serializer.is_valid():
                obj = serializer.save()
                info_logger.info("Question update successfully.")
                return Response(data={
                    'status': 'Success',
                    'data': {'message': f'Record Updated Successfully.', 'questionId': obj.id}
                }, status=200)
            warning_logger.warning("Some Error occured while updating Quiz Question.")
            return Response(data={
                'status': 'Failed',
                'data': serializer.errors
            }, status=400)
        except QuizQuestions.DoesNotExist:
            warning_logger.warning("Received Invalid QuestionId.")
            return Response(data={
                'status': 'Failed',
                'data': {"message": f"Invalid questionId."}
            }, status=404)
        except ValueError:
            warning_logger.warning("Received QuestionId has value error.")
            return Response(data={
                'status': 'Failed',
                'data': {"message": f"Excepted a number but got '{questionId}'."}
            }, status=404)


class PUTOption(APIView):
    description = """
        <p>This API facilitates the updating of option text and other associated fields by specifying the option ID. <br><br>
        Users can also adjust the order of options within a question and toggle the <strong>active/inactive</strong>
         status of existing options within the question.</p>
        <p><strong>Important Points:</strong></p> 
        <ul>
            <li><p>You cannot add more options within a question if the <strong>quiz's start date or end date is earlier than or the same as today's date</strong>.</p></li>
        </ul>
    """

    @swagger_auto_schema(tags=['Question APIs'], request_body=UPDATEOptionSerializer,
                         responses={200: put_question_response_schema},
                         manual_parameters=requested_data_for_put_option_schema)
    def put(self, request, optionId, *args, **kwargs):
        try:
            instance = QuizOptions.objects.get(id=optionId)
            serializer = UPDATEOptionSerializer(instance=instance, data=request.data, partial=True,
                                                context={'question_id': instance.question_id, 'answer_id': optionId})

            if serializer.is_valid():
                serializer.save()
                info_logger.info("Option Updated Successfully.")
                return Response(data={
                    'status': 'Success',
                    'data': {'message': f'Record Updated Successfully.'}
                }, status=200)
            warning_logger.warning("While updating option some error occured.")
            return Response(data={
                'status': 'Failed',
                'data': serializer.errors
            }, status=400)
        except QuizOptions.DoesNotExist:
            warning_logger.warning("Received Invalid OptionId.")
            return Response(data={
                'status': 'Failed',
                'data': {"message": f"Invalid answerId."}
            }, status=404)
        except ValueError:
            warning_logger.warning("Received OptionId has value error.")
            return Response(data={
                'status': 'Failed',
                'data': {"message": f"Excepted a number but got '{optionId}'."}
            }, status=404)


class POSTOption(APIView):
    description = """
        <p>This API assists in adding new options within a question by specifying the required fields.</p>
        <p><strong>Important Points:</strong></p> 
        <ul>
            <li><p>You cannot update option details of a question if the <strong>quiz's start date or end date is earlier than or the same as today's date</strong>.</p></li>
        </ul>
    """
    message = 'Record Added Successfully.'
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
                        example=message
                    ),
                    'option_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=78),
                }
            )
        }
    )
    @swagger_auto_schema(tags=['Question APIs'], request_body=CREATEOptionSerializer, responses={200: success_response})
    def post(self, request, *args, **kwargs):
        serializer = CREATEOptionSerializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.save()
            info_logger.info("New Option Added Successfully.")
            return Response(data={
                'status': 'Success',
                'data': {'message': self.message, "option_id":instance.id}
            }, status=200)
        warning_logger.warning("While adding new option some error occured.")
        return Response(data={
            'status': 'Failed',
            'data': serializer.errors
        }, status=400)


class GETAllQuestionsByUserIdAndQuizId(APIView):
    description = """
        <p>This API selectively displays <strong>active</strong> questions and sorts options based on the '<strong>order</strong>' field.<br> 
        All the options of a questions will come in sorted order. <br><br>
         It returns both <strong>attempted</strong> and <strong>unattempted</strong> questions associated with a specific '<strong>userId</strong>'.<br>
         <strong>Unattempted</strong> questions will always come in random order.<br><br>
    """

    # def filter_queryset(self, request, quizId):
    #     queryset = QuizQuestions.objects.select_related('quiz_id').prefetch_related(
    #             Prefetch('options', queryset=QuizOptions.objects.filter(isActive=True).order_by('order'))
    #         ).filter(quiz_id=quizId, isActive=True)
    #
    #     return queryset
    def filter_queryset(self, request, quizId, userId):
        queryset = QuizQuestions.objects.filter(
            quiz_id=quizId,
            isActive=True
        ).prefetch_related(
            Prefetch(
                'options',
                queryset=QuizOptions.objects.filter(isActive=True).order_by('order')
            ),
            # Prefetch(
            #     'quiz_plays',
            #     queryset=QuizPlay.objects.filter(userId=userId).values_list('answerId__id', flat=True),
            #     to_attr='user_answers_id'
            # )
        )
        return queryset

    @swagger_auto_schema(tags=['Question APIs'], description=description,responses={200: get_questions_response_schema})
    def get(self, request, quizId, userId, *args, **kwargs):
        # try:
            print("method is calling..")
            quiz_result = QuizEnrollment.objects.filter(quiz_id=quizId, user_id=userId).first()
            print('quiz_result=> ', quiz_result)
            # if user has overed this quiz already
            if quiz_result and quiz_result.status == 'complete':
                return Response(
                    data={
                        'status': 'Failed',
                        'data': {'message': "You have finished this quiz."}
                    },
                    status=400
                )

            questions_queryset = self.filter_queryset(request=request, quizId=quizId, userId=userId)
            # print("questions_queryset==> ", questions_queryset)
            if not questions_queryset.exists():
                info_logger.info("Not any question added yet inside this quiz.")
                return Response(
                    data={
                        'status': 'Success',
                        'data': {'message': "No Record Found."}
                    },
                    status=200
                )

            # get all attempted questionsId
            attempted_questions_queryset = QuizPlay.objects.filter(userId=userId, quizId=quizId).values_list('questionId', flat=True)
            if attempted_questions_queryset:
                unattempted_queryset = questions_queryset.exclude(id__in=attempted_questions_queryset).order_by('?')
                # print('explanation=> ', unattempted_queryset.explain())
                attempted_queryset = questions_queryset.exclude(~Q(id__in=attempted_questions_queryset))
                # print("queryset order==> ", attempted_queryset.query)
                # print("attempted_queryset order==> ", attempted_queryset.query)

                attempted_questions_serializer = GETAllQuizQuestionsByQuizIdAndUserIdSerializer(attempted_queryset, many=True,
                                                                            context={'user_id': userId,
                                                                                     'quiz_id': quizId})
                unattempted_questions_serializer = GETAllQuizQuestionsByQuizIdAndUserIdSerializer(unattempted_queryset, many=True,
                                                                            context={'user_id': userId,
                                                                                     'quiz_id': quizId})
                return Response(data={
                    'status': 'Success',
                    'data': {
                        'correct_answers': quiz_result.correctAnswer,
                        'incorrect_answers': quiz_result.incorrectAnswer,
                        'unattempted_questions': unattempted_questions_serializer.data,
                        'attempted_questions': attempted_questions_serializer.data,
                    }
                }, status=200)

            # print('queryset123==> ', questions_queryset)
            serializer = GETAllQuizQuestionsByQuizIdAndUserIdSerializer(questions_queryset, many=True, context={'user_id':userId, 'quiz_id': quizId})

            info_logger.info("Return all questions with option Successfully.")
            return Response(data={
                'status': 'Success',
                'data': {
                    'correct_answers': 0 if quiz_result is None else quiz_result.correctAnswer,
                    'incorrect_answers': 0 if quiz_result is None else quiz_result.incorrectAnswer,
                    'unattempted_questions': serializer.data,
                    'attempted_questions': []
                }
            }, status=200)
        # except ValueError:
        #     warning_logger.warning("Quiz Id type error.")
        #     return Response(data={
        #         'status': 'Failed',
        #         'data': {"message": f"Excepted a number but got '{quizId}'"}
        #     }, status=404)
