#!/bin/env python3
import requests
import os

# AIに追加で聞いて足した部分
from dotenv import load_dotenv
load_dotenv()

# Cloudflare APIキーとゾーンIDを環境変数から取得
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
CLOUDFLARE_ZONE_ID = os.getenv('CLOUDFLARE_ZONE_ID')

# 更新したいDNSレコードの名前と新しいIPアドレス
DNS_RECORD_NAME = os.getenv('DNS_RECORD_NAME')

# この関数は前に書いたのを流用
def get_global_ip() -> str :
    '''
    Returns
    -------
    global_ip : str
        This machine's Global IP Address
    '''
    global_ip = requests.get('https://ifconfig.me/ip').text
    return global_ip

NEW_IP_ADDRESS = get_global_ip()    # IPべた書きだったのを関数で取得に変更

headers = {
    'Authorization': f'Bearer {CLOUDFLARE_API_TOKEN}',
    'Content-Type': 'application/json'
}

# DNSレコードのIDを取得
response = requests.get(f'https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records?name={DNS_RECORD_NAME}', headers=headers)
record_id = response.json()['result'][0]['id']

# DNSレコードを更新
data = {
    'type': 'A',
    'name': DNS_RECORD_NAME,
    'content': NEW_IP_ADDRESS,
    'proxied': True
}
response = requests.put(f'https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records/{record_id}', headers=headers, json=data)

if response.status_code == 200:
    print('DNS record updated successfully.')
else:
    print('Failed to update DNS record.')
    print(response.text)
