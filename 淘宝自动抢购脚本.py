from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common import keys
from selenium.webdriver.common.action_chains import ActionChains
import random
import time
import json
import os
import pytime
from pykeyboard import *

def create_browser():  #初始化浏览器
    chrome_options = Options()
    #chrome_options.add_argument('--headless')  #定义无界面模式
    chrome_options.add_argument('--window-size=1920,1080') #定义窗口大小
    chrome_options.add_argument('--disable-gpu') #禁用谷歌gpu加速
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation']) #进入谷歌开发者模式
    chrome_options.add_argument('blink-settings=imagesEnabled=false') #采用不加载图片形式，提高速度
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  #禁用启用Blink运行时的功能
    # path为自己的chrome.exe位置，我这里写的是我自己电脑中的位置
    path = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    chrome_options.binary_location = path  #使用本地安装的浏览器
    browser = webdriver.Chrome(chrome_options=chrome_options)  #创建Chrome浏览器对象
    #Selenium执行cdp命令,
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                          get: () => undefined
                        })
                      """
    })
    #来自https://blog.csdn.net/dslkfajoaijfdoj/article/details/109146051
    return browser
def real_Click(xpahvalue:str,):  #模拟移动点击
    get_qr=''
    cishu=0
    cishu+=1
    while True:
        try:
            get_qr = browser.find_element(by=By.XPATH, value=xpahvalue)  #需要点击的对象
        except:
            pass
        if get_qr !='':
            x=random.randint(1,2)  #距离x轴偏差值
            y=random.randint(1,2)  #距离y轴偏差值
            ActionChainS = ActionChains(browser)  #创建事件对象
            #鼠标移动到元素位置上，偏移该距离左上角元素随机位置，并点击
            ActionChainS.move_to_element(get_qr).move_to_element_with_offset(to_element=get_qr,xoffset=x,yoffset=y).click().perform()
            break
class taobao:
    zhanghao=''
    url="https://www.taobao.com/"
    denglu="https://login.taobao.com/"
    jianyan=""
    zhuangtaima=0
    denglushijian=''
    qianggoutime=''
    def jiancedenglu(self):
        browser.get(self.url)
        try:
            self.on_cookies()
        except:
            print('该账号未曾使用过')
        browser.refresh()
        real_Click('//*[@id="J_SiteNavMytaobao"]/div[1]/a/span')#进入点击我的淘宝，判断是否为登录状态
        gouwucheurl=browser.current_url
        if gouwucheurl[:20] != self.denglu[:20]:  #如果能进入到我的淘宝，则为登录状态。并修改状态码
            print('账号已登录')
            self.get_cookies()  #
        else:                                     #如果不能进入我的淘宝，则为未登录状态，打开登录界面，并点击二维码登录，等待用户扫描
            self.zhuangtaima=0
            print('未登录，请扫描二维码进入登录状态')
            browser.get(self.denglu)
            real_Click('//*[@id="login"]/div[1]/i')
            if self.zhuangtaima==0:
                while True:
                    login=""
                    try:
                        #获取左上角用户登录后显示的淘宝id，有id则为登录状态
                        login=browser.find_element(by=By.XPATH,value='//*[@id="J_SiteNavLogin"]/div[1]/div/a').text
                        if login==self.zhanghao:
                            print('登录成功啦')
                            self.get_cookies()
                            break
                    except:
                        pass
    def get_cookies(self):
        self.zhuangtaima = 1
        self.denglushijian = time.time()
        jscookies = browser.get_cookies()
        jscookies = json.dumps(jscookies)
        with open(f"./{self.zhanghao}_cookies.txt", 'w', encoding='utf-8') as f:  # 保存cookies
            f.write(jscookies)
    def on_cookies(self):
        with open(f"./{self.zhanghao}_cookies.txt", 'r', encoding='utf-8') as f:
            cookies=json.load(f)
            for i in cookies :
                cookies_dict={'domain': '.taobao.com', 'httpOnly': False, 'name': i.get('name'), 'path': '/', 'sameSite': 'None', 'secure': True, 'value':i.get('value')}
                browser.add_cookie(cookies_dict)
    def buy(self):
        real_Click('//*[@id="J_MiniCart"]/div[1]/a/span[2]')#点击购物车
        real_Click('//div[@id="J_CartMain"]/div[2]//div[@class="shop-info"]/div[1]')#选择购物车第一个
        real_Click('//*[@id="J_Go"]/span')#点结算
        while True:
            dangqiantime = time.strftime('%Y-%m-%d %H:%M:%S')
            if self.qianggoutime ==dangqiantime:
                browser.refresh()
                real_Click('//*[@id="submitOrderPC_1"]//div/a[2]')#提交订单
                while True:
                    a=''
                    try:
                        a=browser.find_element(by=By.XPATH,value='//*[@id="J_authSubmit"]')
                    except:
                        pass
                    if a != "":     #检测到确认支付按钮，输入密码
                        k=PyKeyboard()#构建键盘对象
                        k.type_string("") #输入密码
                        break
                real_Click('//*[@id="J_authSubmit"]')
if __name__=='__main__':
    browser = create_browser() #构建浏览器对象
    taobao = taobao()       #构建淘宝类
    # 设置使用的淘宝账号
    taobao.zhanghao = ''
    taobao.qianggoutime='2022-06-17 19:30:00'
    # 检验登录状态
    try:
        taobao.jiancedenglu()
        # 进入购物车选择第一个商品进行下单
        taobao.buy()
    except:
        browser.save_screenshot("yichangye.png")
        # with open(f"./{taobao.zhanghao}_cookies.txt", 'w', encoding='utf-8') as f:
        #     pass
