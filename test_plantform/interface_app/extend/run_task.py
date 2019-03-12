import json
import unittest
from os.path import dirname, abspath

import requests
import xmlrunner
from ddt import ddt, data, file_data, unpack

BASE_PATH = dirname(dirname(dirname(abspath(__file__)))).replace("\\", "/")
# 测试任务地址
TASK_PATH = BASE_PATH + "/resource/tasks/"
# 测试文件路径
CASE_FILE_PATH = TASK_PATH + "case_data.json"

# 把变量添加到系统环境变量中
# sys.path.append(BASE_PATH)


@ddt
class RunTask(unittest.TestCase):
    @unpack
    @file_data(CASE_FILE_PATH)
    def test_case_file(self, url, method, type_, header, parameter, assert_):
        # print("url", url)
        # print("method", method)
        # print("type_", type_)
        # print("header", header)
        # print("parameter", parameter)
        # print("assert_", assert_)

        if method.upper() == "GET":   # get请求
            r = requests.get(url, params=json.loads(parameter), headers=json.loads(header))
        elif method.upper() == "POST":  # post请求
            if type_ == "form-data":
                r = requests.post(url, data=json.loads(parameter), headers=json.loads(header))
            else:
                r = requests.post(url, json=parameter, headers=json.loads(header))
        elif method.upper() == "PUT":
            r = requests.put(url, data=json.loads(parameter))
        elif method.upper() == "DELETE":
            r = requests.delete(url)
        elif method.upper() == "HEAD":
            r = requests.head(url)
        elif method.upper() == "OPTION":
            r = requests.options(url)

        # print(r.status_code)
        # print(r.text)
        # 断言
        self.assertIn(assert_, json.dumps(r.text))


# 运行测试用例
def run_case():
    with open(TASK_PATH + 'results.xml', 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)


if __name__ == '__main__':
    run_case()
