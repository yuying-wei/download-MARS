import time
import cdsapi
from datetime import datetime, timedelta

# Initialize CDS API client
c = cdsapi.Client()

# Download period and interval
start_date_str = "2021-06-13 00"
end_date_str   = "2021-06-30 21"
hour_interval  = 3

def download_data(date_str, hour_str, step_str, init_date, init_hour):
    """Download ERA5 hourly surface forecast fields for a given target time."""

    start_time = time.time()
    file_name = f"{date_str}-{hour_str}.nc"

    # Retrieve surface forecast variables
    c.retrieve(
        "reanalysis-era5-complete",
        {
            "class":  "ea",
            "expver": "1",
            "stream": "oper",
            "type":   "fc",
            "levtype": "sfc",
            "date":   init_date,
            "time":   f"{init_hour}:00:00",
            "step":   step_str,
            "param":"235033", #mean_surface_sensible_heat_flux
            "grid": "0.50/0.50",
            "format": "netcdf",
        },
        f"msshf-{file_name}"
    )

    elapsed = time.time() - start_time
    print(f"*** {file_name} saved successfully, time: {elapsed:.3f}s / {elapsed/60:.3f} mins ***")


# Convert to datetime objects
start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H")
end_date   = datetime.strptime(end_date_str, "%Y-%m-%d %H")

current_time = start_date

# Loop through all target times
while current_time <= end_date:

    date_str = current_time.strftime("%Y-%m-%d")
    hour_str = current_time.strftime("%H")
    hour = current_time.hour

    # -------------------------------
    # Determine the correct forecast cycle
    # ERA5 cycles: 06, 18
    # -------------------------------
    if 6 <= hour <= 17:
        init_time = current_time.replace(hour=6)
        init_hour_str = "06"
    elif 18 <= hour <= 23:
        init_time = current_time.replace(hour=18)
        init_hour_str = "18"
    else:  # 00–05 → use previous day's 18 UTC cycle
        prev_day = current_time - timedelta(days=1)
        init_time = prev_day.replace(hour=18)
        init_hour_str = "18"

    init_date_str = init_time.strftime("%Y-%m-%d")

    step = int((current_time - init_time).total_seconds() // 3600)
    step_str = str(step)

    download_data(date_str, hour_str, step_str, init_date_str, init_hour_str)
    current_time += timedelta(hours=hour_interval)