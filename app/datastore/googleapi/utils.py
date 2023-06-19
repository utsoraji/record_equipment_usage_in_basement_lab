import datetime
import math

GSPREAD_MIN_DATE = datetime.datetime(1899, 12, 31)
SEC_IN_DAY = 24 * 60 * 60


def convert_to_serial_datetime(date: datetime.datetime) -> float:
    delta = date - GSPREAD_MIN_DATE
    return (1 + delta.days) + (delta.seconds / SEC_IN_DAY)


def convert_from_serial_datetime(serial_date: float) -> datetime.datetime:
    part_of_day, days = math.modf(serial_date)
    return GSPREAD_MIN_DATE + datetime.timedelta(
        days=days - 1, seconds=part_of_day * SEC_IN_DAY
    )
