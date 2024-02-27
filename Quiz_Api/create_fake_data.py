from .models import Quiz
from datetime import datetime
import time

start_time = time.time()
total_records = 10000
# Create 1000 Quiz objects
for i in range(total_records):
    Quiz.objects.create(
        tittle=f'Quiz {i+1}',
        startDate=datetime.now(),
        endDate=datetime.now(),
        resultDate=datetime.now(),
        prize=f'Prize {i+1}',
        duration='30 minutes',
        totalQuestions=10,
        order=i+1,
        isVerified=True
    )

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Time taken to create {total_records} records: {elapsed_time} seconds")

