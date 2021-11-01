# YibanAuto
### 适用于易班校本化分应用打卡
### config.json中提交表单需要手动抓包填写


## Usage
```
# edit config.json
{
    "UserList": [
        {"name": "张三", "mobile": "mobile", "password": "password"}, 
        {...}
    ],

    "SubmitData": {
        "Data": {...}, 
        "Extend": {...}
    }
}

# python index.py
```

