import pytest

@pytest.fixture()
def done():
    print('done')


def test_1(done):
    assert 1==1


def test_2(done):
    assert 1 == 2

@pytest.mark.skip
def test_3(done):
    pass

@pytest.fixture()
def f():
    assert  1==2

def test_4(done,f,):
    pass
