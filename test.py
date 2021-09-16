import os
mobile = os.getenv('MOBILE', default = None)
password = os.getenv('PASSWORD', default = None)
print(mobile)
print(password)

if mobile is None:
  print('Error')