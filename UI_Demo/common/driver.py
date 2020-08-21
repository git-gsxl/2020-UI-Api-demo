import sys
import os
from selenium import webdriver
from common.base import Base
config = Base.yaml_load(os.path.join(os.path.dirname(os.getcwd()), "config.yaml"))


def is_driver():
    browser = config.get("browser")         # todo 浏览器选择配置
    win_modes = config.get("win_UI_mode")   # todo Windows模式配置

    # todo docker-selenium 配置
    docker_selenium = config.get("docker-selenium")
    mode = docker_selenium.get("mode")
    host_port = docker_selenium.get("host_port")
    remote_mode = config.get("remote_mode")

    options = webdriver.ChromeOptions()                 # todo ChromeOptions配置
    options.add_argument('headless')                    # todo 浏览器不提供可视化页面
    options.add_argument('no-sandbox')                  # todo 以最高权限运行
    options.add_argument('--start-maximized')           # todo 最大化运行（全屏窗口）设置元素定位比较准确
    options.add_argument('--disable-gpu')               # todo 谷歌文档提    到需要加上这个属性来规避bug
    options.add_argument('--window-size=1920,1080')     # todo 设置浏览器分辨率（窗口大小）
    # todo 判断在哪个系统下运行，如linux、Windows
    if 'linux' in sys.platform:
        if mode:
            driver = webdriver.Remote(
                command_executor=host_port + '/wd/hub',
                desired_capabilities={'browserName': browser},
                keep_alive=True,
                options=options)
        else:
            driver = webdriver.Chrome(options=options)
    else:
        if remote_mode:
            driver = webdriver.Remote(
                command_executor=host_port + '/wd/hub',
                desired_capabilities={'browserName': browser},
                keep_alive=True,
                options=options)
        elif win_modes.get("UI_mode"):
            if win_modes.get("max_window"):
                driver = webdriver.Chrome()
                driver.maximize_window()
            else:
                driver = webdriver.Chrome()
        else:
            option = webdriver.ChromeOptions()               # todo win系统下无界面模式
            option.add_argument('headless')                  # todo 浏览器不提供可视化页面
            option.add_argument('--start-maximized')         # todo 最大化运行（全屏窗口）设置元素定位比较准确
            option.add_argument('--disable-gpu')             # todo 谷歌文档提到需要加上这个属性来规避bug
            driver = webdriver.Chrome(options=option)
    return driver
