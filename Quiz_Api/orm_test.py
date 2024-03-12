from .models import *
from django.db.models import Count
value = input("enter the value of isActive: ")
filtered_data = Quiz.objects.annotate(
    total_questions=Count('quiz_questions__id')
)
all_quiz_question_count = [i.total_questions for i in filtered_data]
print("questions count before filtering ==> ", all_quiz_question_count)
if value is not None:
    filtered_data2 = filtered_data.filter(quiz_questions__isActive=bool(value))
    print(filtered_data[1].total_questions)
    question_count = [i.total_questions for i in filtered_data2]
    print(f"question count after filtering {value}=> ", filtered_data2)

# filtered_data3 = filtered_data.filter(quiz_questions__isActive=False)
# question_counts = [i.total_questions for i in filtered_data3]
# print("question count after filtering False=> ", filtered_data3)
