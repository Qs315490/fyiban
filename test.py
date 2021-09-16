import os
mobile = os.getenv('YIBAN_MOBILE', default = None)
password = os.getenv('YIBAN_PASSWORD', default = None)
print(mobile)
print(password)

if "YIBAN_MOBILE" in os.environ:
    print("已获取并使用Env环境 MOBILE")
    
if mobile is None:
  print('Error')