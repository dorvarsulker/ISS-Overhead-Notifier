# ISS-Overhead-Notifier
Checks if the ISS is observeable by you, and sends an email if it is.

To check if it is observable , two conditions needs to be met:
1.The ISS is approx over user's head. to check that, I took the user input regarding his location (using coordinates) and compared them to the ISS coordinates.
2.If it is over user's head, it checks to see if its dark outside. taking the User's location current time and comparing it to the sunset & sunrise time.
3. If both conditions are met, than the program sends an email roughly every minute to the user.
