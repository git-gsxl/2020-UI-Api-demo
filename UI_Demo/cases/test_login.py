import allure
from pages.page_login import Login
from elements import elem_login
from common.sql import send_sql

ele = elem_login


@allure.feature("hrun登录模块")
class TestLogin:
    """ 这是登录模块，包含登录、注册 """

    def setup_class(self):
        sql = "delete from UserInfo where username='gsxl11';"
        send_sql(sql)

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("输入【正确】的账号密码登录")
    def test_login1(self, driver):
        """ 1.在登录页中输入【正确】的账号密码
            2.点击登录，该用例正常能登录成功
        """
        res = Login(driver).login_page(out=1)
        assert res

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("输入【错误】的账号密码登录")
    def test_login2(self, driver):
        """ 1.在登录页中输入【错误】的账号密码
            2.点击登录，登录不成功
        """
        res = Login(driver).login_page(user="admin111", out=1)
        assert res is False

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("输入【空账号密码】点击登录")
    def test_login3(self, driver):
        """ 1.在登录页中输入【空账号密码】
            2.点击登录，该用例不能登录成功
        """
        res = Login(driver).login_page(user="", pwd="", out=1)
        assert res is False

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("正常注册账号，注册成功！")
    def test_register1(self, driver):
        """ 1.在注册页中输入【账号/密码/邮箱】
            2.点击注册，该用例注册成功
        """
        res = Login(driver).register()
        assert res

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("正常注册账号，注册失败！")
    def test_register2(self, driver):
        """ 1.在注册页中输入【账号/密码/邮箱】
            2.点击注册，该用例注册失败
        """
        res = Login(driver).register(user='admin')
        assert res is False


