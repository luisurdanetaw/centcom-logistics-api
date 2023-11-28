from datetime import datetime

from starlette.exceptions import HTTPException

from controller.tmr_controller import find_all_tmrs

from datetime import datetime, timedelta, date

from repository.tmr_repository import find_all_tmrs_by_country


async def tmrs_completed_service(country: str = ""):
    try:
        tmrs = await find_all_tmrs_by_country(country)

        # Get the current month and the first day of the current month
        current_month = datetime.now().month

        # Filter records for the current month and the previous month
        current_month_records = list(filter(lambda tmr: tmr['add'] and tmr['add'].month == current_month, tmrs))
        last_month_records = list(filter(lambda tmr: tmr['add'] and tmr['add'].month == current_month - 1, tmrs))

        current_month_completed = len(current_month_records)
        last_month_completed = len(last_month_records)

        change_percentage = ((current_month_completed - last_month_completed) / last_month_completed) * 100
        delta = current_month_completed - last_month_completed
        return current_month_completed, round(change_percentage, 2), delta

    except HTTPException as http_exception:
        raise http_exception


async def tmrs_received_service(country: str = ""):
    try:
        tmrs = await find_all_tmrs_by_country(country)

        # Get the current month and the first day of the current month
        current_month = datetime.now().month

        # Filter records for the current month and the previous month
        current_month_records = list(filter(lambda tmr: tmr['date_received'] and tmr['date_received'].month == current_month, tmrs))
        last_month_records = list(filter(lambda tmr: tmr['date_received'] and tmr['date_received'].month == current_month - 1, tmrs))

        current_month_received = len(current_month_records)
        last_month_received = len(last_month_records)



        print(current_month_received)
        change_percentage = ((current_month_received - last_month_received) // last_month_received) * 100 if last_month_received != 0 else 0

        delta = current_month_received - last_month_received
        return current_month_received, round(change_percentage, 2), delta

    except HTTPException as http_exception:
        print(http_exception.detail)
        raise http_exception


async def shipment_speed_service(country: str = ""):
    try:
        tmrs = await find_all_tmrs_by_country(country)

        # Get the current month and the first day of the current month
        current_month = datetime.now().month

        # Filter records for the current month and the previous month
        current_month_records = list(filter(lambda tmr: tmr['date_received'] and tmr['add'] and tmr['add'].month == current_month, tmrs))
        last_month_records = list(filter(lambda tmr: tmr['date_received'] and tmr['add'] and tmr['add'].month == current_month - 1, tmrs))

        # Calculate shipment speed in days for the current month
        current_month_speeds = []
        for tmr in current_month_records:
            speed_days = (tmr['add'] - tmr['date_received']).days
            current_month_speeds.append(speed_days)

        # Calculate average shipment speed for the current month
        average_speed_current_month = sum(current_month_speeds) / len(
            current_month_speeds) if current_month_speeds else 0

        # Calculate average shipment speed for the previous month
        last_month_speeds = []
        for tmr in last_month_records:
            if tmr['add'] and tmr['date_received']:
                speed_days = (tmr['add'] - tmr['date_received']).days
                last_month_speeds.append(speed_days)

        average_speed_last_month = sum(last_month_speeds) / len(last_month_speeds) if last_month_speeds else 0

        # Calculate change compared to the previous month
        change_percentage = ((average_speed_current_month - average_speed_last_month) / average_speed_last_month) * 100 if average_speed_last_month != 0 else 0
        delta = average_speed_current_month - average_speed_last_month

        return round(average_speed_current_month, 2), round(change_percentage, 2), delta

    except HTTPException as http_exception:
        raise http_exception


async def delayed_shipments_service(country: str = ""):
    try:
        tmrs = await find_all_tmrs_by_country(country)

        # Get the current month and the first day of the current month
        current_month = datetime.now().month

        # Filter records for the current month and the previous month
        current_month_records = list(filter(lambda tmr: tmr['rdd'] and tmr['add'] and tmr['add'].month == current_month, tmrs))
        last_month_records = list(filter(lambda tmr: tmr['rdd'] and tmr['add'] and tmr['add'].month == current_month - 1, tmrs))

        current_month_delayed = len(list(filter(lambda tmr: tmr['rdd'] - tmr['add'] < timedelta(days=0), current_month_records)))
        last_month_delayed = len(list(filter(lambda tmr: tmr['rdd'] - tmr['add'] < timedelta(days=0), last_month_records)))

        change_percentage = ((current_month_delayed - last_month_delayed) // last_month_delayed) * 100
        delta = current_month_delayed - last_month_delayed
        return current_month_delayed, round(change_percentage, 2), delta

    except HTTPException as http_exception:
        raise http_exception