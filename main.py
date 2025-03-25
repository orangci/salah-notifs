import time
import json
import urllib.request
from datetime import datetime, timedelta
import subprocess
import os

city, country = "Riyadh", "Saudi+Arabia"
icon_path = f"{subprocess.check_output(['pwd']).decode('utf-8').strip()}/icon.png"
# subprocess.run([ "notify-send", "notify-salawāt", "Test", "-i", icon_path, "-a", "notify-salawat"])


def get_prayer_times():
    current_date = datetime.now().strftime("%d-%m-%Y")
    api_url = f"https://api.aladhan.com/v1/timingsByCity/{current_date}?city={city}&country={country}"

    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read())
            if data and data.get("data"):
                return data["data"]["timings"]
    except Exception as e:
        subprocess.run(
            ["notify-send", "notify-salawāt", "API Error; maybe you don't have internet access? Quitting notify-salawāt.", "-i", icon_path, "-a", "notify-salawat"])
        raise SystemExit
    return {}


def send_notification(prayer_name, prayer_time, calltype):
    subprocess.run(["notify-send", f"{prayer_name.capitalize()} Time", f" It is {prayer_time}, the time for the {prayer_name.capitalize()} {calltype}.", "-i", icon_path, "-a", "notify-salawat"])


def main():
    prayer_times = get_prayer_times()

    while True:
        current_time = datetime.now().strftime("%H:%M")
        for prayer_name, prayer_time in prayer_times.items():
            if prayer_time:
                prayer_time_obj = datetime.strptime(prayer_time, "%H:%M").time()
                current_time_obj = datetime.strptime(current_time, "%H:%M").time()

                if prayer_time_obj == current_time_obj:
                    send_notification(prayer_name, prayer_time, "adhān")
                    time.sleep(60)

                    reminder_time_obj = (
                        datetime.combine(datetime.today(), prayer_time_obj)
                        + timedelta(minutes=15)
                    ).time()
                    while datetime.now().time() < reminder_time_obj:
                        time.sleep(10)
                    send_notification(prayer_name, prayer_time, "iqāma")

        time.sleep(30)


if __name__ == "__main__":
    main()
