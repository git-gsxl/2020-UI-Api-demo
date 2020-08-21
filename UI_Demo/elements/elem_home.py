def add_projects(
        project_name='hrun', responsible_name=u'小龙', test_user=u'广深小龙、漂亮的小姐姐', dev_user=u'程序猿、程序媛'):
    ''' 新增项目 9个步骤 '''
    yield '/html/body/div[2]/div[1]/div[2]/ul[1]/li[2]/a'   # 点击 新增项目
    yield ("send", project_name,
           '//*[@id="project_name"]')                       # 输入 项目名称
    yield ("send", responsible_name,
           '//*[@id="responsible_name"]')                   # 输入 负责人
    yield ("send", test_user,
           '//*[@id="test_user"]')                          # 输入 测试人员
    yield ("send", dev_user,
           '//*[@id="dev_user"]')                           # 输入 开发人员
    yield ("send", '测试的发布应用',
           '//*[@id="publish_app"]')                        # 输入 发布应用
    yield ("send", "这是小龙和妹子一起努力的成果",
           '//*[@id="simple_desc"]')                        # 输入 简要描述
    yield ("send", "我可以不写吗",
           '//*[@id="other_desc"]')                         # 输入 其他信息
    yield '//*[@id="add_project"]/div[8]/div/button'        # 弹窗 点击提交
    yield '//*[@id="my-alert"]/div/div[3]/span'             # 弹窗 点击确定


def del_project():
    yield ("open",
           "/api/project_list/1/")
    yield '//*[@id="project_list"]/table/tbody/tr[1]/td[9]/div/div/button[3]/span'      # 点击 删除
    yield '//*[@id="my-invalid"]/div/div[3]/span[2]'                                    # 点击  确定
    yield ("get_txt",
           '//*[@id="project_list"]/table/tbody/tr/td[4]')                              # 点击 删除断言
