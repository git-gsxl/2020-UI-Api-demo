import os
import pytest
import sys

cur_path = os.path.dirname(os.getcwd())
sys.path.append(cur_path)
from common.base import Api
from common.sql import send_sql
r = "r.yaml"


@pytest.mark.parametrize("data", Api.cases_datas())
def test_all(data: dict):
    assert_datas = data.pop('validators')
    res = Api().send(data=data)
    Api().assertion(
        data=assert_datas,
        result=res)


def setup_module():
    isfile = os.path.isfile(r)
    if isfile:
        os.remove(r)


def teardown_module():
    sql = "delete from UserInfo where username='gsxl11';"
    send_sql(sql)
    isfile = os.path.isfile(r)
    if isfile:
        os.remove(r)
