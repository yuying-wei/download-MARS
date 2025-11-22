import time
import cdsapi
from datetime import datetime, timedelta

# Initialize CDS client
c = cdsapi.Client()

# Download period and interval
start_date_str = "1995-06-11 00"
end_date_str   = "1995-06-19 21"
hour_interval  = 3

def download_data(date_str, hour_str):
    """Download ERA5 analysis data for a given date and hour."""

    start_time = time.time()
    file_name = f"{date_str}-{hour_str}.nc"

    # Retrieve surface analysis variables
    c.retrieve(
        "reanalysis-era5-complete",
        {
            "class": "ea",
            "expver": "1",
            "date": date_str,
            "time": f"{hour_str}:00:00",
            "levtype": "sfc",
            "stream": "oper",
            "type": "an",
            "param": "134",  # surface pressure
            "grid": "0.50/0.50",
            "format": "netcdf",
        },
        f"sp-{file_name}"
    )
    print(f"*** sp-{file_name} saved, time: {time.time() - start_time:.2f}s ***")


# Iterate through the date range
start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H")
end_date   = datetime.strptime(end_date_str,   "%Y-%m-%d %H")

current = start_date
while current <= end_date:
    date_str = current.strftime("%Y-%m-%d")
    hour_str = current.strftime("%H")

    download_data(date_str, hour_str)
    current += timedelta(hours=hour_interval)