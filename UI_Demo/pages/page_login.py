import time
from common import base, driver
from elements import elem_login

ele = elem_login


class Login(base.Base):

    def login_page(self, user="admin", pwd="123456", exp="admin", out=0):
        loops = ele.ele_login(user, str(pwd), exp)
        self.loop(loops, 4)
        time.sleep(1)
        res = self.step(next(loops, None))
        if res and out == 1:
            self.step(next(loops, None))
            return True
        else:
            return False

    def register(self, user='gsxl11', email='gsxl11@gmail.com', pwd1='gsxl12', pwd2='gsxl12'):
        ''' 注册账号 '''
        loops = ele.ele_register(user, pwd1, pwd2, email)
        self.loop(loops, 5)
        time.sleep(0.2)             # 操作太快，缓一缓
        self.step(next(loops, None))
        if self.is_alert():
            print('弹窗处理：确定')
        time.sleep(0.2)  # 操作太快，缓一缓
        # 注册成功后会回到登录页，所以断言title是否是登录即可
        if self.driver.title == '登录':
            return True
        else:
            return False


if __name__ == '__main__':
    driver = driver.is_driver()
    b = Login(driver)
    print(b.login_page())
    # print(b.register())
    # driver.quit()
