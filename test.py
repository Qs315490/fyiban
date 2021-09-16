import os
mobile = os.getenv('YIBAN_MOBILE', default = None)
password = os.getenv('YIBAN_PASSWORD', default = None)
print(mobile)
print(password)

if "YIBAN_MOBILE" in os.environ:
    print(type(mobile))
    print(type(password))