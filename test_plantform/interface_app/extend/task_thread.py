import json
import os
import threading
from os.path import dirname, abspath
from time import sleep
from xml.dom import minidom
from interface_app.apps import TASK_PATH, RUN_TASK_FILE
from interface_app.models import TestTask, TestCase, TestResult

class TaskThread:
    """
    多线程运行测试任务
    """
    def __init__(self, task_id):
        self.tid = task_id


    def run_cases(self, tid):
        """
        运行测试任务
        :param tid:
        :return:
        """
        task = TestTask.objects.get(pk=tid)
        case_id_list = task.cases.split(",")
        # print(case_id_list)

        # 将任务状态更新为执行中
        task.status = 1
        task.save()

        # 循环读取testcase，添加到测试数组准备文件中
        case_file = {}
        for case_id in case_id_list:
            testcase = TestCase.objects.get(pk=case_id)
            case_dict = {
                "url": testcase.url,
                "method": testcase.req_method,
                "type_": testcase.req_type,
                "header": testcase.req_header,
                "parameter": testcase.req_parameter,
                "assert_": testcase.response_assert
            }
            case_file[case_id] = case_dict
        cases_str = json.dumps(case_file)

        file_name = "case_data.json"
        test_data_file = TASK_PATH + file_name

        # 读取测试数据，保持到文件中
        with open(test_data_file, "w+") as f:
            f.write(cases_str)

        # 运行测试用例
        os.system("python3 " + RUN_TASK_FILE)

        sleep(2)
        print("测试任务运行完成后，开始收集测试数据。。。")
        # 更新任务运行状态
        task.status = 2
        task.save()

        # 保存测试结果
        self.save_result()

    def run_thread(self):
        """
        多线程实现异步运行
        :return:
        """
        threads = []
        t = threading.Thread(target=self.run_cases, args=(self.tid,))
        threads.append(t)

        # 运行进程
        for t in threads:
            t.start()

        # 守护进程
        # for t in threads:
        #     t.join()

    def save_result(self):
        """
        保存测试结果
        :return:
        """
        dom = minidom.parse(TASK_PATH + "results.xml")
        root = dom.documentElement
        ts = root.getElementsByTagName("testsuite")
        # 读取结果值
        name = ts[0].getAttribute("name")
        errors = ts[0].getAttribute("errors")
        failures = ts[0].getAttribute("failures")
        skipped = ts[0].getAttribute("skipped")
        tests = ts[0].getAttribute("tests")
        run_time = ts[0].getAttribute("time")

        with open(TASK_PATH + "results.xml", "r", encoding="utf-8") as f:
            result_text = f.read()
            # print("type result :", type(result_text))

        # 获取关联的测试任务
        task = TestTask.objects.get(id=self.tid)

        # 保存测试结果
        task_result = TestResult.objects.create(
            name=name,
            task=task,
            errors=errors,
            failures=failures,
            skipped=skipped,
            tests=tests,
            run_time=run_time,
            result=result_text
        )

        if task_result is None:
            print("测试结果保存失败！")
        else:
            print("测试结果保存成功！")