from datetime import datetime, timedelta
import subprocess, os, argparse, time, json, urllib.request


def get_prayer_times(city, country):
    current_date = datetime.now().strftime("%d-%m-%Y")
    api_url = f"https://api.aladhan.com/v1/timingsByCity/{current_date}?city={city}&country={country}"
    print(f"Using API URL: {api_url}")

    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read())
            if data and data.get("data"):
                timings = data["data"]["timings"]
                # fmt: off
                for key in ["Sunrise", "Sunset", "Imsak", "Midnight", "Firstthird", "Lastthird"]:
                    # fmt: on
                    timings.pop(key, None)
                return timings
    except Exception as e:
        # fmt: off
        subprocess.run(["notify-send", "notify-salawāt", "API Error; maybe you don't have internet access? Quitting notify-salawāt.", "-i", icon_path, "-a", "notify-salawat"])
        # fmt: on
        raise SystemExit
    return {}


def send_notification(prayer_name, prayer_time, calltype): # fmt: off
    subprocess.run(["notify-send", f"{prayer_name.capitalize()} Time", f" It is {prayer_time}, the time for the {prayer_name.capitalize()} {calltype}.", "-i", icon_path, "-a", "notify-salawat"])
    # fmt: on


def main(city, country, iqama_enabled, gap_minutes):
    prayer_times = get_prayer_times(city, country)

    while True:
        current_time = datetime.now().strftime("%H:%M")
        for prayer_name, prayer_time in prayer_times.items():
            if prayer_time:
                prayer_time_obj = datetime.strptime(prayer_time, "%H:%M").time()
                current_time_obj = datetime.strptime(current_time, "%H:%M").time()

                if prayer_time_obj == current_time_obj:
                    send_notification(prayer_name, prayer_time, "adhān")
                    time.sleep(60)

                    if iqama_enabled:
                        # fmt: off
                        reminder_time_obj = (datetime.combine(datetime.today(), prayer_time_obj) + timedelta(minutes=gap_minutes)).time()
                        # fmt: on
                        while datetime.now().time() < reminder_time_obj:
                            time.sleep(15)
                        send_notification(prayer_name, prayer_time, "iqāma")
        time.sleep(30)


parser = argparse.ArgumentParser(
    prog="notify-salawāt",
    description="A Python CLI program for Linux for sending notifications at the adhān and iqāma times of each Islāmic prayer.",
    epilog="This program is open source! https://github.com/orangci/notify-salawat",
)

# fmt: off
parser.add_argument("--city", required=True, help="Your city.")
parser.add_argument("--country", required=True, help="Your country.")
parser.add_argument("-i", "--iqama", action="store_true", default=True, help="Enable iqāma notifications.")
parser.add_argument("-g", "--gap", type=int, default=15, help="Gap in minutes between the adhān and iqāma notifications.")
# fmt: on

args = parser.parse_args()
icon_path = f"{subprocess.check_output(['pwd']).decode('utf-8').strip()}/icon.png"

print("\033[1mSuccess! If all goes well, you'll be notified at the adhān and iqāma of each salah, insha'allah. <3\033[0m\n")
main(args.city, args.country.replace(" ", "+"), args.iqama, args.gap - 1)