import time
import json
import base64
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

class SubmitTask():
    def __init__(self, subList) -> None:
        """
        selenium自动化打卡，传入列表，并支持多人打卡
        example:
        [
            {
            'name': 'Sricor',  # 名称
            'unHealth': '否',  # 健康异常状态(非必须)
            'wfid': '79e8f8c7172f88705f4161ef0f379285',  # wfid
            'temperature': '36.5',  # 体温
            'location': '示例位置',  # 位置
            'journeyCode': 'C:/Users/Sricor/OneDrive/Data/img/1.jpg',  # 行程码图片路径
            'healthCode': 'C:/Users/Sricor/OneDrive/Data/img/2.jpg',  # 健康码图片路径
            'cookie': {
                'name': 'PHPSESSID', 
                'value': '62c5e24d697ae5d262709160a6cfe8f7', 
                'domain': '.uyiban.com'},  # 登录状态cookie，只需要PHPSESSID
            'extend': {
                "TaskId": "", 
                "title": "任务信息", 
                "content": [
                    {"label": "任务名称", "value": "每日学生疫情上报"}, 
                    {"label": "发布机构", "value": "学生处"}, 
                    {"label": "发布人", "value": "邸灿"}
                    ]
                }, 
            },
            {...}
        ]
        """
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.action = ActionChains(self.driver)
        self.driver.implicitly_wait(60)  # 隐式等待
        self.result = {}
        print('selenium action')
        for i in subList:
            self.submit(i)
            print(f'{i["name"]}：Done')
            time.sleep(1)

    def __del__(self):
        print('selenium end')
        self.driver.close()  # 生命周期结束，关闭浏览器

    def selectXPath(self, XPath):
        return self.driver.find_element_by_xpath(XPath)

    def submit(self, data):
        """
        主自动化函数，传入单个对象
        """
        # 预跳转
        self.driver.get('https://app.uyiban.com')
        # 设置cookie，保持登录状态
        self.driver.add_cookie({
            'domain':  data['cookie']['domain'], 
            'name': data['cookie']['name'], 
            'value': data['cookie']['value']
        })

        extend = base64.b64encode(quote(json.dumps(data['extend'], ensure_ascii=False)).encode("utf-8")).decode('utf-8')

        self.driver.get(f'https://app.uyiban.com/workflow/client/#/initiate?wfid={data["wfid"]}&extend={extend}')  # 跳转工作流页面
        self.selectXPath('//*[@id="root"]/div/main/div[4]/div[2]/div[2]/input').send_keys(data['temperature'])  # 体温
        self.selectXPath('//*[@id="root"]/div/main/div[4]/div[3]/textarea').send_keys(data['location'])  # 位置
        self.selectXPath('//*[@id="root"]/div/main/div[4]/div[4]/div[3]/div/div/div/div[1]/div/input').send_keys(data['journeyCode'])  # 行程码
        self.selectXPath('//*[@id="root"]/div/main/div[4]/div[5]/div[3]/div/div/div/div[1]/div/input').send_keys(data['healthCode'])  # 健康码
        
        # 动态元素选择，弹出滑动框，异常状态选择否
        self.selectXPath('//*[@id="root"]/div/main/div[4]/div[1]/div[2]').click()  # 弹出滑动选择框
        time.sleep(1)
        unHealth = self.selectXPath('//*[contains(@id,"am-modal-container")]/div/div[2]/div/div/div/div[2]/div/div/div[3]/div[1]')  # 滑动选择
        self.action.click_and_hold(unHealth).move_by_offset(0, -35).release().perform()  # 向下滑动
        time.sleep(1)
        self.selectXPath('//*[contains(@id,"am-modal-container")]/div/div[2]/div/div/div/div[1]/a[2]').click() # 确定

        self.selectXPath('//*[@id="root"]/div/footer/a').click()  # 提交
        self.driver.delete_all_cookies()  # 清除cookie登录状态


if __name__ == '__main__':
    SubmitTask()