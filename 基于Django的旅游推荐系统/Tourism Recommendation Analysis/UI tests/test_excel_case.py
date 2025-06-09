from pathlib import Path

from commons.excel_utils import read_case
from commons.case_urtils import make_pytest_case
import logging

logger = logging.getLogger(__name__)

g_vars = globals()  # 全局变变量
case_dir = Path('tests/excel_case')  # 1. 指定目录

excel_path_list = list(case_dir.glob('test_*.xlsx'))  # 2. 搜集所有test_开头的xlsx文件

for excel_path in excel_path_list:  #

    case = read_case(excel_path)  # 3.动态的读取excel用例

    case_name = 'test_' + case['name']  # 变量名 == 用例名，是动态拼接的
    g_vars[case_name] = make_pytest_case(case)
