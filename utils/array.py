import copy
from functools import reduce

from utils import string

################################################################################
### data point
################################################################################

class Point(object):
    def __init__(self, d, k):
        self.d = d
        self.k = k

    def get(self):
        return self.d[self.k]

    def set(self, v):
        self.d[self.k] = v

    def update(self, v):
        self.d[self.k].update(v)

    def append(self, v):
        self.d[self.k].append(v)

    def extend(self, v):
        self.d[self.k].extend(v)

    def __setitem__(self, key, value):
        if not isinstance(self.d[self.k], dict):
            return
        self.d[self.k][key] = value


def get_data_point_with_path(data, kp, rw=False):
    """根据key获取源文档树中的节点

    xxx 没看懂, 还缺测试用例

    注意：如果叶子节点是 list 类型的值，本函数会将各叶子节点合并后返回。

    :param data:
    :param kp: str, keypath
    :param rw: 以读写方式获取
    :return:
    """
    parts = _key_to_parts(kp)

    def _get_data_point(data, parts, rw):
        if len(parts) == 1 and isinstance(data, dict) and parts[0] in data:
            key = parts[0]
            val = data[key]
            if isinstance(val, list):
                return [Point(val, i) for i in range(len(val))] if rw else [Point([copy.deepcopy(d)], 0) for d in val]
            else:
                return [Point(data, key)] if rw else [Point({key: copy.deepcopy(val)}, key)]

        if isinstance(data, list):
            tmp_list = [_get_data_point(d, parts, rw) for d in data]
            return reduce(lambda x, y: x + y, tmp_list) if tmp_list else []

        elif isinstance(data, dict):
            return _get_data_point(data.get(parts[0]), parts[1:], rw)

        return []

    return _get_data_point(data, parts, rw) if parts else []


################################################################################
###  根据点位 keypath 操作文档对象
################################################################################

def get_real_val(data, key, ensure_str=True, keep_self=False, is_copy=False, is_no_empty=False):
    """根据给定 key list 获取文档对象中对应点位的单值结果(取多值中的第一个值)

    :param data:dict, mongo 中的文档对象
    :param key: mix, 可以是以 '|' 或 '.' 分隔的 key 路径，也可以是列表
    :param ensure_str: bool, 是否确保结果为字符串
    :return: mix

    示例:
    >>> get_real_val({'a':{'b':{}}}, 'a|b|c')
    >>> get_real_val({'a':{'b':{'c':[]}}}, 'a|b|c')
    >>> get_real_val({'a':{'b':{'c':['test', 'test1']}}}, 'a|b|c')
    'test'
    >>> get_real_val({'a':{'b':{'c':['test']}}}, 'a|b', ensure_str=True)
    '{"c": ["test"]}'
    >>> get_real_val({'a':{'b':{'c':['test']}}}, 'a|b', ensure_str=False)
    {'c': ['test']}
    """
    vals = get_real_lst(data, key, keep_self, is_copy)
    # 无值
    if not vals:
        return None

    # 有值
    if is_no_empty:
        for val in vals:
            if not val:
                continue
            return string.to_str(val) if ensure_str else val

    return string.to_str(vals[0]) if ensure_str else vals[0]


def get_real_lst(data, key, keep_self=False, is_copy=False):
    """根据给定 key path 获取文档对象中对应点位的所有值(列表形式)

    :param data: dict, mongo 中的文档对象
    :param key: mix, 可以是以 '|' 或 '.' 分隔的 key 路径，也可以是列表
    :return: list

    示例:
    >>> get_real_lst({'a':{'b':{}}}, 'a|b|c')
    []
    >>> get_real_lst({'a':{'b':{'c':[]}}}, 'a|b|c')
    []
    """
    parts = _key_to_parts(key)

    def _do_traverse(parts, idx, rec, vals):
        # 已达到 key path 的指定深度
        if idx == len(parts):
            # 若当前结点为列表则将其元素全部加入结果集, 否则将非 None 值的当前结点直接加入结果集
            if keep_self:
                vals.append(rec if not is_copy else copy.deepcopy(rec))
            else:
                if isinstance(rec, list):
                    vals.extend(rec if not is_copy else copy.deepcopy(rec))
                elif rec is not None:
                    vals.append(rec if not is_copy else copy.deepcopy(rec))
            return

        # 尚未达到 key path 指定深度
        if isinstance(rec, list):
            # 若当前结点为列表则深入遍历其中的每个元素
            for obj in rec:
                _do_traverse(parts, idx, obj, vals)

        elif isinstance(rec, dict):
            # 若当前结点为字典且当前 key 对应值非 None 则深入一个层级
            part = parts[idx]
            obj = rec.get(part)
            if obj is not None:
                _do_traverse(parts, idx + 1, obj, vals)

    vals = []
    _do_traverse(parts, 0, data, vals)

    return vals


def isset(data, key):
    """判断点位是否存在

    :param data: dict, 文档对象
    :param key: mix, 点位路径, 可以是 '.'或'|' 分隔的字符串, 也可以是数组
    :return: bool, True or False

    示例:
    >>> isset({'a': {'b': {}, }, }, 'a|b|c')
    False
    >>> isset({'a': {'b': {'c': [], }, }, }, 'a|b|c')
    True
    >>> isset({'a': {'b': {'c': [], }, }, },['a', 'b', 'c'])
    True
    >>> isset({'a': [{'b': [{'c': [], }]}],}, 'a.b.c')
    True
    """
    parts = _key_to_parts(key)

    def _do_isset(parts, idx, rec):
        # 已经达 key path 的指定深度, 只要结点为非 None 值, 则表示点位存在
        if idx == len(parts):
            return True if rec is not None else False

        # 尚未达到 key path 指定深度
        if isinstance(rec, list):
            # 若结点为列表, 则只要列表中任意一个元素满足条件即可
            return any([_do_isset(parts, idx, obj) for obj in rec])

        elif isinstance(rec, dict):
            # 若结点为字典且 key 对应值非 None 则深入一个层级
            part = parts[idx]
            obj = rec.get(part)
            if obj is not None:
                return _do_isset(parts, idx + 1, obj)

        return False

    return _do_isset(parts, 0, data)


def _key_to_parts(key):
    """将点位路径切分为数组

    :param key: mix, 点位路径, 可以是 '.'或'|' 分隔的字符串, 也可以是数组
    :return: list
    """
    if not isinstance(key, str) and not isinstance(key, list):
        return []

    if isinstance(key, list):
        return key

    return list(filter(lambda x: x, key.replace('.', '|').lstrip('|').split('|')))


def set_value(record, keypath, value, allow_empty=True):
    """对象设值点位值

    :param record: 对象
    :param keypath: 点位
    :param value: 值
    :param allow_empty: 是否允许为空
    :return:

    示例:
    >>> set_value({'a': {}}, 'a', ['test'])
    {'a': ['test']}
    >>> set_value({'a': {'b': {}}}, 'a|b|c', 'test')
    {'a': {'b': {'c': 'test'}}}
    >>> set_value({'a': {'b': []}}, 'a|b|c', 'test')
    {'a': {'b': [{'c': 'test'}]}}
    >>> set_value({'a': {'b': [7, {'e': 12, }]}}, 'a|b|c|d', 'test')
    {'a': {'b': [7, {'e': 12, 'c': {'d': 'test'}}]}}
    """
    if value is None:
        return record

    if not allow_empty and not value:
        return record

    parts = _key_to_parts(keypath)

    def _do_traverse(rec, parts, value):
        if isinstance(rec, list):
            # 判断列表中是否包含字典, 没有则补一个空字典
            has_dct = any([isinstance(r, dict) for r in rec])
            if not has_dct:
                rec.append({})

            for r in rec:
                # 只处理字典类型的数据
                if not isinstance(r, dict):
                    continue
                _do_traverse(r, parts, value)

        elif isinstance(rec, dict):
            if len(parts) == 1:
                rec[parts[0]] = value
            else:
                first_key = parts.pop(0)
                if first_key not in rec:
                    rec[first_key] = {}
                _do_traverse(rec[first_key], parts, value)

    _do_traverse(record, parts, value)

    return record


def set_value_std(record, keypath, value, allow_empty=True):
    """对象设值点位值

    :param record: 对象
    :param keypath: 点位
    :param value: 值
    :param allow_empty: 是否允许为空
    :return:
    """

    return set_value(record, keypath + '|std', value, allow_empty)


def remove_keys(data, keys):
    if isinstance(data, list):
        return [remove_keys(v, keys) for v in data]
    if isinstance(data, dict):
        tmp_key_lst = [k for k in keys if '|' not in k]
        for k in tmp_key_lst:
            if k in data:
                del data[k]
        keys = [k.split('|') for k in keys if '|' in k]
        keys = [(k[0], '|'.join(k[1:])) for k in keys]
        tmp_key_dic = {}
        for k in keys:
            tmp_key_dic.setdefault(k[0], [])
            tmp_key_dic[k[0]].append(k[1])
        for k in tmp_key_dic:
            if k in data:
                data[k] = remove_keys(data[k], tmp_key_dic[k])
    return data


def remove_empty(record):
    """
    裁剪空的点位
    :param record:
    :return:
    """
    if isinstance(record, list):
        record = [item for item in record if not is_empty(remove_empty(item))]
    elif isinstance(record, dict):
        for k, v in list(record.items()):
            v = remove_empty(v)
            if is_empty(v):
                del record[k]
            else:
                record[k] = v

    return record


def is_empty(item):
    """
    判断是否是list或dict， 且为空
    :param item:
    :return:
    """
    if not item:
        return True
    if isinstance(item, list) or isinstance(item, dict) or isinstance(item, str):
        return not item
    return False


def deep_merge_dic(dic1, dic2):
    """
    字典2深度遍历，合并到字典1
    注意：两个字典中不能有路径完全相同的两个叶子
    :param dic1:
    :param dic2:
    :return:
    """
    if isinstance(dic1, dict) and isinstance(dic2, dict):
        for key in dic2:
            if key not in dic1:
                dic1[key] = dic2[key]
            else:
                dic1[key] = deep_merge_dic(dic1[key], dic2[key])
    elif isinstance(dic1, list):
        if not isinstance(dic2, list):
            dic2 = [dic2]
        dic1.extend(dic2)
    else:
        dic1 = dic2
    return dic1


def get_val_raw(data, key, *args, **kwargs):
    """
    调用获取点位中的 raw 值
    :return:
    """

    # 有可能传入的分隔符是 {.}, 统一修正为 {|}
    key = key.replace('.', '|')

    if 'raw' not in key:
        key += '|raw'

    return get_real_val(data, key, *args, **kwargs)


def get_val(data, key, raw_optional=False, *args, **kwargs):
    """
    获取点位中的 std 值
    如果 raw_optional = True, 获取不到 std 结果(std 点位不存在), 返回 raw
    :return:
    """

    # 有可能传入的分隔符是 {.}, 统一修正为 {|}
    key = key.replace('.', '|')

    if raw_optional:
        if key.endswith('std') or key.endswith('raw'):
            # 去掉结尾
            key = key[:-4]

        if 'ensure_str' in kwargs:
            del kwargs['ensure_str']
        group = get_real_val(data, key, ensure_str=False, *args, **kwargs)

        # 不存在 std, 去获取 raw
        if not isset(group, 'std'):
            k = 'raw'
        else:
            k = 'std'

        return get_real_val(group, k, *args, **kwargs)

    # else: 获取 std 结果
    if 'std' not in key:
        key += '|std'
    return get_real_val(data, key, *args, **kwargs)


def get_lst(data, key, raw_optional=False, *args, **kwargs):
    """
    获取点位中的 std 值
    如果 raw_optional = True, 获取不到 std 结果(std 点位不存在), 返回 raw
    :return:
    """

    # 有可能传入的分隔符是 {.}, 统一修正为 {|}
    key = key.replace('.', '|')

    if raw_optional:
        if key.endswith('std') or key.endswith('raw'):
            # 去掉结尾
            key = key[:-4]

        group = get_real_lst(data, key, *args, **kwargs)

        # 不存在 std, 去获取 raw
        if not isset(group, 'std'):
            k = 'raw'
        else:
            k = 'std'

        return get_real_lst(group, k, *args, **kwargs)

    # else: 获取 std 结果
    if 'std' not in key:
        key += '|std'
    return get_real_lst(data, key, *args, **kwargs)
