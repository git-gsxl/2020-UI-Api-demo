def ele_login(user='admin', pwd="123456", exp_name="admin"):
    """todo 打开登录页→输入账号密码→点击登录→断言exo_bane→是否退出登录"""
    yield ("open",
           "/api/login/")
    yield ("send", user,
           'id', 'account')
    yield ("send", pwd,
           'id', 'password')
    yield '//*[@id="login_submit"]'
    yield ("txt_in_ele", exp_name,
           '/html/body/div[2]/div[1]/div[1]')
    yield '/html/body/div[2]/div[1]/div[1]/a'


def ele_register(user='gsxl11', pwd1='gsxl12', pwd2='gsxl12', email='gsxl11@gmail.com'):
    """todo 打开注册页-输入账号密码、确认密码、邮箱-点击注册 """
    yield ("open",
           "/api/register/")
    yield ("send", user,
           '//*[@id="account"]')
    yield ("send", pwd1,
           '//*[@id="password"]')
    yield ("send", pwd2,
           '//*[@id="repassword"]')
    yield ("send", email,
           '//*[@id="email"]')
    yield '//*[@id="register_form"]/div[5]/input'
