from datetime import datetime

from starlette.exceptions import HTTPException

from repository.trends_repository import tmrs_completed_repository

from datetime import datetime, timedelta, date


async def tmrs_completed_service(facility_id: str = ""):
    try:
        tmrs = await tmrs_completed_repository(facility_id)

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

