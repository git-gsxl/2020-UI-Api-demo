** UI自动化简介 **

**重点：元素传参方式(单个/多个)**

一、单个定位：
	
	打开网页连接：loc=("open", "/url/xxlogin")
	
	(程序会根据配置文件config.yaml的host拼接url，如：host/url/xxlogin)
	
	点击：
	
		click：loc="#s-top-left"
		
		click：loc=("id", "s-top-left")
	
	输入：
	
		send： loc=("send", "广深小龙", "#kw") 
		
		send： loc=("send", "广深小龙", "id", "kw")
	
	清空：
		clear： loc=("clear", "#kw")  
		
		clear： loc=("clear", "id", "kw")  
	
	获取元素是否存在：（返回布尔值）
	
		get_ele： loc=("get_ele", "#su") 
		
		get_ele： loc=("get_ele", "id", "su") 
		
	获取元素的文本值：
		
		get_txt：loc=("get_txt", "#s-usersetting-top")
		
		get_txt：loc=("get_txt", "id", "s-usersetting-top")
		
	文本在元素文本值：（部分匹配返回布尔值）
		
		txt_in_ele：loc=("txt_in_ele", "设置", "#s-usersetting-top")   
		
		txt_in_ele：loc=("txt_in_ele", "设置", "id", "s-usersetting-top")
	
	
二、复数定位：

	点击：

		clicks：loc=("0", "#s-top-left") 
		
		clicks：loc=("0", "id", "s-top-left")
	
	输入：
	
		sends： loc=("sends", "广深小龙", "0", "#kw") 
		
		sends： loc=("sends", "广深小龙", "0", "id", "kw")
		
	清空：
	
		clears：loc=("clears", "0", "#kw")  
		
		clears：loc=("clears", "0", "id", "#kw")  


	获取元素是否存在：
	
		get_eles： loc=("get_eles", "0", "#su")
		
		get_eles： loc=("get_eles", "0", "id", "su")
		
	获取元素的文本值：
		
		get_txts：loc=("get_txts", "0", "#s-usersetting-top")
		
		get_txts：loc=("get_txts", "0", "id", "s-usersetting-top")	

三、其它说明


步骤1：(配置文件)

	1. config. yaml 配置好 host (其它配置一般不用动)
	
	2. config. yaml设置 default 定位方式，可自行喜欢设置；


步骤2：(元素定位及方式)

	1.  elements文件夹下新建：ele_login. py文件
	
		用哪种方式看自己喜欢，命名也可以其它命名，注意别与其它模块重复就可。
		
		建议元素写成流程的方式：yield 迭代器接收，让loop方法循环处理操作事件。
	

步骤3：(页面流程编写)

	1.  pages 文件夹下新建：页面文件，如page_login. py
	
	2. 导入基础类Base，让登录的类继承
	
	3.  导入编写元素的类或方法，供页面操作使用
	
	4. 编写操作/输入页面的流程
	
	注意：最好在当前模块下调试封装好的登录或其它流程是否正常
	

步骤4：(基于页面流程组装测试数据)

	1. 导入页面流程的模块：from pages. page_login import Login
	
	2. 导入driver：from common. driver import is_driver
	
	3. setup_class、teardown_class分别为用例执行的前置与后置
		
		前置：driver 驱动打开浏览器
		
		后置：关闭浏览器
		
	4. allure装饰器是用来加入报告中的一些描述之类的，可参考report连接里面的写法
	
	5. 这里的流程基本是：调用页面流程，输入不一样的参数进行测试
	
	6. 补充：比如新增项目测试，那么需要先登录，这里是这样，在用例传入login方法即可，既是先登录成功后，返回driver驱动，给予后面所需传入
	

步骤5：(命令行运行)
	
	1.  打开到用例文件的目录
	
	2.  命令行输入：pytest(会执行目录下所有符合规则的文件，如test_login. py，所以我们用例需要命名为test_xx开头)
	
	3. 命令行输入： pytest test_login. py（单个文件执行）
	
	
步骤6：(查看报告)
	
	1. 直接打开report目录下可直接查看简陋报告
	
	2. allure报告需更多配置或学习，请参考【项目目录简介】中生成allure报告或者自行百度
	
	allure示例链接：http://47.97.194.84:8085
	

** 基类方法简介：**

    0. find：单个元素定位：locator = ("id", "id值")
	
    1. finds：复数元素定位：locator = ("id", "id值")[x]，取第几个？
	
    2. send：文本输入
	
    3. click：点击操作
	
    4. clear：清空文本
	
    5. text_in_enement：判断 _text 文本值是否 in 定位元素中，返回 bool 值
	
    6. text_in_enement：
	
    7. get_enement：判断元素是否存在，返回 bool 值
	
    8. get_text：获取元素的文本值
	
    9. now_title：获取当前页面的 title
	
    10. move_element：鼠标悬停操作，传locator
	
    11. select_index：index是索引定位第x个，从0开始，默认第1个
	
    12. select_value：select中的value方法，如html中：value="50"，则value传：50
	
    13. select_text：select中的text方法全匹配文本，如html中显示：每页显示50条，则文本需全部匹配
    
	14. switch_iframe：切换iframe：传下标 或 locator
    
	15. is_alert：
            alert弹窗处理_text：
            --1. 默认点击：确定
            --2. 取消操作传：取消
            --3. 获取弹窗文本传：text
            --4. 弹出输入文本传：输入 + 文本值
    
	16. switch_handle：句柄切换，传int类型，从0开始，-1既是最新打开的一个
    
	17. js_top：页面滚动条滑动至顶部
   
    18. js_element：聚焦元素位置,传locator
    
	19. js_tail：页面滚动条滑动至底部
	
    20. screenshot：截图
	
    21. yaml_load：读取yaml文件
	
    22. get：输入打开网址
	
	23. open：输入打开网址
	
	24. quit：关闭浏览器
	
	25. refresh：刷新页面
	
	26. del_cookie：清空缓存
	
	27. location：单个定位，提供step方法调用
	
	28. locations：复数定位，提供step方法调用
	
	29. handle：传参step方法带过来的参数，判断执行
	
	30. step：传参处理，使用这种方式必须按照规则传参
	
	31. loop：循环处理元素操作事件

conftest.py 已封装发生异常截图目录：report/screenshot，以及将截图放入简陋测试报告中；

**登录例子：**
	
	**elements**：登录的元素编写(前面4步骤是登录，5：断言，6：是否退出登录的元素)
	
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
	
	**pages**：运行前面4步骤：self.loop(loops, 4)，默认参数登录成功（5：断言，返回布尔值，6：如果out=1登录成功就退出）
	
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
	
如有其它疑问，欢迎联系广深小龙！！！QQ交流群：482713805

个人博客：https://www.cnblogs.com/gsxl/	

github：https://github.com/git-gsxl