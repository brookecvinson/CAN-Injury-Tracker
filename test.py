from time import *


def is_valid_date(date_str):
    try:
        # Attempt to parse the string as a date with the specified format
        strptime(date_str, '%m/%d/%Y')
        return True
    except ValueError:
        # If parsing fails, it's not a valid date
        return False


# Example usage:
date_string = "05/10/2024"
if is_valid_date(date_string):
    print(f"{date_string} is a valid date in the format mm/dd/yyyy.")
else:
    print(f"{date_string} is not a valid date in the format mm/dd/yyyy.")
