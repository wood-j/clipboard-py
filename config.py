import json
import os
from common.jsonn import JsonSerializable
from common.paths import get_data_root


class Config(JsonSerializable):
    def __init__(self):
        self.server_setting = ServerSetting()

    def load_dict(self, dic: dict):
        super(Config, self).load_dict(dic)
        content = dic.get('server_setting', None)
        if content:
            setting = ServerSetting()
            setting.load_dict(content)
            self.server_setting = setting

    @classmethod
    def load(cls):
        root = get_data_root()
        path = os.path.join(root, 'config.json')
        dic = {}
        if os.path.exists(path):
            with open(path, 'r') as f:
                dic = json.load(f)
        result = Config()
        result.load_dict(dic)
        return result

    def save(self):
        root = get_data_root()
        path = os.path.join(root, 'config.json')
        if not os.path.exists(root):
            os.makedirs(root)
        with open(path, 'w') as f:
            js = self.dump_json()
            f.write(js)


class ServerSetting(JsonSerializable):
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 10000


if __name__ == '__main__':
    conf = Config()
    conf.save()
    conf = Config.load()
    pass
