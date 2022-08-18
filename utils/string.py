import json
import re

SBC_DBC_DCT = {
    '０': '0',
    '１': '1',
    '２': '2',
    '３': '3',
    '４': '4',
    '５': '5',
    '６': '6',
    '７': '7',
    '８': '8',
    '９': '9',
    'Ａ': 'A',
    'Ｂ': 'B',
    'Ｃ': 'C',
    'Ｄ': 'D',
    'Ｅ': 'E',
    'Ｆ': 'F',
    'Ｇ': 'G',
    'Ｈ': 'H',
    'Ｉ': 'I',
    'Ｊ': 'J',
    'Ｋ': 'K',
    'Ｌ': 'L',
    'Ｍ': 'M',
    'Ｎ': 'N',
    'Ｏ': 'O',
    'Ｐ': 'P',
    'Ｑ': 'Q',
    'Ｒ': 'R',
    'Ｓ': 'S',
    'Ｔ': 'T',
    'Ｕ': 'U',
    'Ｖ': 'V',
    'Ｗ': 'W',
    'Ｘ': 'X',
    'Ｙ': 'Y',
    'Ｚ': 'Z',
    'ａ': 'a',
    'ｂ': 'b',
    'ｃ': 'c',
    'ｄ': 'd',
    'ｅ': 'e',
    'ｆ': 'f',
    'ｇ': 'g',
    'ｈ': 'h',
    'ｉ': 'i',
    'ｊ': 'j',
    'ｋ': 'k',
    'ｌ': 'l',
    'ｍ': 'm',
    'ｎ': 'n',
    'ｏ': 'o',
    'ｐ': 'p',
    'ｑ': 'q',
    'ｒ': 'r',
    'ｓ': 's',
    'ｔ': 't',
    'ｕ': 'u',
    'ｖ': 'v',
    'ｗ': 'w',
    'ｘ': 'x',
    'ｙ': 'y',
    'ｚ': 'z',
    '（': '(',
    '）': ')',
    '〔': '(',
    '〕': ')',
    '【': '[',
    '】': ']',
    '〖': '[',
    '〗': ']',
    '“': '"',
    '”': '"',
    '‘': '\'',
    '’': '\'',
    '｛': '{',
    '｝': '}',
    '《': '<',
    '》': '>',
    '％': '%',
    '＋': '+',
    '—': '-',
    '－': '-',
    '～': '~',
    '：': ':',
    '。': '.',
    '、': ',',
    '，': ',',
    '；': ';',
    '？': '?',
    '！': '!',
    '…': '-',
    '‖': '|',
    '｜': '|',
    '〃': '"',
    '　': ' ',
    '×': '*',
    '．': '.',
    '＊': '*',
    '＆': '&',
    '＜': '<',
    '﹤': '<',
    '＞': '>',
    '＄': '$',
    '＠': '@',
    '＾': '^',
    '＿': '_',
    '＂': '"',
    '￥': '$',
    '＝': '=',
    '＼': '\\',
    '／': '/',
}


def to_str(s):
    """将给定数据转换为 unicode 字符串

    :param s: any, 待转换的数据源
    :return:

    示例:
    >>> to_str(None)
    'null'
    >>> to_str(123)
    '123'
    >>> to_str([1, 2, 3])
    '[1, 2, 3]'
    >>> to_str({'a': '测试1'})
    '{"a": "测试1"}'
    >>> to_str({'a': 'test', 'b': [1, 2, 3]})
    '{"a": "test", "b": [1, 2, 3]}'
    """
    if isinstance(s, str):
        return s

    return json.dumps(s, ensure_ascii=False)


def element_to_str(data):
    """将给定数据的元素转换为 str 字符串

    :param data: any
    :return: mix
    """

    def _f(data):
        if isinstance(data, list):
            return [_f(s) for s in data]
        elif isinstance(data, dict):
            return {k: _f(v) for k, v in data.items()}
        else:
            return str(data)

    return _f(data)


def is_link(s):
    """判断给定数据是否是一个带链接的字符串

    :param  s: str, 待判定的字符串
    :return: True or False

    示例:
    >>> is_link('http://abc')
    True
    >>> is_link('ahttp://abc')
    False
    >>> is_link('qiniu://abc')
    True
    """
    if not isinstance(s, str):
        return False

    link_prefix_lst = ('qiniu:', 'https:', 'http:', 'ftp:')

    return any([s.startswith(prefix) for prefix in link_prefix_lst])


def strtr(s, replace_pairs):
    """替换字符串中特定的字符

    :param s: str, 需要处理的字符串
    :param replace_pairs: dict, {'替换前字符串': 替换后字符串}
    :return: str, 替换后的字符串

    示例:
    >>> strtr('aaa-bb-aabc', {'aa': '&&', 'aaa': 'AAA', 'bb': 'BB'})
    'AAA-BB-&&bc'
    >>> strtr('０１２', {'０': '0', '１': '1', '２': '2'})
    '012'
    """
    if not isinstance(s, str):
        return s

    pattern = '|'.join(map(re.escape, sorted(replace_pairs, key=len, reverse=True)))

    return re.sub(pattern, lambda m: replace_pairs[m.group()], s)


def sbc2dbc(s):
    """将全角字符串替换为半角 unicode 字符串

    :param s: str, 需要处理的字符串
    :return: str, 替换后的字符串

    示例:
    >>> sbc2dbc('０１２')
    '012'
    """
    if not isinstance(s, str):
        return s

    return strtr(s, SBC_DBC_DCT)
