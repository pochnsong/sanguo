# coding = utf-8
from __future__ import unicode_literals
import codecs
import json


def load_json_file(path):

    with codecs.open(path, 'r', "utf-8") as rf:
        dat = rf.read()
        res = json.loads(dat)

    return res


def save_json_file(path, values):
    with codecs.open(path, 'w', 'utf-8') as wf:
        dat = json.dumps(values)
        wf.write(dat)
