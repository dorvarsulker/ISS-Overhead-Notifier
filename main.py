import requests
from datetime import datetime
from smtplib import *
import time


def check_pos(user_long, user_lat, isslong, isslat):
    """Returning True if the current position of ISS is nearby"""
    if user_long + 5 > iss_long > user_long - 5 and user_lat + 5 > isslat > user_lat - 5:
        return True
    else:
        return False


def check_if_dark(sunset_hour, sunrise_hour, current_hour):
    """Returns True if its dark outside"""
    if sunset_hour < current_hour < sunrise_hour:
        return True
    else:
        return False


def calculate_iss_watch(sunset, sunrise, current, userlong, userlat, isslong, isslat):
    """Checks both the location of the ISS relative to your position and if its dark outside"""
    is_dark = check_if_dark(sunset, sunrise, current)
    is_above = check_pos(userlong, userlat, isslong, isslat)

    if is_above and is_dark:
        return True
    else:
        return False

# Recieve user's email & password (To send yourself an email notifing you)
email = input("Please enter your email: ")
password = input("Please enter your password: ")

# Recieve User location coordinates.
MY_LAT = float(input("Please enter your location's latitude: "))
MY_LONG = float(input("Please enter your location's longitude: "))

# Recieve ISS location through API
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
iss_data = response.json()

# Pulling ISS location coordinates
iss_long = float(iss_data['iss_position']['longitude'])
iss_lat = float(iss_data['iss_position']['latitude'])

# Recieve local time for the User's location.
parameters = {
    "long": MY_LONG,
    "lat": MY_LAT,
    "formatted":0
}
time_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
time_response.raise_for_status()
time_data = time_response.json()

# Check when the sunrise and sunset times for the user's location.
sunrise_time = int(time_data['results']['sunrise'].split("T")[1].split(":")[0])
sunset_time = int(time_data['results']['sunset'].split("T")[1].split(":")[0])
current_time = datetime.now().hour

# A loop to check wether the ISS is overhead & It's dark outside.
while True:
    # If returns true, sends email to user.
    if calculate_iss_watch(sunset_time, sunrise_time, current_time, MY_LONG, MY_LAT, iss_long, iss_lat):
        print("You've just received an email")
        with SMTP("smtp.gmail.com") as email:
            email.starttls()
            email.login(user=email, password=password)
            email.sendmail(
                from_addr=email,
                to_addrs=email,
                msg="Subject:Testing This Feature\n\nThe ISS is over your head")
    print("I'm sorry the ISS is not overhead.")
    time.sleep(60)
