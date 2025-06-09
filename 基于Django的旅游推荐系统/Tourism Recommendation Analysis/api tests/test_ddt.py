import pytest
import yaml


def add(a, b):
    return a + b


with open(r"data/ddt_data.yaml", encoding="utf-8") as f:
    s = f.read()  # 字符串
    data_yaml = yaml.safe_load(s)  # 数据


@pytest.mark.parametrize(
    "a, b, c",
    data_yaml
)
def test_add(a, b, c):
    assert add(a, b) == c


with open(r"data/data.yaml", encoding="utf-8") as f:
    s = f.read()  # 字符串
    data_yaml = yaml.safe_load(s)  # 数据


@pytest.mark.parametrize(
    "s",
    data_yaml
)
def test_add_str(s):
    pass
