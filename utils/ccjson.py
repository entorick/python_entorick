import json


class CCJson:

    def two_dimension(self, json_str):
        ret_dct = {}
        if isinstance(json_str, str):
            json_str = json.loads(json_str)

        if isinstance(json_str, list):
            ret_dct.update(self.handle_lst(j_lst=json_str, pre_key=''))

        if isinstance(json_str, dict):
            ret_dct.update(self.handle_dct(j_dct=json_str, pre_key=''))

        return ret_dct

    def handle_lst(self, j_lst: list, pre_key: str) -> dict:
        ret_dct = {}
        idx = 0
        for v in j_lst:
            key = [pre_key, str(idx)] if pre_key != '' else [str(idx)]
            key = '|'.join(key)
            if isinstance(v, list):
                ret_dct.update(self.handle_lst(j_lst=v, pre_key=key))
            elif isinstance(v, dict):
                ret_dct.update(self.handle_dct(j_dct=v, pre_key=key))
            else:
                ret_dct.update({key: v})
            idx += 1
        return ret_dct

    def handle_dct(self, j_dct: dict, pre_key: str) -> dict:
        ret_dct = {}
        for k, v in j_dct.items():
            key = [pre_key, k] if pre_key != '' else [k]
            key = '|'.join(key)
            if isinstance(v, list):
                ret_dct.update(self.handle_lst(j_lst=v, pre_key=key))
            elif isinstance(v, dict):
                ret_dct.update(self.handle_dct(j_dct=v, pre_key=key))
            else:
                ret_dct.update({key: v})

        return ret_dct


if __name__ == '__main__':
    json = {
        'a': 'b',
        'c': {
            'xx1': 123,
            'xx2': 345,
            'xx3': [
                {
                    'yy1': 123,
                    'yy2': 345
                },
                {
                    'yy1': 1223,
                    'yy2': 456
                }
            ],
            'xx4': {
                'zz1': 123,
                'zz2': 435
            }
        }
    }
    x = CCJson()
    for k, v in x.two_dimension(json_str=json).items():
        print(f"{k}:{v}")

    json = [{
        'a': 'b',
        'c': {
            'xx1': 123,
            'xx2': 345,
            'xx3': [
                {
                    'yy1': 123,
                    'yy2': 345
                },
                {
                    'yy1': 1223,
                    'yy2': 456
                }
            ],
            'xx4': {
                'zz1': 123,
                'zz2': 435
            }
        }
    }]
    x = CCJson()
    for k, v in x.two_dimension(json_str=json).items():
        print(f"{k}:{v}")
