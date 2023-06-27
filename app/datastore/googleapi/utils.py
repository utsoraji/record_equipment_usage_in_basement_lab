import datetime
import math

GSPREAD_MIN_DATE = datetime.datetime(1899, 12, 31)
SEC_IN_DAY = 24 * 60 * 60


def convert_to_serial_datetime(date: datetime.datetime) -> float:
    if date is None:
        return None
    delta = date - GSPREAD_MIN_DATE
    return (1 + delta.days) + (delta.seconds / SEC_IN_DAY)


def convert_from_serial_datetime(serial_date: float | int) -> datetime.datetime:
    if serial_date is None:
        return None
    if not isinstance(serial_date, (int, float)):
        print(f"Invalid data type: {type(serial_date)}")
        return None
    part_of_day, days = math.modf(serial_date)
    return GSPREAD_MIN_DATE + datetime.timedelta(
        days=days - 1, seconds=part_of_day * SEC_IN_DAY
    )


def parse_equipments(equipments: str | None) -> list[str]:
    """
    Parse a comma separated list of equipments into a list of string names or ids.

    Args:
        equipments (str | None): A string of comma-separated equipment names.

    Returns:
        list[str]: A list of stripped and non-empty strings.
    """
    if equipments is None:
        return list()
    return filter(
        lambda n: n != "", [equipment.strip() for equipment in equipments.split(",")]
    )


def parse_equipments_reservation(equipments: str | None) -> list[str]:
    """
    Parse reservation equipments data formatting as "{room} {equipment_name}".
    example: "011 複合材料切断機①(丸東製作所 AC-500CF), 013 加熱冷却自動プレス機(PEI)"

    Args:
        equipments (str | None): A string containing the names of the equipment
            separated by commas. If None, an empty list is returned.

    Returns:
        set[str]: A list of equipment names.
    """
    list_room_space_name = parse_equipments(equipments)
    names = [name[name.find(" ") + 1 :] for name in list_room_space_name]
    return names
