import os
import json

import yaml
from fsspec.implementations.sftp import SFTPFileSystem


def 不许看(s):
    for entity_id in sorted(所有entity_id | 所有device_id, key=len, reverse=True):
        s = s.replace(entity_id, '不许看！')
    return s


fs = SFTPFileSystem(host='raspberrypi', username='****', password='****')

所有entity_id = {i['entity_id'] for i in json.loads(fs.open('/home/homeassistant/.homeassistant/.storage/core.entity_registry', encoding='utf8').read())['data']['entities']}
所有device_id = {i['id'] for i in json.loads(fs.open('/home/homeassistant/.homeassistant/.storage/core.device_registry', encoding='utf8').read())['data']['devices']}


源 = fs.open('/home/homeassistant/.homeassistant/automations.yaml').read()
with open(f'automations.yaml', 'wb') as f:
    f.write(源)
for d in yaml.safe_load(源):
    if not d.get('alias'):
        continue
    del d['id']
    名字 = d.pop('alias')
    文件夹 = '其他'
    if '-' in 名字:
        文件夹 = 名字.split('-')[0].strip()
    os.makedirs(f'automations/{文件夹}', exist_ok=True)
    with open(f'automations/{文件夹}/{名字}.yaml', 'w', encoding='utf8') as f:
        f.write(不许看(yaml.dump(d, allow_unicode=True, width=9999, sort_keys=False)))
