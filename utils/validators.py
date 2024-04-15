# from datetime import datetime, date
# from django.conf import settings
#
#
# def compare_dates(start_date, end_date=None):
#     """ Check start_date is greater than or equal to end_date.
#     if you don't pass end_date then it will assume it today's date."""
#
#     default_format = "%d/%m/%Y"
#     dateformat = getattr(settings, 'DEFAULT_DATE_FORMAT', default_format)
#     print("date format==> ", dateformat)
#     # Get today's date
#     today = date.today()
#     try:
#         # Parse date strings into datetime objects
#         start_date_obj = datetime.strptime(start_date, dateformat)
#
#         end_date_obj = datetime.strptime(end_date, dateformat) if end_date else date.strptime(dateformat)
#     except Exception as e:
#         if dateformat == default_format:
#             print("date should be in this format 'day/month/year[2024]'")
#         elif dateformat == "%d %B, %Y":
#             print("date should be in this format 'day [January... December], year[2024]'")
#
#         # print(e)
#         raise ValueError
#
#     # Compare the dates
#     if start_date_obj >= end_date_obj:
#         # print("True")
#         return True
#     else:
#         # print("False")
#         return False


from datetime import datetime
from django.conf import settings


def is_startDate_greater_than_or_equal_to_endDate(start_date, end_date):
    """ Check if start_date is greater than or equal to end_date."""

    default_format = "%d/%m/%Y"
    dateformat = getattr(settings, 'DEFAULT_DATE_FORMAT', default_format)

    try:
        # Parse date strings into datetime objects
        start_date_obj = datetime.strptime(start_date, dateformat)

        end_date_obj = datetime.strptime(end_date, dateformat)

    except ValueError:
        if dateformat == default_format:
            print("Date should be in the format 'day/month/year[2024]'")
        elif dateformat == "%d %B, %Y":
            print("Date should be in the format 'day [January... December], year[2024]'")
        raise ValueError("Invalid dateformat.")  # Re-raise the exception to propagate it further if needed

    # Compare the dates
    # print("start-date_obje=> ", start_date_obj)
    # print("end-date_obje=> ", end_date_obj)
    return start_date_obj >= end_date_obj


def is_given_date_greater_than_or_equal_to_today(given_date):
    """Check if the given date is less than or equal to today's date."""
    default_format = "%d/%m/%Y"  # Define the default date format
    dateformat = getattr(settings, 'DEFAULT_DATE_FORMAT', default_format)
    try:
        # Parse the given date string into a datetime object
        given_date_obj = datetime.strptime(given_date, dateformat)
    except ValueError:
        if dateformat == default_format:
            print("Date should be in the format 'day/month/year[2024]'")
        elif dateformat == "%d %B, %Y":
            print("Date should be in the format 'day [January... December], year[2024]'")
        raise ValueError("Invalid dateformat.")

    # Get today's date
    today_date_obj = datetime.today()

    # Compare the given date with today's date
    return given_date_obj >= today_date_obj


