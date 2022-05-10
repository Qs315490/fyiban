<h2 align="center">适用于易班校本化分应用打卡🔔</h2>

## Basic Usage

克隆本仓库
```Bash
git clone https://github.com/Sricor/yiban.git
```

安装依赖
```Bash
cd yiban
pip install -r requirements.txt
```

修改 index.py 中 `config` 配置

```Bash
python3 index.py
```


<details>
<summary>Config 配置项说明</summary><br>
<li>手动抓包提交<br></li>
<li>找到 Str 加密表单<br></li>
<li>利用 crypter.py 解密<br></li>
<li>修改 index.py config<br></li>
<br></details>

<br>

<details>
<summary>Qinglong 配置</summary><br>

```
ql repo https://github.com/Sricor/yiban.git "index" "crypter|yiban" "utils" "main"
```

<br></details>
