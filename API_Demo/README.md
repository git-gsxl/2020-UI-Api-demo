**一、简介：**

框架：python3 + request + pytest + yaml + faker

1、host域名配置，config.yaml文件 host: www.xxx.com； 

2、request默认是post请求(如需get请求则写：method: get)；

3、xpath：存取你要的值，用来参数化关联(列表形式)写法："$..dict"
    
    json写法："$..dictid"
    
    re写法：{"re", "dictid", "invalidxx('(.+?)'\xx)"}

4、支持多个yaml文件的测试用例执行(指定某个yaml文件待实现)；
   
5、pytest.ini 默认值：addopts = -s --html=../report/report.html

6、注意json、data的格式，该是什么写什么，例1，json: xxx  例2，data:current=1&size=9999&type=2

7、validators：多个断言
	
    check：   因返回的是result对象，如填写 status_code -->等价于 result.status_code
    selector：断言方式，例1填写==，则exp == xx，例2填写len，则exp == len(xx)
    exp：     断言您的期望的结果

8、引用变量

    xpath变量：意思是你自己存的参数，比如存了token，则这样引用：${token}
    
    系统随机变量(faker随机生成)：则这样引用：ppl{xxx}，其中xxx为faker的方法，官方请参考：https://faker.readthedocs.io/en/master/locales/zh_CN.html
    
    faker常用部分示例：
        1.随机名字：ppl{name}
            返回结果：苏丽丽
            
        2.随机地址：ppl{address}
            返回结果：北京市建平市南长贾路K座 324786
            
        3.返回随机邮箱：ppl{email}
            返回结果：zhutao@hotmail.com
            
        4.返回随机网址：ppl{uri}
            返回结果：http://82.cn/wp-content/categories/main.html
        
        5.返回当前日期与时间：ppl{date_time_between_dates}
            返回结果：2020-08-01 20:02:12
          返回当前日期：date_between_dates
            返回结果：2020-08-01
            
        6.返回随机日期：ppl{date}
            返回结果：2020-08-01
            
        7.返回随机手机号码：ppl{phone_number}
            返回结果：13815429659
            
        8.返回随机身份证号码：ppl{ssn}
            返回结果：130205195901209552
    
**yaml编写测试用例：**

例子：	

    - url: /xxxx/login
      json: {"account":"xxxxxxx","pwd":"xxxxx"}
      xpath: 
	    - "$..token"
        - {"re", "token22", "invalidxx('(.+?)'xx)"}
      validators:
        - {"check": "status_code", "selector": "==", "exp": "200"}
        - {"check": "headers", "selector": "in", "exp": 'application/json'}
        - {"check": "json()", "selector": "len", "exp": "5"}
        - {"check": "json()['data']['customerName']", "selector": "==", "exp": "泡泡龙"}
        - {"check": "text", "selector": "in", "exp": "泡泡龙"}
	    - {"check": "text", "selector": "not in", "exp": "广深小龙"}
	    
    - url: /vip/xxx
      json: {"phone":"ppl{phone_number}","pwd":"xxxxxxx","token":"$token"}
      xpath: "$..jsonpath"
      validators:
        - {"check": "status_code", "selector": "==", "exp": "200"}
        - {"check": "text", "selector": "not in", "exp": "广深小龙"}
	  
    - url: xxx/xxx
      method: get
      headers:
        authToken: ${token22}
      data: ppl{name}
      validators:
        - {"check": "status_code", "selector": "==", "exp": "200"}
        - {"check": "text", "selector": "not in", "exp": "广深小龙"}

如有其它疑问，欢迎联系广深小龙！！！QQ交流群：482713805

个人博客：https://www.cnblogs.com/gsxl/
	
github：https://github.com/git-gsxl
