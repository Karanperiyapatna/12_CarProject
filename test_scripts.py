from datetime import datetime


cdt = datetime.today()
cdt = datetime.strftime(cdt, '%y-%m-%d %H:%M:%S')
print(cdt)



import datetime

start_date = "2024-07-27"
end_date = "2024-07-28"

date_format = "%Y-%m-%d"
start_date = datetime.datetime.strptime(start_date, date_format)
end_date = datetime.datetime.strptime(end_date, date_format)
a =  abs((end_date-start_date).days)
ab = int(a) + 1
print(ab)




# def date_range_list(start_date, end_date):
#     # Return list of datetime.date objects (inclusive) between start_date and end_date (inclusive).
#     date_list = []
#     curr_date = start_date
#     while curr_date <= end_date:
#         date_list.append(curr_date)
#         curr_date += timedelta(days=1)
#     return date_list

# days = date_range_list(start_date, end_date)
# # print(days)


'''
# Generate the first two letters (uppercase)
first_two_letters = ''.join(random.choices(strings.ascii_uppercase, k=2))
# Generate the next two digits
two_digits = ''.join(random.choices(string.digits, k=2))
# Combine them to form the unique ID
labour_id = first_two_letters + two_digits
print(labour_id)
'''



'''

import pytz

IST = pytz.timezone('Asia/Kolkata')
inserted_at= datetime.now(IST)  # Correctly localized to IST
print(inserted_at)


'''



'''
import random
import string

# Generate the first two letters (uppercase)
first_two_letters = ''.join(random.choices(string.ascii_uppercase, k=2))

# Generate the next two digits
two_digits = ''.join(random.choices(string.digits, k=2))

# Combine them to form the unique ID
unique_id = first_two_letters + two_digits

print(unique_id)

'''




'''

import uuid
import random

# Generate a UUID
unique_id = str(uuid.uuid4())
print(unique_id)

# Extract the first two letters and convert them to uppercase
first_two_letters = unique_id[:2].upper()

# Generate two random digits
two_digits = f"{random.randint(0, 9)}{random.randint(0, 9)}"

# Combine the parts to form the final unique ID
final_unique_id = first_two_letters + two_digits

print(final_unique_id)

'''


'''
import mysql.connector

cnx = mysql.connector.connect(user='root', password='YES',
                              host='127.0.0.1',
                              database='vehicle_rental',
                              use_pure=False)
cnx.close()
'''