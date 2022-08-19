
# -*- coding: utf-8 -*-
import zlib
import json
import base64
from argparse import ArgumentParser
from collections import deque
from deploy.fw_user import fw_user_keys
import codecs
import hashlib
import time


print(time.strftime('%Y-%m-%d %H:%M:%S'))

a = {"a": True}

print(a.update({"b": True}))
exit()


xx = '2_3_4_5_6_7'

xx = 'asdasd_123'

xx = xx.split('_')
print(xx)

xx = '_'.join(xx[:-1])

print(xx)

exit()

content = codecs.open('', mode='r', encoding='utf').read()
content = content.split("\n")
for line in content:
    line = json.loads(line)
    print(json.dumps(line, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': ')))

exit()
"""
cache_model.model_keys = base64.b64encode(
    zlib.compress(json.dumps(model_keys).encode(encoding='utf-8'))
)
"""

with open('', mode='r') as fp:
    content = fp.read()

x = ""
x.split("\t")
x = zlib.decompress(base64.b64decode(x))
x = json.loads(x)
json.dumps(x).encode(encoding='utf-8')

exit()
x = "abcdefghijk"
y = "defghi"

offset_len = len(x) - len(y)
for offset in range(0, offset_len + 1):
    if x[offset:offset + len(y)] == y:
        print("True")

exit()

salt = "linddoc#$!#$%@##"
x = "zy13839089316"
x += salt
x = hashlib.md5(x.encode('utf-8'))
print(x.hexdigest())
x = "secret"
x += salt
x = hashlib.md5(x.encode('utf-8'))
print(x.hexdigest())
x = "linkdoc123"
x += salt
x = hashlib.md5(x.encode('utf-8'))
print(x.hexdigest())

sql = "INSERT INTO `users` " \
      "(`uid`, `name`, `gender`, `username`, `email`, `mobile`, `password`, `init_password`, `internal`, `status`, `temp_status`, `last_login_ip`, `client`, `type`, `ip`, `operator_id`) " \
      "VALUES (4, '郑燕', 2, '15713660065', '', '', '87702fb855550fadbca0e61a5630421b', 0, 0, 0, 0, '', '', '', '', -1)," \
      "(5, '治东', 2, '15168838570', '', '', '8aaf7a10393db11643ed4c2ec3fe51ae', 0, 0, 0, 0, '', '', '', '', -1)," \
      "(6, '156000000001', 2, '15168838570', '', '', 'f01cc566f7aed1d2ab5627b66c0c2f4b', 0, 0, 0, 0, '', '', '', '', -1)," \
      "(7, '156000000002', 2, '15168838570', '', '', 'f01cc566f7aed1d2ab5627b66c0c2f4b', 0, 0, 0, 0, '', '', '', '', -1)," \
      "(8, '156000000003', 2, '15168838570', '', '', 'f01cc566f7aed1d2ab5627b66c0c2f4b', 0, 0, 0, 0, '', '', '', '', -1);"
print(sql)
exit()

content = codecs.open("/Users/chenchao/Downloads/consul_test_fw-user_raw.json", encoding='utf8').read()
content = json.loads(content)

for v in content:
    key = str(v['key']).split("/")
    del key[0]
    key = "/".join(key)
    if key in fw_user_keys:
        fw_user_keys[key] = v['value']
print(json.dumps(fw_user_keys, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': ')))
exit()
# ========================================

content = codecs.open("/Users/chenchao/Downloads/consul_kv_hz_20220726.json", encoding='utf8').read()

content = json.loads(content)

for v in content:
    v["value"] = str(base64.b64decode(v["value"]), 'utf-8')
    # print(v)

content = json.dumps(content, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ': '))

codecs.open("/Users/chenchao/Downloads/consul_kv_hz_20220726.json", 'w').write(content)
