# coding=utf8
"""
Label 文字标签
Button n按钮
"""

from base import *
from frame import *
from label import Label
from button import Button, TextButton
import utils


def _(value):

    if isinstance(value, unicode):
        return value.encode("utf-8")
    return value
