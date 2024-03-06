from django.db import transaction

from ..models import QuizQuestions, QuizOptions, Quiz
from datetime import datetime
import time
import faker
import random
fake = faker.Faker()


def create_question_and_options():
    number_of_question = None
    start_time = time.time()
    with (transaction.atomic()):
        try:
            quiz_title = input("Enter the quiz title: ")
            number_of_question = input("Enter int value to generate no. of question: ")
            option_type = input("""
            select the quiz questions option type:
            1. Radio type only
            2. both checkbox and radio
            """)
            try:
                number_of_question = int(number_of_question)
                option_type = int(option_type)
                if option_type not in [1, 2]:
                    return "please enter either 1 or 2."

            except ValueError:
                return "Please enter only integer value."

            print("Please wait....")

            quiz_id = Quiz.objects.create(
                title=quiz_title,
                startDate=datetime.now(),
                endDate=datetime.now(),
                resultDate=datetime.now(),
                prize=f'Prize',
                duration='30 minutes',
                totalQuestions=10,
                order=random.randint(1, 59),
                isVerified=True
            )

            for i in range(number_of_question):
                question_instance = QuizQuestions.objects.create(
                    quiz_id=quiz_id,
                    question=fake.text(),
                    type="Checkbox",
                    level="Easy"
                )
                no_of_options = random.randint(2, 5)
                print("no of options==> ", no_of_options)
                if option_type == 2:
                    options_list = [QuizOptions(question_id=question_instance, option=fake.name, correctOption=True if i==0 else random.choice([True, False]))
                                            for i in range(no_of_options)]
                elif option_type == 1:
                    random_correct_option = random.randint(0, no_of_options-1)
                    print("random_correct_option==> ", random_correct_option)
                    options_list = [QuizOptions(question_id=question_instance, option=fake.name,
                                                correctOption=True if i == random_correct_option else False)
                                    for i in range(no_of_options)]
                # for i in range(2, no_of_options):
                #     option = {
                #         "question_id": question_instance,
                #         "option": fake.text(),
                #         "correctOption": random.choice([True, False])
                #     }
                #     options_list.append(option)

                options_instance = QuizOptions.objects.bulk_create(options_list)
                no_of_correctOptions = question_instance.options.filter(correctOption=True).count()
                print("no_of_correctOptions=> ", no_of_correctOptions)
                if no_of_correctOptions > 1:
                    question_instance.type = 'Checkbox'
                elif no_of_correctOptions == 1:
                    question_instance.type = 'Radio'
                question_instance.save()

            end_time = time.time()
            total_time = end_time - start_time

            return f"{number_of_question} created successfully inside '{quiz_title}' quiz and its 'quiz_id'= {quiz_id.id} and total time taken=>{total_time} "
        except Exception as e:
            transaction.set_rollback(True)
            print("Exception:==> ", str(e))


    # return f"Time taken to create {number_of_question} questions in a quiz: {total_time} seconds"
    return None
