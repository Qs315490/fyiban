<h1 align="center"> 易班 🔔</h1>  
  
- 🔥 简单、易用、可扩展的易班 API 接口  
- 📕 适用于校本化分应用打卡
- 🔧 可适配不同分应用


[![python version](https://img.shields.io/pypi/pyversions/fyiban)](https://pypi.org/project/fyiban/)

```bash
pip install --upgrade fyiban
```

## 快速入门

```python
"""快速入门"""
from yiban import Yiban

if __name__ == '__main__':
    yb = Yiban("手机号", "密码")
    user   = yb.get_user_name()         # 获取用户信息
    token  = yb.get_access_token()      # 获取登录密钥
    uftask = yb.get_uncompleted_task()  # 获取校本化未完成任务
    ...

```
## 示例 
- 校本化健康打卡提交示例 [SubmitTask](https://github.com/Sricor/yiban/blob/main/examples/example-03-%E5%81%A5%E5%BA%B7%E6%89%93%E5%8D%A1.py)  

```python
"""校本化健康打卡"""
from yiban import Yiban

if __name__ == '__main__':
    task_data = {
        "Data":{...},
        "Extend": {...}
    }
    yb = Yiban("手机号", "密码")
    yb.submit_task(task_data)
    ...
```

- 更多示例 [Examples](https://github.com/sricor/yiban/tree/main/examples)



## 目录结构
```
yiban
├── Apis
│   ├── Task.py
│   ├── User.py
│   └── Yiban.py
└── Core
    ├── BaseYiban.py
    ├── Login.py
    └── STask.py
```


## 声明

> 此项目仅供学习交流，为配合防疫工作，请确保每日体温正常再进行上报。  