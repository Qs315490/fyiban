# YibanAuto
### 适用于易班校本化分应用打卡
### 提交表单需要手动抓一次包
### 可直接Fork利用Actions运行

## 10.14更新：
## 提交表单数据中data和extend替换成Str
## 暂存Cookie使用Selenium进行最后一步的提交


```
# index.py
# 适用于多人打卡
"USER": [
  {
    "name": "",  # 名称
    "mobile": "",  # 账号
    "password": ""  # 密码
  },
  {
    "name": "",
    "mobile": "",
    "password": ""
  }
],
```


```
# FIX 
# 因学业原因，逆向js需要时间。
# 暂时改用Selenium进行打卡，详情查看submit.py注释
# data与extend暂时弃用
"data": {...}
"extend": {...}
```

