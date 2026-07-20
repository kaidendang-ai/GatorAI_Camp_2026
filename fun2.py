# program to get user's birthday and calculate their age in days

from datetime import datetime

name = input("What is your name? ")
birthday = input("What is your birthday? (YYYY-MM-DD) ")

# Convert the birthday string to a datetime object
birthday_date = datetime.strptime(birthday, "%Y-%m-%d")

# Calculate the age in days
age_in_days = (datetime.now() - birthday_date).days

print(f"{name} is {age_in_days} days old.")