# -*- coding: utf-8 -*-
import json
from datetime import datetime, date, time
from common.log import logger


class JsonSerializable(object):
    def dump_json(self):
        # return json.dumps(self, indent=4, ensure_ascii=False, cls=DefaultEncoder)
        dic = self.dump_dict()
        return json.dumps(dic, indent=4, ensure_ascii=False, cls=DefaultEncoder)

    def dump_dict(self):
        # return self.__dict__
        def recurse_dic(dic: dict):
            for key, value in dic.items():
                if isinstance(value, JsonSerializable):
                    dic[key] = value.dump_dict()
                elif isinstance(value, (list, tuple)) and value:
                    first = value[0]
                    if isinstance(first, JsonSerializable):
                        dic[key] = [x.dump_dict() for x in value]
                elif isinstance(value, dict) and value:
                    dic[key] = recurse_dic(value)
            return dic

        dic = recurse_dic(self.__dict__)
        return dic

    def load_dict(self, dic: dict):
        for key, value in dic.items():
            if not hasattr(self, key):
                logger.warning(f'"JsonSerializable" load from dict skip unexpected property name: {key}')
                continue
            setattr(self, key, value)


class DefaultEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field, datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field, date):
            return field.strftime('%Y-%m-%d')
        elif isinstance(field, time):
            return field.strftime('%H:%M:%S')
        elif isinstance(field, JsonSerializable):
            return field.dump_dict()
        elif hasattr(field, '__dict__'):
            return field.__dict__
        else:
            return json.JSONEncoder.default(self, field)


class SampleChild(JsonSerializable):
    def __init__(self):
        self.child_name = 'child'
        self.date = datetime.now().date()
        self.time = datetime.now().time()


class Sample(JsonSerializable):
    def __init__(self):
        self.text = 'sample'
        self.date = datetime.now().date()
        self.time = datetime.now().time()
        self.default_child = SampleChild()
        self.child_tuple = (
            SampleChild(),
            SampleChild(),
            SampleChild(),
        )
        self.child_list = [
            SampleChild(),
            SampleChild(),
            SampleChild(),
        ]
        self.child_dic = {
            '1': SampleChild(),
            '2': SampleChild(),
            '3': SampleChild(),
        }


if __name__ == '__main__':
    sample = Sample()
    js = sample.dump_json()
    logger.debug(js)
    pass
