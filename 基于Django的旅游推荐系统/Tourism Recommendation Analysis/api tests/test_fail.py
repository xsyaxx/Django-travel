import random


def test_fail():
    n = random.randint(0, 9)

    assert n == 4  # 1/10的成功概率
