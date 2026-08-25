# test_buggy.py
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.buggy import add_numbers, multiply_numbers, divide_numbers

def test_add_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0, 0) == 0
    assert add_numbers(100, 200) == 300

def test_multiply_numbers():
    assert multiply_numbers(2, 3) == 6
    assert multiply_numbers(-2, 3) == -6
    assert multiply_numbers(0, 5) == 0
    assert multiply_numbers(7, 7) == 49

def test_divide_numbers():
    assert divide_numbers(6, 3) == 2.0
    assert divide_numbers(5, 2) == 2.5
    assert divide_numbers(-10, 2) == -5.0
    assert divide_numbers(0, 5) == 0.0

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)
