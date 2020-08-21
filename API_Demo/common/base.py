import re
import yaml
import os
import time
import logging
import requests
from faker import Faker
from jsonpath import jsonpath
s, faker, now_date = requests.session(), Faker("zh_CN"), time.strftime('%Y-%m-%d')  # todo s保持cookie、faker随机数据


class Api:
    def __init__(self):
        self.host = self.yaml_load("../config.yaml").get("host")

    @staticmethod
    def yaml_load(path):
        try:
            with open(path, encoding="utf-8") as f:
                return yaml.safe_load(f)
        except:
            logging.error("请检查 r.yaml 文件目录或格式是否正确")

    @staticmethod
    def cases_datas():
        # todo 读取测试yaml数据
        cases_yaml = os.path.join(os.path.dirname(os.getcwd()), "cases")
        yaml_list = []
        for name in os.listdir(cases_yaml):
            if ".yaml" in name:
                yaml_list.append(os.path.join(os.path.dirname(os.getcwd()), "cases", name))

        all_data = []
        for data in yaml_list:
            all_data.append(Api.yaml_load(data))

        all_data_list = []
        for all_datas in all_data:
            for data in all_datas:
                all_data_list.append(data)
        return all_data_list

    @classmethod
    def json_path(cls, path, r=None):
        if r:
            return jsonpath(r, path)
        else:
            return logging.warning("jsonpath：返回格式错误")

    def send(self, data: dict, rel_path="r.yaml"):
        raw = yaml.dump(data)
        rel_file = os.path.isfile(rel_path)
        if rel_file:
            rel_data = self.yaml_load(rel_path)
            if rel_data:
                for k in rel_data:
                    raw = raw.replace(("${%s}" % k), str(rel_data[k]))

        re_ppl = re.findall("ppl{(.+?)}", raw)
        for ppl in re_ppl:
            try:
                if "now_date" in ppl:
                    res_txt = str(now_date)
                else:
                    res_txt = str(eval("faker.%s()" % ppl))
                raw = raw.replace("ppl{%s}" % ppl, res_txt)
            except:
                logging.error("Faker语法错误:【%s】，方法请查看：https://faker.readthedocs.io/en/master/locales/zh_CN.html" % ppl)

        data = yaml.load(raw)
        # todo: 如果 r.yaml 中 method 为空，默认为 post 请求
        if data.get('method'):
            method = data.pop('method')
        else:
            method = 'post'

        # todo: 如果 r.yaml 中 xpath 存在，那么存取它
        if data.get('xpath'):
            xpaths = data.pop('xpath')
        else:
            xpaths = False

        # todo: request拼装发送请求
        result = s.request(
            method=method,
            url=self.host + data.pop('url'),
            **data)
        if xpaths:
            with open(rel_path, "a", encoding="utf-8")as f:
                for xpath in xpaths:
                    if isinstance(xpath, str):
                        try:
                            extract = self.json_path(xpath, result.json())[0]
                            write_data = xpath[3:] + ": " + str(extract) + "\n"
                            f.write(write_data)
                        except:
                            logging.warning("注意：result.json()语法错误或json格式错误：%s" % xpath)
                    else:
                        result_text = result.content.decode("utf-8")
                        dic_k = xpath.get("re")
                        k = None
                        for i in dic_k:
                            k = i
                        try:
                            re_data = re.findall(dic_k[k], result_text)[0]
                            write_re_data = str(k) + ": " + str(re_data) + "\n"
                            f.write(write_re_data)
                        except:
                            logging.warning("注意：re匹配错误返回列表为空，请检查正则语法：%s" % xpath)
        return result

    @classmethod
    def assertion(cls, data: dict, result):
        # todo 多个断言封装
        for i in data:
            selector = i['selector']
            exp = i['exp']

            if i.get("check"):
                check = i['check']
            else:
                check = "text"
            result_res = eval("result.%s" % check)
            if selector in ["eq", "equals", "==", "is", "="]:
                assert str(exp) == str(result_res)
            elif selector in ["in"]:
                assert str(exp) in str(result_res)
            elif selector in ["len"]:
                assert str(exp) == len(result_res)
            elif selector in ["not", "not in"]:
                assert str(exp) not in str(result_res)
            else:
                logging.error("selector 格式错误,请使用eq/in/len等方式进行")
