from datetime import datetime

from starlette.exceptions import HTTPException

from controller.tmr_controller import find_all_tmrs

from datetime import datetime, timedelta, date


async def tmrs_completed_service(facility_id: str = ""):
    try:
        tmrs = await find_all_tmrs(facility_id)

        # Get the current month and the first day of the current month
        current_month = datetime.now().month

        # Filter records for the current month and the previous month
        current_month_records = list(filter(lambda tmr: tmr['add'] and tmr['add'].month == current_month, tmrs))
        last_month_records = list(filter(lambda tmr: tmr['add'] and tmr['add'].month == current_month - 1, tmrs))

        current_month_completed = len(current_month_records)
        last_month_completed = len(last_month_records)

        delta = ((current_month_completed - last_month_completed) / last_month_completed) * 100
        return current_month_completed, delta

    except HTTPException as http_exception:
        raise http_exception


async def tmrs_received_service(facility_id: str = ""):
    try:
        tmrs = await find_all_tmrs(facility_id)

        # Get the current month and the first day of the current month
        current_month = datetime.now().month

        # Filter records for the current month and the previous month
        current_month_records = list(filter(lambda tmr: tmr['date_received'] and tmr['date_received'].month == current_month, tmrs))
        last_month_records = list(filter(lambda tmr: tmr['date_received'] and tmr['date_received'].month == current_month - 1, tmrs))

        current_month_received = len(current_month_records)
        last_month_received = len(last_month_records)

        delta = ((current_month_received - last_month_received) / last_month_received) * 100
        return current_month_received, delta

    except HTTPException as http_exception:
        raise http_exception
