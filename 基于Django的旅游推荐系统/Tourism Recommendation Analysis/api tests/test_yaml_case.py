from pathlib import Path

import logging
import pytest
import allure

from commons.model_util import verify_case, ddt_case, flow_case
from commons.to_python import by_yaml
from commons.request_utils import RequestUtils
from commons.extract_utils import verify_resp, extract_by_re, extract_by_jsonpath, g_var, use_vars
from commons.hotload_utils import use_funcs
from commons.assert_utils import assert_all

logger = logging.getLogger("case")

case_list = []

case_dir = Path('tests/yaml_case')  # 1. 指定目录，而不是指定文件

yaml_path_list = list(case_dir.glob("test_*.yaml"))  # 2.1 从目录中搜索文件，并且返回列表

# print(yaml_path_list)

# 调用列表方法自动排序

yaml_path_list.sort()  # 递增排序，数字越小，越靠前
# yaml_path_list.reverse()  # 递减排序，数字越大，越靠前


for yaml_path in yaml_path_list:  # 2.2 从列表中读取yaml路径
    logger.info(f'正在加载yaml文件:{yaml_path}')
    data = by_yaml(yaml_path)  # 3. 读取内容

    if isinstance(data, list):  # 流程用例
        case = flow_case(data)
        case_list.append(case)
    elif data.get('parametrize'):  # 数据驱动用例
        ddt_case_list = ddt_case(data)  # 返回列表
        case_list.extend(ddt_case_list)
    else:
        case = verify_case(data)  # 4.验证格式
        case_list.append(case)  # 单接口用例

case_list.sort(key=lambda case: case.order)

case_ids = []
for case in case_list:
    case_name = case.name
    case_ids.append(case_name)



@pytest.mark.parametrize(
    "case",
    case_list,  #列表：用例参数
    ids=case_ids,  # 列表：用例名称
)
def test_api(case):
    allure.dynamic.epic('码尚自动化测平台')
    allure.dynamic.feature(case.feature)
    allure.dynamic.story(case.story)
    allure.dynamic.title(case.name)

    # 对于流程用例，每个接口都请求（使用for循环）
    # 对于非流程用例，只会请求一个接口

    if case.flow_list:  # 流程用例
        logger.info('这是流程用例')
        flow_list = case.flow_list  # 使用列表
    else:  # 非流程用例
        logger.info('这是非流程用例')
        flow_list = [case]  # 创作列表

    for temp_case in flow_list:
        new_request = use_funcs(use_vars(temp_case.request))
        resp = RequestUtils().send_request(**new_request)
        resp = verify_resp(resp)

        for var_name, var_args in temp_case.extract.items():
            if var_args[0] in ['headers', 'json']:
                extract_by_jsonpath(resp, var_name, *var_args)
            else:
                extract_by_re(resp, var_name, *var_args)


        validate = use_funcs(use_vars(temp_case.validate))
        assert_all(validate)
