import os
import yaml
import time
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select


class Base:
    def __init__(self, driver: webdriver.Chrome, timeout=5, poll=0.5):
        self.driver = driver
        self.timeout = timeout
        self.poll = poll
        self.yaml = self.yaml_load(os.path.join(os.path.dirname(os.getcwd()), "config.yaml"))
        self.default = self.yaml.get("default")
        self.host = self.yaml.get("host")

    def find(self, locator):
        """ todo 单个元素定位：locator = ("id", "id值") """
        if len(locator) > 2:
            locator = (self.default, locator)
            try:
                element = WebDriverWait(self.driver, self.timeout, self.poll).until(
                    lambda x: x.find_element(*locator))
                return element
            except:
                logging.error('元素定位超时，定位方式->%s,value值->%s' % (locator[0], locator[1]))
        elif not isinstance(locator, tuple):
            logging.error('参数类型错误，locator必须是元祖类型')
        else:
            try:
                element = WebDriverWait(self.driver, self.timeout, self.poll).until(
                    lambda x: x.find_element(*locator))
                return element
            except:
                logging.error('元素定位超时，定位方式->%s,value值->%s' % (locator[0], locator[1]))

    def finds(self, locator):
        """ todo 复数元素定位：locator = ("id", "id值")[x]，取第几个？ """
        if len(locator) > 2:
            locator = (self.default, locator)
            try:
                element = WebDriverWait(self.driver, self.timeout, self.poll).until(
                    lambda x: x.find_elements(*locator))
                return element
            except:
                logging.error('元素定位超时，定位方式->%s,value值->%s' % (locator[0], locator[1]))
        elif not isinstance(locator, tuple):
            logging.error('参数类型错误，locator必须是元祖类型')
        else:
            try:
                element = WebDriverWait(self.driver, self.timeout, self.poll).until(
                    lambda x: x.find_elements(*locator))
                return element
            except:
                logging.error('元素定位超时，定位方式->%s,value值->%s' % (locator[0], locator[1]))

    def send(self, locator, _text):
        """ todo 文本输入 """
        try:
            self.find(locator).send_keys(_text)
        except:
            logging.error('元素定位超时，定位方式->%s,value值->%s' % (locator[0], locator[1]))

    def click(self, locator):
        """ todo 点击操作 """
        try:
            self.find(locator).click()
        except:
            logging.error('元素定位超时，定位方式->%s,value值->%s' % (locator[0], locator[1]))

    def clear(self, locator):
        """ todo 清空文本 """
        try:
            self.find(locator).clear()
        except:
            logging.error('清空文本发生异常，定位方式->%s,value值->%s' % (locator[0], locator[1]))

    def text_in_enement(self, locator, _text):
        """ todo 判断 _text 文本值是否 in 定位元素中，返回 bool 值"""
        if len(locator) > 2:
            locator = (self.default, locator)
            try:
                WebDriverWait(self.driver, self.timeout, self.poll
                              ).until(EC.text_to_be_present_in_element(locator, _text))
                return True
            except:
                return False
        else:
            if not isinstance(locator, tuple):
                logging.error('参数类型错误，locator必须是元祖类型')
            else:
                try:
                    WebDriverWait(self.driver, self.timeout, self.poll
                                  ).until(EC.text_to_be_present_in_element(locator, _text))
                    return True
                except:
                    return False

    def get_enement(self, locator):
        """ todo 判断元素是否存在，返回 bool 值 """
        if len(locator) > 2:
            locator = (self.default, locator)
            try:
                self.find(locator)
                return True
            except:
                return False
        else:
            if not isinstance(locator, tuple):
                logging.error('参数类型错误，locator必须是元祖类型')
            else:
                try:
                    self.find(locator)
                    return True
                except:
                    return False

    def get_text(self, locator):
        """ todo 获取元素的文本值 """
        if len(locator) > 2:
            locator = (self.default, locator)
            try:
                element_text = WebDriverWait(self.driver, self.timeout, self.poll).until(
                    lambda x: x.find_element(*locator).text)
            except:
                element_text = ''
            return element_text
        else:
            if not isinstance(locator, tuple):
                logging.error('参数类型错误，locator必须是元祖类型')
            else:
                try:
                    element_text = WebDriverWait(self.driver, self.timeout, self.poll).until(
                        lambda x: x.find_element(*locator).text)
                except:
                    element_text = ''
                return element_text

    def exp_title(self, title=''):
        """ todo 断言获取当前页面的 title，完全匹配 返回bool值 """
        try:
            t = WebDriverWait(self.driver, self.timeout, self.poll).until(EC.title_is(title))
            return t
        except:
            return False

    def move_element(self, locator):
        """ todo 鼠标悬停操作 """
        try:
            element = self.find(locator)
            ActionChains(self.driver).move_to_element(element).perform()
        except:
            logging.error('鼠标悬停操作发生异常，定位方式->%s' % locator)

    def select_index(self, locator, index=0):
        """ todo index是索引定位第x个，从0开始，默认第1个 """
        try:
            element = self.find(locator)
            Select(element).select_by_index(index)
        except:
            logging.error('select中的index方法发生异常，定位方式->%s' % locator)

    def select_value(self, locator, value):
        """ todo select中的value方法，如html中：value="50"，则value传：50 """
        try:
            element = self.find(locator)
            Select(element).select_by_value(value)
        except:
            logging.error('select中的value方法-发生异常，定位方式->%s' % locator)

    def select_text(self, locator, text):
        """ todo select中的text方法全匹配文本，如html中显示：每页显示50条，则文本需全部匹配 """
        try:
            element = self.find(locator)
            Select(element).select_by_visible_text(text)
        except:
            logging.error('select中的text方法-发生异常，定位方式->%s' % locator)

    def switch_iframe(self, index_locator):
        """ todo 切换iframe：传下标 或 locator """
        try:
            if isinstance(index_locator, int):
                self.driver.switch_to.frame(index_locator)
            else:
                element = self.find(index_locator)
                self.driver.switch_to.frame(element)
        except:
            logging.error("iframe切换发生异常：%s" % index_locator)

    def is_alert(self, _text='确定', send_alert=None):
        """
        todo alert弹窗处理：
            --1.默认点击：确定
            --2.取消操作传：取消
            --3.获取弹窗文本传：text
            --4.弹出输入文本传：输入 + 文本值
       """
        try:
            WebDriverWait(self.driver, self.timeout, self.poll).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            if _text == 'text':
                return 'alert获取的文本为：%s' % alert.text
            elif _text == '输入':
                alert.send_keys(send_alert)
                return 'alert弹窗已为您输入文本：%s' % send_alert
            elif _text == '取消':
                alert.dismiss()
                return 'alert弹窗已为您处理：取消'
            else:
                alert.accept()
                return 'alert弹窗已为您处理：确定'
        except:
            return False

    def switch_handle(self, window_name):
        """ todo 句柄切换，传int类型，从0开始，-1既是最新打开的一个 """
        try:
            if not isinstance(window_name, int):
                logging.error('参数类型错误，window_name必须传 int 类型！！！')
            else:
                handlels = self.driver.window_handles
                self.driver.switch_to.window(handlels[window_name])
        except:
            logging.error('句柄切换发生错误：%s' % window_name)

    def js_top(self):
        """ todo 页面滚动条滑动至顶部 """
        self.driver.execute_script('window.scrollTo(0,0)')

    def js_element(self, locator):
        """ todo 聚焦元素位置 """
        if not isinstance(locator, tuple):
            logging.error('参数类型错误，locator必须是元祖类型')
        else:
            try:
                element = self.find(locator)
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
            except:
                logging.error('聚焦元素位置-发生异常，定位方式：' % locator)

    def js_tail(self):
        """ todo 页面滚动条滑动至底部 """
        self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')

    @staticmethod
    def yaml_load(path):
        """ todo 读取yaml文件 """
        try:
            with open(path, encoding="utf-8") as f:
                return yaml.safe_load(f)
        except IOError:
            return logging.error("请检查 yaml 文件目录或格式是否正确")

    def get(self, url):
        """ todo 打开网站 """
        return self.driver.get(url)

    def open(self, url):
        """ todo 打开网站 """
        return self.driver.get(url)

    def quit(self):
        """ todo 关闭浏览器 """
        return self.driver.quit()

    def refresh(self):
        """ todo 刷新页面 """
        return self.driver.refresh()

    def del_cookie(self):
        """ todo 清空缓存 """
        return self.driver.delete_all_cookies()

    """ 以下是元素操作传参的封装，请按照RMD文件示例格式进行使用@全体成员"""
    def location(self, locator):
        """ todo 单个定位 """
        try:
            res = WebDriverWait(self.driver, self.timeout, self.poll).until(
                lambda x: x.find_element(*locator))
            return res
        except:
            logging.error("格式错误或超时-->locator实际为：%s" % locator)

    def locations(self, locator):
        """ todo 复数定位 """
        try:
            res = WebDriverWait(self.driver, self.timeout, self.poll).until(
                lambda x: x.find_elements(*locator))
            return res
        except:
            logging.error("格式错误或超时-->locator实际为：%s" % locator)

    def handle(self, locators):
        """ todo 元素操作的数据处理 """
        txt = "".join(locators)
        if "open" in txt:
            self.open(self.host+locators[-1])
        elif"sends" in txt:
            try:
                index = int(locators[2])
            except:
                index = None
                logging.error("sends：格式错误，格式必须为：('sends','输入的文本','下标','元素值')或('sends','输入的文本','下标','定位方式如id','元素值')")
            if len(locators) == 4 and type(index) is int:
                try:
                    locator = (self.default, locators[-1])
                    _text = locators[1]
                    res = self.locations(locator)
                    return res[index].send_keys(_text)
                except:
                    logging.error("sends：元素不存在或超时，默认格式必须为：('sends','输入的文本','下标','元素值') -->locator为：%s,输入为：%s下标为：%s" % (
                        locator, _text, index))
            elif len(locators) == 5 and type(index) is int:
                try:
                    _text = locators[1]
                    locator = (locators[-2], locators[-1])
                    res = self.locations(locator)
                    return res[index].send_keys(_text)
                except:
                    logging.error(
                        "sends：元素不存在或超时，自定义格式必须为：('sends','输入的文本','下标','定位方式如id','元素值') -->locator为：%s,输入为：%s下标为：%s" % (
                            locator, _text, index))
            else:
                logging.error("sends：格式错误，格式必须为：('sends','输入的文本','下标','元素值')或('sends','输入的文本','下标','定位方式如id','元素值')")
        elif "send" in txt:
            if len(locators) == 3:
                try:
                    locator = (self.default, locators[-1])
                    _text = locators[-2]
                    res = self.location(locator)
                    return res.send_keys(_text)
                except:
                    logging.error(
                        "send：元素不存在或超时，默认格式必须为：('send','输入的文本','元素值') -->locator实际为：%s,输入为：%s" % (locator, _text))
            elif len(locators) == 4:
                try:
                    _text = locators[-3]
                    locator = (locators[-2], locators[-1])
                    res = self.location(locator)
                    return res.send_keys(_text)
                except:
                    logging.error(
                        "send：元素不存在或超时，自定义定位格式必须为：('send', '输入的文本', '定位方式如id', '元素值') -->locator实际为：%s,输入为：%s" % (
                            locator, _text))
            else:
                logging.error("send：格式错误,格式必须为:('send','输入的文本','元素值')或('send', '输入的文本', '定位方式如id', '元素值')")
        elif "clears" in txt:
            try:
                index = int(locators[1])
            except:
                index = None
                logging.error(
                    "clears：格式错误，格式必须为：('sends','输入的文本','下标','元素值')或('sends','输入的文本','下标','定位方式如id','元素值')")
            if len(locators) == 3 and type(index) is int:
                try:
                    locator = (self.default, locators[-1])
                    res = self.locations(locator)
                    return res[index].clear()
                except:
                    logging.error(
                        "clears：元素不存在或超时，默认格式必须为：('0', 'clear', '元素值')-->locator为：%s,输入为：%s下标为：%s" % (locator, index))
            elif len(locators) == 4 and type(index) is int:
                try:
                    locator = (locators[-2], locators[-1])
                    res = self.locations(locator)
                    return res[index].clear()
                except:
                    logging.error(
                        "clears：元素不存在或超时，自定义格式必须为：('clear', '定位方式如id', '元素值')-->locator为：%s,输入为：%s下标为：%s" % (
                            locator, index))
            else:
                logging.error("clears：格式错误，格式必须为：('sends','输入的文本','下标','元素值')或('sends','输入的文本','下标','定位方式如id','元素值')")
        elif "clear" in txt:
            if len(locators) == 2:
                try:
                    locator = (self.default, locators[-1])
                    res = self.location(locator)
                    return res.clear()
                except:
                    logging.error("clear：元素不存在或超时，默认格式必须为：('clear', '元素值') -->locator实际为：%s" % locator)
            elif len(locators) == 3:
                try:
                    locator = (locators[-2], locators[-1])
                    res = self.location(locator)
                    return res.clear()
                except:
                    logging.error("clear：元素不存在或超时，自定义定位格式必须为：('clear', '定位方式如id', '元素值') -->locator实际为：%s" % locator)
            else:
                logging.error("clear格式错误,格式必须为：('clear', '元素值')或('clear', '定位方式如id', '元素值')")
        elif "txt_in_ele" in txt:
            if len(locators) == 3:
                locator = (self.default, locators[-1])
                _text = locators[-2]
                try:
                    WebDriverWait(self.driver, self.timeout, self.poll
                                  ).until(EC.text_to_be_present_in_element(locator, _text))
                    return True
                except:
                    return False
            elif len(locators) == 4:
                locator = (locators[-2], locators[-1])
                _text = locators[1]
                try:
                    WebDriverWait(self.driver, self.timeout, self.poll
                                  ).until(EC.text_to_be_present_in_element(locator, _text))
                    return True
                except:
                    return False
            else:
                logging.error(
                    'text_in_ele：格式错误，格式必须为：("text_in_ele","泡泡龙","#kw")或("text_in_ele", "泡泡龙", "id", "kw")')
        elif "get_txts" in txt:
            try:
                index = int(locators[1])
            except:
                logging.error(
                    "get_txts：格式错误，必须为：('get_txts','0','#s-usersetting-top')或('get_txts','0','id','s-usersetting-top')")
                index = None
            if len(locators) == 3 and type(index) is int:
                locator = (self.default, locators[-1])
                try:
                    element_text = self.locations(locator)[index].text
                except:
                    element_text = None
                return element_text
            elif len(locators) == 4 and type(index) is int:
                locator = (locators[-2], locators[-1])
                try:
                    element_text = self.locations(locator)[index].text
                except:
                    element_text = None
                return element_text
            else:
                logging.error(
                    "get_txts：格式错误，必须为：('get_txts','0','#s-usersetting-top')或('get_txts','0','id','s-usersetting-top')")
        elif "get_txt" in txt:
            if len(locators) == 2:
                locator = (self.default, locators[-1])
                try:
                    element_text = WebDriverWait(self.driver, self.timeout, self.poll).until(
                        lambda x: x.find_element(*locator).text)
                except:
                    element_text = None
                return element_text
            elif len(locators) == 3:
                locator = (locators[-2], locators[-1])
                try:
                    element_text = WebDriverWait(self.driver, self.timeout, self.poll).until(
                        lambda x: x.find_element(*locator).text)
                except:
                    element_text = None
                return element_text
            else:
                logging.error('get_text：格式错误，格式必须为：("get_text","#kw")或("get_text","id","kw")')
        elif "get_eles" in txt:
            try:
                index = int(locators[1])
            except:
                index = None
                logging.error('get_ele：格式错误，格式必须是("get_ele","0","#kw")或("get_ele","0","id","kw")')
            if len(locators) == 3 and type(index) is int:
                locator = (self.default, locators[-1])
                try:
                    res = self.locations(locator)[index]
                    if res:
                        return True
                    else:
                        return False
                except:
                    return False
            elif len(locators) == 4 and type(index) is int:
                locator = (locators[-2], locators[-1])
                try:
                    res = self.locations(locator)[index]
                    if res:
                        return True
                    else:
                        return False
                except:
                    return False
            else:
                logging.error('get_ele：格式错误，格式必须是("get_ele","0","#kw")或("get_ele","0","id","kw")')
        elif "get_ele" in txt:
            if len(locators) == 2:
                locator = (self.default, locators[-1])
                try:
                    self.find(locator)
                    return True
                except:
                    return False
            elif len(locators) == 3:
                locator = (locators[-2], locators[-1])
                try:
                    self.find(locator)
                    return True
                except:
                    return False
            else:
                logging.error('get_ele：格式错误，格式必须是("get_ele","#kw")或("get_ele","id","kw")')
        else:
            try:
                index = int(locators[0])
            except:
                index = ""
            if len(locators) > 5:
                try:
                    locator = (self.default, locators)
                    res = self.location(locator)
                    return res.click()
                except:
                    logging.error("click：元素不存在或超时：默认定位格式必须为：'元素值xxx' -->locator实际为：%s" % locator)
            elif isinstance(index, int):
                if len(locators) == 3:
                    try:
                        locator = (locators[1], locators[-1])
                        num = int(locators[0])
                        res = self.locations(locator)
                        return res[num].click()
                    except:
                        logging.error(
                            "clicks：元素不存在或超时，自定义格式必须为：('0', 'id', 's-top-left')-->locator为：%s,输入为：%s下标为：%s" % (
                                locator, num))
                elif len(locators) == 2:
                    try:
                        locator = (self.default, locators[-1])
                        res = self.locations(locator)
                        return res[index].click()
                    except:
                        logging.error(
                            "clicks：元素不存在或超时，默认格式必须为：('0', 's-top-left')-->locator为：%s,输入为：%s下标为：%s" % (
                                locator, index))
                else:
                    logging.error("clicks：格式错误，格式必须为：('0', 's-top-left')或('0', 'id', 's-top-left')")
            elif len(locators) == 2:
                try:
                    locator = (locators[-2], locators[-1])
                    res = self.location(locator)
                    return res.click()
                except:
                    logging.error("clicks：元素不存在或超时：自定义定位格式必须为：('定位方式如id', '元素值') -->locator实际为：%s" % locator)
            else:
                logging.error(
                    "点击操作格式错误，单数格式必须为：'元素值xxx'或('定位方式如id', '元素值')，复数必须为：('0', 's-top-left')或('0', 'id', 's-top-left')")

    def step(self, locators):
        if len(locators) > 5:
            return self.handle(locators)
        elif not isinstance(locators, tuple):
            logging.error('参数类型错误，locator必须是元祖类型')
        else:
            return self.handle(locators)

    def loop(self, loops: object, break_num: int):
        """ todo 循环操作每个步骤 """
        num = 0
        while 1:
            num += 1
            self.step(next(loops, None))
            if num == break_num:
                break


if __name__ == '__main__':
    from common.driver import is_driver

    driver = is_driver()
    b = Base(driver)
    b.step("open", "https://www.baidu.com/")

    loc1 = "#s-top-left"                                    # todo click ：默认【单个】定位方法
    loc2 = ("id", "s-top-left")                             # todo click：自定义【单个】定位方法
    loc11 = ("0", "#s-top-left")                            # todo click ：默认【复数】定位方法
    loc22 = ("0", "id", "s-top-left")                       # todo click ：自定义【复数】定位方法

    loc3 = ("send", "广深小龙", "#kw")                      # todo send ：默认【单个】定位方法
    loc4 = ("send", "广深小龙", "id", "kw")                 # todo send：自定义【单个】定位方法
    loc33 = ("sends", "广深小龙", "0", "#kw")               # todo send ：默认定位方法：send 写法
    loc44 = ("sends", "广深小龙", "0", "id", "kw")          # todo send ：自定义【复数】定位方法

    loc5 = ("clear", "#kw")                                 # todo clear：默认【单个】定位方法
    loc51 = ("clear", "id", "kw")                           # todo clear：默认【单个】定位方法
    loc55 = ("clears", "0", "#kw")                          # todo clear：自定义【复数】定位方法
    loc551 = ("clears", "0", "id", "#kw")                   # todo clear：自定义【复数】定位方法

    # todo txt in 元素文本值，只能单数，返回布尔值
    loc6 = ("txt_in_ele", "设置", "#s-usersetting-top")        # todo clear：默认【单个】定位方法
    loc66 = ("txt_in_ele", "设置", "id", "s-usersetting-top")  # todo clear：默认【单个】定位方法

    # 判断元素值存不存在，支持单复数，返回布尔值
    loc7 = ("get_ele", "id", "su")                          # todo clear：默认【单个】定位方法
    loc77 = ("get_ele", "#su")                              # todo clear：默认【单个】定位方法

    loc71 = ("get_eles", "0", "id", "su")                   # todo clear：默认【单个】定位方法
    loc771 = ("get_eles", "0", "#su")                       # todo clear：默认【单个】定位方法

    loc8 = ("get_txt", "#s-usersetting-top")
    loc88 = ("get_txt", "id", "s-usersetting-top")

    loc81 = ("get_txts", "0", "#s-usersetting-top")
    loc881 = ("get_txts", "0", "id", "s-usersetting-top")

    # b.step(loc1)
    # b.step(loc11)
    # b.step(loc2)
    # b.step(loc22)
    # b.step(loc3)
    # b.step(loc33)
    # b.step(loc4)
    # b.step(loc44)
    # b.step(loc5)
    # b.step(loc55)

    # print(b.step(loc6))
    # print(b.step(loc66))

    # print(b.step(loc7))
    # print(b.step(loc77))

    # print(b.step(loc71))
    # print(b.step(loc771))

    # print(b.step(loc8))
    # print(b.step(loc88))

    # print(b.step(loc81))
    print(b.step(loc881))

    time.sleep(1)
    driver.quit()
