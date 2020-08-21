import time
from common.base import Base
from elements import elem_home

ele = elem_home


class Home(Base):

    def add_projects(self, project_name='hrun', responsible_name=u'小龙', test_user=u'广深小龙、漂亮的小姐姐', dev_user=u'程序猿、程序媛'):
        ''' 新增项目 '''
        add = ele.add_projects(project_name, responsible_name, test_user, dev_user)
        self.loop(add, 8)
        jop = next(add, None)
        txt = self.get_text(jop)
        if txt:
            self.step(jop)
            return False
        else:
            return True

    def del_project(self):
        loops = ele.del_project()
        self.loop(loops, 3)
        loc_exp = next(loops, None)
        exp = self.step(loc_exp)
        self.refresh()
        time.sleep(0.5)
        res = self.step(loc_exp)
        time.sleep(0.5)
        if res != exp:
            return True
        else:
            return False


if __name__ == '__main__':
    from common.driver import is_driver
    from pages.page_login import Login

    driver = is_driver()
    Login(driver).conftest_login()
    b = Home(driver)
    # print(b.add_projects())
    print(b.del_project())
    # driver.quit()
