import pytest
import allure
import time
from pages.page_home import Home


@allure.feature("hrun添加项目模块")
class TestHome:

    @allure.story("添加【正常】的项目")
    def test_add1(self, login):
        """ 1.添加项目
            2.点击新增，该用例正常能添加项目成功
        """
        res = Home(login).add_projects()
        assert res is False

    @allure.story("添加【重复】的项目")
    def test_add2(self, login):
        """ 1.添加项目
            2.点击新增，该用例不能添加项目成功，名称重复
        """
        res = Home(login).add_projects(project_name="广深小龙")
        assert res is False

    @allure.story("添加【正常】的项目")
    def test_add3(self, login):
        """ 1.添加项目，输入其它值
            2.点击新增，该用例正常能添加项目成功
        """
        res = Home(login).add_projects(
            project_name=str(time.strftime('%Y-%m-%d %H-%M-%S')),
            responsible_name=u'泡泡龙哈哈',
            test_user=u'广深小龙、漂亮的小姐姐',
            dev_user=u'程序猿、程序媛')
        assert res

    @allure.story("【正常删除】的项目")
    def test_del(self, login):
        """ 1.正常删除，第一个项目
            2.点击删除，该用例正常能删除项目成功
        """
        res = Home(login).del_project()
        assert res
