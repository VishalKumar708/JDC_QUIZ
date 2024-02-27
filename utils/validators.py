from datetime import datetime
from django.conf import settings


def compare_dates(start_date, end_date):
    """ Check start_date is greater than or equal to end_date"""
    default_format = "%d/%m/%Y"
    dateformat = getattr(settings, 'DEFAULT_DATE_FORMAT', default_format)

    try:
        # Parse date strings into datetime objects
        start_date_obj = datetime.strptime(start_date, dateformat)
        end_date_obj = datetime.strptime(end_date, dateformat)
    except Exception as e:
        if dateformat == default_format:
            print("date should be in this format 'day/month/year[2024]'")
        elif dateformat == "%d %B, %Y":
            print("date should be in this format 'day [January... December], year[2024]'")
        else:
            print(e)
        return ValueError

    # Compare the dates
    if start_date_obj > end_date_obj or start_date_obj == end_date_obj:
        return True
    else:
        return False
